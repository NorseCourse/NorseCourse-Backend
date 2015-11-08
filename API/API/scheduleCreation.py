

# Given a list of required sections and preferred sections, create a list of sections for schedules


# Import the needed packages
# import mysql.connector
# import mysql.connector.pooling

import config
import string
import time
import itertools
import ast
import datetime
import random

from API import NorseCourse, API, cnx_pool
from flask import Flask, request
from flask.ext.restplus import Api, Resource
from  NorseCourseObjects import ScheduleCreationObject


@API.route("/scheduleCreation")
class ScheduleCreation(Resource):

	@NorseCourse.doc(
		params = {
			"required": "Provide a comma separated list of section IDs that are required in schedule",
			"preferred": "Provide a comma separated list of section IDs that are preferred in schedule",
			"geneds": "Provide a comma separated list of Gen Ed abbreviation strings wanted",
			"numcourses": "Provide an integer for desired number of courses wanted",
			"division": "Provide a department ID that the student is a part of",
			"index": "Provide an integer of last location in schedule list, if known"
		}
	)



	# Grab the correct set of properties to use and create a connection pool
	db_properties = config.db_pool_config
	cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)


	global_dict = {}

	def betweenTimes(original,check):
		original_start = original[0]
		original_end = original[1]

		if original_start.tm_wday == check.tm_wday:
			if original_start <= check <= original_end:
				return True
		return False


	def checkTimeConflict(one,two):

		start_one = one[0]
		end_one = one[1]

		start_two = two[0]
		end_two = two[1]

		if betweenTimes((start_one,end_one),start_two):
			return True
		if betweenTimes((start_one,end_one),end_two):
			return True

		return False


	def checkScheduleConflict(section_ids):

		sections = []
		days_dict = {'M':'2','T':'3','W':'4','R':'5','F':'6'}

		for section_id in section_ids:

			if section_id in global_dict:
				sections.append(global_dict[section_id])
			else:

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

				if start_time == "nan" or end_time == "nan" or days == "nan":
					return False

				times = []
				for day in range(len(days)):

					d = str(days_dict[str(days[day])])

					st = time.strptime(str(start_time)+' '+d, '%H:%M %w')
					et = time.strptime(str(end_time)+' '+d, '%H:%M %w')
					times.append((st,et))


				sections.append((times,len(days)))

				global_dict[section_id] = (times,len(days))


		for section1 in range(len(sections)):
			for section2 in range(section1,len(sections)):
				if section1 != section2:
					for time1 in range(sections[section1][-1]):
						for time2 in range(sections[section2][-1]):
							if checkTimeConflict(sections[section1][0][time1],sections[section2][0][time2]):
								return True

		return False


	def checkSameCourse(schedule):
		course_ids = []
		for section_id in schedule:

			sectionQuery = "SELECT course_id FROM Sections WHERE section_id = %s"

			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			cursor.execute(sectionQuery % str(section_id))

			for (course_id) in cursor:
				if course_id not in course_ids:
					course_ids.append(course_id)

			cursor.close()
			cnx.close()

		if len(course_ids) != len(schedule):
			return True
		return False


	def checkLab(schedule):
		labs = []
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

			if labs != None:
				return True
		return False




	def addLab(schedule):
		schedule = list(schedule)
		labs = []
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

			if labs != None:
				added = False
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

						if (not checkScheduleConflict(schedule)):
							added = True
						else:
							schedule = schedule[:-1]
				if added == False:
					return False

		return schedule


	def verify(schedule):

		if checkLab(schedule):
			s = addLab(schedule)
			if s != False:
				schedule = s

		if checkScheduleConflict(schedule):
			return False

		if checkSameCourse(schedule):
			return False

		return schedule


	def get(self):

		required = request.args.get("required")
		preferred = request.args.get("preferred")
		geneds = request.args.get("geneds")
		num_courses = request.args.get("numcourses")
		division = request.args.get("division")
		index = request.args.get("index")

		if checkScheduleConflict(required) or len(required) > num_courses:
			print "Required courses conflict, or too many required courses, can not make a schedule"
			return None

		best = required+preferred

		if not checkScheduleConflict(best):

			if (len(best) == num_courses):
				return best

			if (len(best) < num_courses):
				num_needed = num_courses - len(best)
				
				if len(geneds) > 0:

					possible_gened_classes = {}
					for gened in range(len(geneds)):

						classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

						cnx = cnx_pool.get_connection()
						cursor = cnx.cursor()

						cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

						classes = []
						for (section_id) in cursor:
							classes.append(section_id[0])

						possible_gened_classes[geneds[gened]] = classes

						cursor.close()
						cnx.close()

					combo = []

					for b in best:
						combo.append([b])

					for x in possible_gened_classes:
						if num_needed > 0:
							combo.append(possible_gened_classes[x])
							num_needed -= 1


					all_combos = list(itertools.product(*combo))

				else:
					all_combos = [best]


				if num_needed > 0:

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


						if len(all_combos) > 1:
							temp = []
							for x in classes:
								if num_needed > 0:
									temp.append(x)
									num_needed -= 1

							new_all = []
							for x in all_combos:

								new_all.append(list(x) + temp)

							all_combos = new_all


			if (len(best) > num_courses):
				# too many total courses, need to remove some preferred courses
				num_removed = len(best) - num_courses
				best = (best+preferred[:-(num_removed)])


		# is a time conflict
		else:
			while checkScheduleConflict(best):
				best = best[:-1]


			###########################
			# same as above in if
			##########################
			if (len(best) == num_courses):
				return best

			if (len(best) < num_courses):
				num_needed = num_courses - len(best)
				
				if len(geneds) > 0:

					possible_gened_classes = {}
					for gened in range(len(geneds)):

						classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

						cnx = cnx_pool.get_connection()
						cursor = cnx.cursor()

						cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

						classes = []
						for (section_id) in cursor:
							classes.append(section_id[0])

						possible_gened_classes[geneds[gened]] = classes

						cursor.close()
						cnx.close()


					combo = []

					for b in best:
						combo.append([b])

					for x in possible_gened_classes:
						if num_needed > 0:
							combo.append(possible_gened_classes[x])
							num_needed -= 1

					all_combos = list(itertools.product(*combo))

				else:
					all_combos = [best]


				if num_needed > 0:

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


						if len(all_combos) > 1:
							temp = []
							for x in classes:
								if num_needed > 0:
									temp.append(x)
									num_needed -= 1

							new_all = []
							for x in all_combos:

								new_all.append(list(x) + temp)

							all_combos = new_all


			if (len(best) > num_courses):
				# too many total courses, need to remove some preferred courses
				num_removed = len(best) - num_courses
				best = (best+preferred[:-(num_removed)])


		random.seed(0)
		random.shuffle(all_combos)

		if index == None:
			pos = 0
			current = all_combos[pos]
			while verify(current) == False:
				pos += 1
				current = all_combos[pos]

			schedule = ScheduleCreationObject(verify(current),pos)
			return schedule
		else:
			pos = index+1
			current = all_combos[pos]
			while verify(current) ==  False:
				pos += 1
				current = all_combos[pos]

			schedule = ScheduleCreationObject(verify(current),pos)
			return schedule


