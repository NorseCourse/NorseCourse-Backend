

from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  NorseCourseObjects import ScheduleCreationObject

import config
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
	def checkScheduleConflict(self,section_ids):

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

		# no time conflict was found in schedule, return False meaning its a valid schedule time wise
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
	def addLab(self,schedule):
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
						if (not self.checkScheduleConflict(schedule)):
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
	def checkBadCredits(self,schedule, maxCredits):

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

		# if good schedule
		return False




	# Function checks if a schedule is a valid schedule or not
	# returns True schedule if it is valid, and False if not
	def verify(self,schedule, maxCredits):

		# checks if there is a lab in schedule
		if self.checkLab(schedule):
			# trys to add lab to schedule
			s = self.addLab(schedule)
			# if lab fit into schedule
			if s != False:
				# update schdule with lab
				schedule = s

			# lab did not fit into schedule
			else:
				# schedule does not work
				return False

		# check if there is a time conflict in schedule
		if self.checkScheduleConflict(schedule):
			# if there is a time conflict, invalid schedule
			return False

		# check if there are duplicate courses in schdule
		if self.checkSameCourse(schedule):
			# there were duplicates
			return False

		# check if there are too many or too little credits
		if self.checkBadCredits(schedule,maxCredits):
			# there was a bad amount of credits
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
			"numCourses": "Provide an integer for desired number of courses wanted, defaults to 4",
			"division": "Provide a department ID that the student is a part of, defaults to nothing",
			"index": "Provide an integer of last location in schedule list, if known, defaults to -1",
			"maxNumCredits": "Provide an integer for maximum number of credits wanted, defaults to 18",
			"limit":"Provide a max amount of schdedules wanted to be returned, defaults to 20"
		}
	)


	# function that takes parameters and returns JSON schedule
	def get(self):

		# checks if limit is empty
		lim = request.args.get("limit")
		# if not empty, it is int
		if lim != None:
			limit = int(lim)

		# if empty, default to 20
		else:
			limit = 20


		# checks if max credits are empty
		maxnc = request.args.get("maxNumCredits")
		# if not empty, it is int
		if maxnc != None:
			maxNumCredits = int(maxnc)

		# if empty, default to 18
		else:
			maxNumCredits = 18


		# checks if requirements are empty
		r = request.args.get("requiredCourses")
		# if not empty, create list
		if r != None:
			required = (r).split(',')

		# if empty, make empty list
		else:
			required = []

		# check if preferred are empty
		p = request.args.get("preferredCourses")
		# if not empty, create list
		if p != None:
			preferred = (p).split(',')

		# if empty, make empty list
		else:
			preferred = []

		# check if geneds are empty
		g = request.args.get("requiredGenEds")
		# if not empty create list
		if g != None:
			req_geneds = (g).split(',')

		# if empty, make empty list
		else:
			req_geneds = []

		# check if geneds are empty
		g = request.args.get("preferredGenEds")
		# if not empty create list
		if g != None:
			preferred_geneds = (g).split(',')

		# if empty, make empty list
		else:
			preferred_geneds = []

		# check if num of courses are empty
		n = request.args.get("numCourses")
		# if not empty, make it an int
		if n != None:
			num_courses = int(n)

		# if empty, default to 4 courses
		else:
			num_courses = 4

		# check if division is empty
		d = request.args.get("division")
		# if not empty, make int
		if d != None:
			division = int(d)

		# if empty, make None
		else:
			division = None

		# check if index is empty
		i = request.args.get("index")
		# if not empty, make int
		if i != None:
			index = int(i)

		# if empty, default to -1
		else:
			index = -1

		# go through requirements and make int instead of unicode
		new_r = []
		for x in required:
			new_r.append(int(x))

		required = new_r

		# go through preferred and make int instead of unicode
		new_p = []
		for x in preferred:
			new_p.append(int(x))

		preferred = new_p

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

		# add all sections of required courses
		temp = required
		lst = []

		for c in temp:
			classQuery = "SELECT section_id from Sections where course_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(classQuery % (str(c)))

			sects = []
			for (section_id) in cursor:
				sects.append(section_id[0])

			lst.append(sects)

			cursor.close()
			cnx.close()


		# add all sections of preferred courses
		temp = preferred

		for c in temp:
			classQuery = "SELECT section_id from Sections where course_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(classQuery % (str(c)))

			sects = []
			for (section_id) in cursor:
				sects.append(section_id[0])

			lst.append(sects)

			cursor.close()
			cnx.close()

		# Create all possible schedules from required and preferred.
		ps = list(itertools.product(*lst))

		possible_sections = []
		for c in ps:
			possible_sections.append(list(c))


		# all possible schedules
		all_combos = []


		# for each possible schedule with req/preferred
		for option in possible_sections:

			best = option
			required = best[:len(required)]
			preferred = best[len(required):]

			# if the best schedule is valid
			if self.verify(best, maxNumCredits) != False:

				best = self.verify(best, maxNumCredits)

				# if the best schedule has amount of sections wanted, add schedule
				if (len(best) == num_courses):
					all_combos += [best]

				# if more courses are needed
				elif (len(best) < num_courses):
					num_needed = num_courses - len(best)

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


					# if more is wanted after gen eds and best, look for recommendations
					if num_needed > 0:

						# check if they specified their division
						if division != None:

							# look for recommendations for division to fill schedule
							classes = []
							for i in range(num_needed):

								classQuery = "SELECT Sections.section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
								
								cnx = cnx_pool.get_connection()
								cursor = cnx.cursor()

								cursor.execute(classQuery % str(division))

								classes = []
								for (section_id) in cursor:
									classes.append(section_id[0])

								cursor.close()
								cnx.close()


							temp = []
							for x in classes:
								if num_needed > 0:
									temp.append(x)
									num_needed -= 1

							new_all = []
							for x in all_combos:

								new_all.append(list(x) + temp)

							all_combos += new_all


			# is best schedule is not valid for some reason
			else:
				best = required+preferred

				# remove courses from best until no conflict.
				while self.verify(best, maxNumCredits) == False:
					best = best[:-1]

				best = self.verify(best, maxNumCredits)

				if len(best) >= len(required):

					# if the best schedule has amount of sections wanted, add schedule
					if (len(best) == num_courses):
						all_combos += [best]

					# if more courses are needed
					elif (len(best) < num_courses):
						num_needed = num_courses - len(best)

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


						# if more is wanted after gen eds and best, look for recommendations
						if num_needed > 0:

							# check if they specified their division
							if division != None:

								# look for recommendations for division to fill schedule
								classes = []
								for i in range(num_needed):

									classQuery = "SELECT Sections.section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
									
									cnx = cnx_pool.get_connection()
									cursor = cnx.cursor()

									cursor.execute(classQuery % str(division))

									classes = []
									for (section_id) in cursor:
										classes.append(section_id[0])

									cursor.close()
									cnx.close()


								temp = []
								for x in classes:
									if num_needed > 0:
										temp.append(x)
										num_needed -= 1

								new_all = []
								for x in all_combos:

									new_all.append(list(x) + temp)

								all_combos += new_all



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
				while self.verify(current, maxNumCredits) == False and pos < len(all_combos)-1:
					pos += 1
					current = all_combos[pos]

				if pos < len(all_combos)-1:
					schedule = ScheduleCreationObject(self.verify(current, maxNumCredits),pos)
					schedules.append(schedule.__dict__)

		if schedules == []:
			s = ScheduleCreationObject([],pos)
			schedules.append(s.__dict__)

		return (schedules)


