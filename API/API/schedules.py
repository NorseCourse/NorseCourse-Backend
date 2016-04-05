

from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import ScheduleCreationObject

from API import config
import string
import time
import itertools
import ast
import datetime
import random


@API.route("/schedules")
class ScheduleCreation(Resource):

	# Function that takes a class time and a check time
	# it checks if the check time is in between start and end time of class
	# returns True if it is, meaning there is a time conflic
	def betweenTimes(self,original,check):
		# Spilt original to start and end times
		original_start = original[0]
		original_end = original[1]

		if original_start.tm_wday == check.tm_wday:
			if original_start <= check <= original_end:
				return True
		return False



	# Function that takes start and end times of a schedule
	# It checks if they are all inbetween time range given
	# returns True if there is a conflict
	def validTimes(self, starts, ends, sect_times):

		for sect in sect_times:
			if sect == None:
				print("\n\n")
				print(sect_times)
				print("\n\n")
			for day in sect:
				for x in range(5):
					if starts[x].tm_wday == day[0].tm_wday:
						if starts[x] > day[0] or day[1] > ends[x]:
							return True
		return False 


	# Function that takes two classes and checks if they conflict in time
	# it calls the betweenTimes function above
	# Return True if time conflic, False otherwise
	def checkTimeConflict(self,one,two):

		start_one = one[0]
		end_one = one[1]

		start_two = two[0]
		end_two = two[1]

		if self.betweenTimes((start_one,end_one),start_two):
			return True
		if self.betweenTimes((start_one,end_one),end_two):
			return True

		return False


	# Function takes a schedule (list of section ids), and checks for time conflict
	# it calls checkTimeConflict function above, between all combos of two classes in schedule
	# returns True if there is a time conflict, and false otherwise
	def checkScheduleConflict(self,section_ids,time_range):

		sections = []
		# create dictionary for datetime days of week
		days_dict = {'M':'2','T':'3','W':'4','R':'5','F':'6'}

		# go through all sections in schedule
		for section_id in section_ids:

			# get start and end times of section
			sectionQuery = "SELECT start_time, end_time, days FROM SectionMeetings WHERE section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(section_id))

			for (start_time, end_time, days) in cursor:
				start_time = start_time
				end_time = end_time
				days = days

			cursor.close()
			cnx.close()

			# if times of course are not listed, then these values with be nan
			# if thats the case there is no time to add
			if start_time == "nan" or end_time == "nan" or days == "nan":
				sections.append((None,None))

			# there is a time and day listed for the section
			else:

				# create a list of datetime objects for each section meeting time
				times = []
				for day in range(len(days)):

					d = str(days_dict[str(days[day])])

					st = time.strptime(str(start_time)+' '+d, '%H:%M %w')
					et = time.strptime(str(end_time)+' '+d, '%H:%M %w')
					times.append((st,et))

				# append list of times to list of sections
				sections.append((times,len(days)))


		# go through every section, comparing it to every other section
		# within each section, compare if there is a time conflict between each meeting time
		for section1 in range(len(sections)):
			for section2 in range(section1,len(sections)):
				if sections[section2] != (None,None) and sections[section1] != (None,None) and section1 != section2:
					# have one section comparing it to another, get every time they meet
					for time1 in range(sections[section1][-1]):
						for time2 in range(sections[section2][-1]):
							if self.checkTimeConflict(sections[section1][0][time1],sections[section2][0][time2]):
								return True

		if time_range != []:
			sect_times = []
			for sect in sections:
				if sect[0] != None:
					sect_times.append(sect[0])

			valid_starts = []
			valid_ends = []
			for x in ['2','3','4','5','6']:
				valid_starts.append(time.strptime(time_range[0]+' '+x, '%H:%M %w'))
				valid_ends.append(time.strptime(time_range[1]+' '+x, '%H:%M %w'))

			# returns False if there was no time conflict was found in schedule, return False meaning its a valid schedule time wise
			# returns True if the schedule does not fit inbetween req time block, meaning its a bad schedule
			return self.validTimes(valid_starts,valid_ends,sect_times)

		return False


	# function takes a schedule (list of section ids)
	# checks if two sections are the same course within the schedule
	def checkSameCourse(self,schedule):
		course_ids = []
		# go through each section in schedule
		for section_id in schedule:

			# get course id of section
			sectionQuery = "SELECT course_id FROM Sections WHERE section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(section_id))

			for (course_id) in cursor:
				if course_id not in course_ids:

					# add course id to list of course ids in schedule
					course_ids.append(course_id)

			cursor.close()
			cnx.close()


		# if the amount of courses in schedule is different than the amount of sections,
		# then there are duplicate courses, so return True, meaning a bad schedule
		# if no two sections are the same course, then its valid schedule and return False
		if len(course_ids) != len(schedule):
			return True
		return False


	# Function checks if any sections in schedule have a required lab course
	def checkLab(self,schedule):
		labs = []
		# go through each section in schedule
		for section_id in schedule:
			sectionQuery = "SELECT req_type,details FROM Sections,Courses,Requirements WHERE Sections.course_id = Courses.course_id and Courses.course_id = Requirements.course_id and Sections.section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(section_id))

			labs = None

			# check if there is a lab
			for (req_type,details) in cursor:
				if req_type == "LAB":
					labs = ast.literal_eval(details)

			cursor.close()
			cnx.close()

			# if there is a lab for any section, return True
			if labs != None:
				return True

		# if no lab for any section, return False
		return False



	# Function takes a schedule and adds labs to any courses needing one
	def addLab(self,schedule,time_range):
		schedule = list(schedule)
		labs = []

		# goes through each section in schedule
		for section_id in schedule:
			
			sectionQuery = "SELECT req_type,details FROM Sections,Courses,Requirements WHERE Sections.course_id = Courses.course_id and Courses.course_id = Requirements.course_id and Sections.section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(section_id))

			labs = None
			for (req_type,details) in cursor:
				if req_type == "LAB":
					labs = ast.literal_eval(details)

			cursor.close()
			cnx.close()

			# find labs for this section and add them below

			if labs != None:
				added = False

				# goes through each potential lab for section
				for lab in labs:
					if not added:

						sectionQuery = "SELECT section_id FROM Sections WHERE name = %s"

						cnx = cnx_pool.get_connection()
						cursor = cnx.cursor()

						cursor.execute(sectionQuery % str("'"+lab+"'"))

						for (section_id) in cursor:
							lab_id = section_id[0]

						cursor.close()
						cnx.close()

						schedule.append(lab_id)

						# if the lab fits into schedule, it will be added
						if (not self.checkScheduleConflict(schedule,time_range)):
							added = True
						else:
							schedule = schedule[:-1]

				# if a lab was added, then added = True
				# if no lab fit into schedule, return False
				if added == False:
					return False

		# after all sections have labs added and they fit into schedule, return the new schedule
		return schedule



	# Function takes a schedule and find if it has a good amount of credits
	def checkBadCredits(self,schedule, maxCredits, minCredits):

		# default to no credits
		credits = 0

		for sect in schedule:

			sectionQuery = "SELECT min_credits FROM Sections WHERE section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(sect))

			for (min_credits) in cursor:
				# add credits for each section
				credits += int(min_credits[0])

			cursor.close()
			cnx.close()

		# if bad schedule
		if credits > maxCredits:
			return True

		if credits < minCredits:
			return True

		# if good schedule
		return False


	# Function that takes a schedule and returns the amount of credits
	def getNumCredits(self, schedule):
		# default to no credits
		credits = 0

		for sect in schedule:

			sectionQuery = "SELECT min_credits FROM Sections WHERE section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(sect))

			for (min_credits) in cursor:
				# add credits for each section
				credits += int(min_credits[0])

			cursor.close()
			cnx.close()

		return credits





	# Function checks if a schedule is a valid schedule or not
	# returns True schedule if it is valid, and False if not
	def verify(self,schedule, maxCredits, minCredits,time_range):

		# checks if there is a lab in schedule
		if self.checkLab(schedule):
			# trys to add lab to schedule
			s = self.addLab(schedule,time_range)
			# if lab fit into schedule
			if s != False:
				# update schdule with lab
				schedule = s

			# lab did not fit into schedule
			else:
				# schedule does not work
				return False

		# check if there is a time conflict in schedule
		if self.checkScheduleConflict(schedule,time_range):
			# if there is a time conflict, invalid schedule
			return False

		# check if there are duplicate courses in schdule
		if self.checkSameCourse(schedule):
			# there were duplicates
			return False

		# check if there are too many or too little credits
		if self.checkBadCredits(schedule,maxCredits,minCredits):
			# there was a bad amount of credits
			return False

		# it was a valid schedule, so return the schedule
		return schedule



	# Function checks if a schedule is a valid schedule or not
	# returns True schedule if it is valid, and False if not
	def verifyBest(self,schedule,time_range):

		# checks if there is a lab in schedule
		if self.checkLab(schedule):
			# trys to add lab to schedule
			s = self.addLab(schedule,time_range)
			# if lab fit into schedule
			if s != False:
				# update schdule with lab
				schedule = s

			# lab did not fit into schedule
			else:
				# schedule does not work
				return False

		# check if there is a time conflict in schedule
		if self.checkScheduleConflict(schedule,time_range):
			# if there is a time conflict, invalid schedule
			return False

		# check if there are duplicate courses in schdule
		if self.checkSameCourse(schedule):
			# there were duplicates
			return False

		# it was a valid schedule, so return the schedule
		return schedule



	# define parameters for api

	@NorseCourse.doc(
		params = {
			"requiredCourses": "Provide a comma separated list of courses IDs that are required in schedule, defaults to nothing",
			"preferredCourses": "Provide a comma separated list of courses IDs that are preferred in schedule, defaults to nothing",
			"requiredGenEds": "Provide a comma separated list of Gen Ed abbreviation strings required, defaults to nothing",
			"preferredGenEds": "Provide a comma separated list of Gen Ed abbreviation strings preferred, defaults to nothing",
			"minCredits": "Provide an integer for maximum number of credits wanted, defaults to 12",
			"maxCredits": "Provide an integer for maximum number of credits wanted, defaults to 18",
			"index": "Provide an integer of last location in schedule list, if known, defaults to -1",
			"limit":"Provide a max amount of schdedules wanted to be returned, defaults to 20",
			"requiredTimeBlock":"Provide comma seperated times, start time and end time Example: 9:00,14:00, defaults to any time allowed",
			"requiredSections": "Provide a comma separated list of section IDs that are required in schedule, defaults to nothing",
			"preferredSections": "Provide a comma separated list of section IDs that are preferred in schedule, defaults to nothing.  Allow one per course."
		}
	)


	# function that takes parameters and returns JSON schedule
	def get(self):

		# initalize error message
		error = "No errors"

		#######################################################
		# checks if limit is empty
		lim = request.args.get("limit")
		# if not empty, it is int
		if lim != None:
			limit = int(lim)

		# if empty, default to 20
		else:
			limit = 20


		#######################################################
		# checks if max credits are empty
		maxnc = request.args.get("maxCredits")
		# if not empty, it is int
		if maxnc != None:
			maxNumCredits = int(maxnc)

		# if empty, default to 18
		else:
			maxNumCredits = 18


		#######################################################
		# checks if min credits are empty
		minnc = request.args.get("minCredits")
		# if not empty, it is int
		if minnc != None:
			minNumCredits = int(minnc)

		# if empty, default to 18
		else:
			minNumCredits = 12


		#######################################################
		# checks if requirements are empty
		r = request.args.get("requiredCourses")
		# if not empty, create list
		if r != None:
			required_courses = (r).split(',')

		# if empty, make empty list
		else:
			required_courses = []


		#######################################################
		# check if preferred are empty
		p = request.args.get("preferredCourses")
		# if not empty, create list
		if p != None:
			preferred_courses = (p).split(',')

		# if empty, make empty list
		else:
			preferred_courses = []


		#######################################################
		# checks if requirements are empty
		r = request.args.get("requiredSections")
		# if not empty, create list
		if r != None:
			required_sections = (r).split(',')

		# if empty, make empty list
		else:
			required_sections = []


		#######################################################		
		# check if preferred are empty
		p = request.args.get("preferredSections")
		# if not empty, create list
		if p != None:
			preferred_sections = (p).split(',')

		# if empty, make empty list
		else:
			preferred_sections = []


		#######################################################
		# check if preferred are empty
		rtb = request.args.get("requiredTimeBlock")
		# if not empty, create list
		if rtb != None:
			req_time_block = (rtb).split(',')

		# if empty, make empty list
		else:
			req_time_block = []


		#######################################################
		# check if geneds are empty
		g = request.args.get("requiredGenEds")
		# if not empty create list
		if g != None:
			req_geneds = (g).split(',')

		# if empty, make empty list
		else:
			req_geneds = []


		#######################################################
		# check if geneds are empty
		g = request.args.get("preferredGenEds")
		# if not empty create list
		if g != None:
			preferred_geneds = (g).split(',')

		# if empty, make empty list
		else:
			preferred_geneds = []


		#######################################################
		# check if index is empty
		i = request.args.get("index")
		# if not empty, make int
		if i != None:
			index = int(i)

		# if empty, default to -1
		else:
			index = -1


		#######################################################
		#######################################################
		##################### Format input ####################
		#######################################################
		#######################################################

		# go through required courses and make int instead of unicode
		new_r = []
		for x in required_courses:
			new_r.append(int(x))

		required_courses = new_r

		# go through preferred courses and make int instead of unicode
		new_p = []
		for x in preferred_courses:
			new_p.append(int(x))

		preferred_courses = new_p

		# go through required Sections and make int instead of unicode
		new_r = []
		for x in required_sections:
			new_r.append(int(x))

		required_sections = new_r

		# go through preferred Sections and make int instead of unicode
		new_p = []
		for x in preferred_sections:
			new_p.append(int(x))

		preferred_sections = new_p

		# go through geneds and make string instead of unicode
		new_ge = []
		for x in preferred_geneds:
			new_ge.append(str(x))

		preferred_geneds = new_ge

		# go through geneds and make string instead of unicode
		new_ge = []
		for x in req_geneds:
			new_ge.append(str(x))

		req_geneds = new_ge

		# go through times and make string instead of unicode
		new_times = []
		for x in req_time_block:
			new_times.append(str(x))

		req_time_block = new_times


		########################################################################
		########################################################################
		####################### Begin Creating Schedule ########################
		########################################################################
		########################################################################

		# add all sections of required courses
		temp = required_courses

		# list of (lists of sections for a given course)
		lst = []

		# Add all required setions
		for sect in required_sections:
			lst.append([sect])


		for c in temp:
			alreadyAdded = False

			classQuery = "SELECT section_id from Sections where course_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(classQuery % (str(c)))

			sects = []
			for (section_id) in cursor:
				if [section_id[0]] in lst:
					alreadyAdded = True
				else:
					sects.append(section_id[0])

			if not alreadyAdded:
				lst.append(sects)

			cursor.close()
			cnx.close()


		# Add all preferred setions
		for sect in preferred_sections:
			lst.append([sect])


		# add all sections of preferred courses
		temp = preferred_courses

		for c in temp:
			alreadyAdded = False

			classQuery = "SELECT section_id from Sections where course_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(classQuery % (str(c)))

			sects = []
			for (section_id) in cursor:
				if [section_id[0]] in lst:
					alreadyAdded = True
				else:
					sects.append(section_id[0])

			if not alreadyAdded:
				lst.append(sects)

			cursor.close()
			cnx.close()

		# Create all possible schedules from required and preferred courses and sections.
		ps = list(itertools.product(*lst))

		possible_sections = []
		for c in ps:
			possible_sections.append(list(c))


		###########################################
		# all possible schedules
		# master list of schedules
		###########################################
		all_combos = []


		# for each possible schedule with req/preferred
		for option in possible_sections:


			best = option
			required = best[:(len(required_courses) + len(required_sections))]
			preferred = best[(len(required_courses)+len(required_sections)):]

			# if the best schedule is valid
			best = self.verifyBest(best,req_time_block)

			if best != False:

				numCredits = self.getNumCredits(best)

				# if the best schedule has a valid amount of credits wanted, add schedule
				if minNumCredits <= numCredits <= maxNumCredits:
					all_combos += [best]

				# if more courses can be added
				if (numCredits < maxNumCredits):
					num_needed = maxNumCredits - numCredits

					# if gen eds are wanted, add gen eds
					if len(req_geneds) + len(preferred_geneds) > 0:

						# checks if req/preferred classes cover any gen eds required.
						for gened in range(len(req_geneds)):
							for section in best:
								classQuery = "SELECT abbreviation from GenEdFulfillments, GenEds where ((GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)) and GenEdFulfillments.section_id = %s"

								cnx = cnx_pool.get_connection()
								cursor = cnx.cursor()

								cursor.execute(classQuery % (str("'"+req_geneds[gened]+"'"),str("'"+req_geneds[gened]+"'"),str("'"+str(section)+"'")))

								abbs = []
								for (abbreviation) in cursor:
									abbs.append(str(abbreviation[0]))

								for ge in abbs:
									if ge in req_geneds:
										req_geneds.remove(ge)
									if ge in preferred_geneds:
										preferred_geneds.remove(ge)

								cursor.close()
								cnx.close()

						# find all classes that cover required gen eds
						possible_gened_classes = {}
						for gened in range(len(req_geneds)):

							classQuery = "SELECT section_id from GenEdFulfillments, GenEds where (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)"

							cnx = cnx_pool.get_connection()
							cursor = cnx.cursor()

							cursor.execute(classQuery % (str("'"+req_geneds[gened]+"'"),str("'"+req_geneds[gened]+"'")))

							classes = []
							for (section_id) in cursor:
								classes.append(section_id[0])

							possible_gened_classes[req_geneds[gened]] = classes

							cursor.close()
							cnx.close()

						# find all classes that cover preferred gen eds
						for gened in range(len(preferred_geneds)):

							classQuery = "SELECT section_id from GenEdFulfillments, GenEds where (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)"

							cnx = cnx_pool.get_connection()
							cursor = cnx.cursor()

							cursor.execute(classQuery % (str("'"+preferred_geneds[gened]+"'"),str("'"+preferred_geneds[gened]+"'")))

							classes = []
							for (section_id) in cursor:
								classes.append(section_id[0])

							possible_gened_classes[preferred_geneds[gened]] = classes

							cursor.close()
							cnx.close()

						# find common geneds
						doubles = {}

						for ge in possible_gened_classes:
							for ge2 in possible_gened_classes:
								if ge != ge2:
									for class1 in possible_gened_classes[ge]:
										for class2 in possible_gened_classes[ge2]:
											if class1 == class2:
												key = ge+" "+ge2
												if key in doubles:
													doubles[key].append(class1)
												else:
													doubles[key] = [class1] 

						# remove duplicate strings that appear in different orders
						# for example HE,HB vs HB,HE
						keys = []
						for key in doubles:
							one,two = key.split()
							new = set((one,two))
							if new not in keys:
								keys.append(new)

						for k in keys:
							delKey = list(k)[0] + " " + list(k)[1]
							del doubles[delKey]

						combo = []


						for b in best:
							combo.append([b])

						for ge in doubles:
							one,two = ge.split()
							if num_needed > 0 and ((one in req_geneds) or (one in preferred_geneds)) and ((two in req_geneds) or (two in preferred_geneds)):
								combo.append(doubles[ge])
								num_needed -= 1
								if one in req_geneds:
									req_geneds.remove(one)
								if one in preferred_geneds:
									preferred_geneds.remove(one)

								if two in req_geneds:
									req_geneds.remove(two)
								if one in preferred_geneds:
									preferred_geneds.remove(two)


						for x in possible_gened_classes:
							if num_needed > 0 and x in req_geneds:
								combo.append(possible_gened_classes[x])
								num_needed -= 1

						for x in possible_gened_classes:
							if num_needed > 0 and x in preferred_geneds:
								combo.append(possible_gened_classes[x])
								num_needed -= 1


						all_combos += list(itertools.product(*combo))


			# is best schedule is not valid for some reason
			else:
				bad = False
				best = required+preferred

				# remove courses from best until no conflict.
				while self.verifyBest(best,req_time_block) == False and len(best) >=1:
					best = best[:-1]
					if len(best) == len(required):
						error = "There was a conflict with required courses/sections"
						bad = True
				if len(best) == 0:
					error = "There was a conflict with required courses/sections"
					best = []
					bad = True

				if not bad:
					best = self.verifyBest(best,req_time_block)

					if len(best) >= len(required):

						numCredits = self.getNumCredits(best)

						# if the best schedule has a valid amount of credits wanted, add schedule
						if minNumCredits <= numCredits <= maxNumCredits:
							all_combos += [best]

						# if more courses can be added
						if (numCredits < maxNumCredits):
							num_needed = maxNumCredits - numCredits

							# if gen eds are wanted, add gen eds
							if len(req_geneds) + len(preferred_geneds) > 0:

								for gened in range(len(req_geneds)):
									for section in best:
										classQuery = "SELECT abbreviation from GenEdFulfillments, GenEds where ((GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)) and GenEdFulfillments.section_id = %s"

										cnx = cnx_pool.get_connection()
										cursor = cnx.cursor()

										cursor.execute(classQuery % (str("'"+req_geneds[gened]+"'"),str("'"+req_geneds[gened]+"'"),str("'"+str(section)+"'")))

										abbs = []
										for (abbreviation) in cursor:
											abbs.append(str(abbreviation[0]))


										for ge in abbs:
											if ge in req_geneds:
												req_geneds.remove(ge)
											if ge in preferred_geneds:
												preferred_geneds.remove(ge)


										cursor.close()
										cnx.close()



								possible_gened_classes = {}
								for gened in range(len(req_geneds)):

									classQuery = "SELECT section_id from GenEdFulfillments, GenEds where (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)"

									cnx = cnx_pool.get_connection()
									cursor = cnx.cursor()

									cursor.execute(classQuery % (str("'"+req_geneds[gened]+"'"),str("'"+req_geneds[gened]+"'")))

									classes = []
									for (section_id) in cursor:
										classes.append(section_id[0])

									possible_gened_classes[req_geneds[gened]] = classes

									cursor.close()
									cnx.close()

								for gened in range(len(preferred_geneds)):

									classQuery = "SELECT section_id from GenEdFulfillments, GenEds where (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)"

									cnx = cnx_pool.get_connection()
									cursor = cnx.cursor()

									cursor.execute(classQuery % (str("'"+preferred_geneds[gened]+"'"),str("'"+preferred_geneds[gened]+"'")))

									classes = []
									for (section_id) in cursor:
										classes.append(section_id[0])

									possible_gened_classes[preferred_geneds[gened]] = classes

									cursor.close()
									cnx.close()


								# find common geneds

								doubles = {}

								for ge in possible_gened_classes:
									for ge2 in possible_gened_classes:
										if ge != ge2:
											for class1 in possible_gened_classes[ge]:
												for class2 in possible_gened_classes[ge2]:
													if class1 == class2:
														key = ge+" "+ge2
														if key in doubles:
															doubles[key].append(class1)
														else:
															doubles[key] = [class1] 

								keys = []
								for key in doubles:
									one,two = key.split()
									new = set((one,two))
									if new not in keys:
										keys.append(new)

								for k in keys:
									delKey = list(k)[0] + " " + list(k)[1]
									del doubles[delKey]

								combo = []

								for b in best:
									combo.append([b])

								for ge in doubles:
									one,two = ge.split()
									if num_needed > 0 and ((one in req_geneds) or (one in preferred_geneds)) and ((two in req_geneds) or (two in preferred_geneds)):
										combo.append(doubles[ge])
										num_needed -= 1
										if one in req_geneds:
											req_geneds.remove(one)
										if one in preferred_geneds:
											preferred_geneds.remove(one)

										if two in req_geneds:
											req_geneds.remove(two)
										if one in preferred_geneds:
											preferred_geneds.remove(two)

								for x in possible_gened_classes:
									if num_needed > 0 and x in req_geneds:
										combo.append(possible_gened_classes[x])
										num_needed -= 1

								for x in possible_gened_classes:
									if num_needed > 0 and x in preferred_geneds:
										combo.append(possible_gened_classes[x])
										num_needed -= 1

								all_combos += list(itertools.product(*combo))

					else:
						error = "There was a conflict with required courses/sections"


		# shuffle list of all potential schedules
		# set seed so it is the same everytime
		random.seed(0)
		random.shuffle(all_combos)

		schedules = []

		pos = index
		for x in range(limit):
			if pos < len(all_combos)-1:
				pos += 1 # x for index
				current = all_combos[pos]
				while self.verify(current, maxNumCredits,minNumCredits,req_time_block) == False and pos < len(all_combos)-1:
					pos += 1
					current = all_combos[pos]

				if pos <= len(all_combos)-1:
					error = "No errors"
					schedule = ScheduleCreationObject(self.verify(current, maxNumCredits,minNumCredits,req_time_block),pos,error)
					schedules.append(schedule.__dict__)

		if schedules == []:
			if error == "No errors":
				error = "No valid schedules can be made from the given criteria"
			s = ScheduleCreationObject([],pos,error)
			schedules.append(s.__dict__)

		return (schedules)