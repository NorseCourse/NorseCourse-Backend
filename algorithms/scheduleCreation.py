

# Given a list of required sections and preferred sections, create a list of sections for schedules


# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config
import string
import time
import itertools

from flask import Flask, request
from flask.ext.restplus import Api, Resource


# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)


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
	pass

def createSchedule(required,preferred,geneds,num_courses,division = None):



	if checkScheduleConflict(required) or len(required) > num_courses:
		print "Required courses conflict, or too many required courses, can not make a schedule"
		return None

	best = required+preferred

	if (len(best) == num_courses) and (not checkScheduleConflict(best)):
		return best

	if (len(best) < num_courses) and (not checkScheduleConflict(best)):
		num_needed = num_courses - len(best)
		# best works, but more courses wanted, add something from gen eds or divisions
		if len(geneds) > 0:
			# look for geneds that fit into schedule

			possible_gened_classes = []
			for gened in range(len(geneds)):

				classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				possible_gened_classes.append(classes)

				cursor.close()
				cnx.close()
				
			for ge in possible_gened_classes:
				added = False
				for sect in ge:
					sect = sect[0]
					if not added:
						if num_needed > 0:
							best.append(sect)

							if (not checkScheduleConflict(best)):
								added = True
								num_needed -= 1
							else:
								best = best[:-1]
						else:
							return best



		if division != None:
			# look for recommendations for division to fill schedule
			for i in range(num_needed):

				classQuery = "SELECT section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
				
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str(division))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				cursor.close()
				cnx.close()


			for sect in classes:
				if num_needed > 0:
					sect = sect[0]
					best.append(sect)
					if (not checkScheduleConflict(best)):
						num_needed -= 1
					else:
						best = best[:-1]
				else:
					return best
			return best
		return best


	# len(best) > num_courses
	if (not checkScheduleConflict(best)):
		# too many total courses, need to remove some preferred courses
		num_removed = len(best) - num_courses
		return best+preferred[:-(num_removed)]




	# best conflicts time, find non conflicting time

	# remove random preferred and check for something that works
	# once found a schedule with most courses that work call it best
	# worst case is down to required, because that should not conflict

	while (checkScheduleConflict(best)):
		best = required+preferred[:-1]

	num_needed = num_courses - len(best)

	if num_needed > 0:

		if len(geneds) > 0:
			# look for geneds that fit into schedule

			possible_gened_classes = []
			for gened in range(len(geneds)):

				classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				possible_gened_classes.append(classes)

				cursor.close()
				cnx.close()
				
			for ge in possible_gened_classes:
				added = False
				for sect in ge:
					sect = sect[0]
					if not added:
						if num_needed > 0:
							best.append(sect)

							if (not checkScheduleConflict(best)):
								added = True
								num_needed -= 1
							else:
								best = best[:-1]
						else:
							return best



		if division != None:
			# look for recommendations for division to fill schedule
			for i in range(num_needed):

				classQuery = "SELECT section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
				
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str(division))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				cursor.close()
				cnx.close()


			for sect in classes:
				if num_needed > 0:
					sect = sect[0]
					best.append(sect)
					if (not checkScheduleConflict(best)):
						num_needed -= 1
					else:
						best = best[:-1]
				else:
					return best
			return best
		return best



	elif num_needed == 0 and (not checkScheduleConflict(best)):
		return best



def createAllSchedules(required,preferred,geneds,num_courses,division = None):

	master = []


	if checkScheduleConflict(required) or len(required) > num_courses:
		print "Required courses conflict, or too many required courses, can not make a schedule"
		master.append(None)
		return master

	best = required+preferred

	if (len(best) == num_courses) and (not checkScheduleConflict(best)):
		master.append(best)
		return master

	if (len(best) < num_courses) and (not checkScheduleConflict(best)):
		num_needed = num_courses - len(best)
		# best works, but more courses wanted, add something from gen eds or divisions
		if len(geneds) > 0:
			# look for geneds that fit into schedule

			possible_gened_classes = []
			for gened in range(len(geneds)):

				classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				possible_gened_classes.append(classes)

				cursor.close()
				cnx.close()
				

			prev = best
			possible = []
			for ge in possible_gened_classes:
				# for HE, NW, etc

				if len(possible) > 0:
					for x in possible:
						
						best = x
						added = False
						for sect in ge:
							# section that is gened

							sect = sect[0]
							if not added:
								if num_needed > 0:
									best.append(sect)

									if (not checkScheduleConflict(best)):
										added = True
										num_needed -= 1
									else:
										best = best[:-1]
							else:
								if best not in master:
									if num_needed == 0:
										master.append(best)
									else:
										possible.append(best)
									best = best[:-1]
									added = False
									num_needed += 1

				else:

					added = False
					for sect in ge:
						# section that is gened

						sect = sect[0]
						if not added:
							if num_needed > 0:
								best.append(sect)

								if (not checkScheduleConflict(best)):
									added = True
									num_needed -= 1
								else:
									best = best[:-1]
						else:
							if best not in master:
								if num_needed == 0:
									master.append(best)
								else:
									possible.append(best)
								best = best[:-1]
								added = False
								num_needed += 1




		if division != None:
			# look for recommendations for division to fill schedule
			classes = []
			for i in range(num_needed):

				classQuery = "SELECT section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
				
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str(division))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				cursor.close()
				cnx.close()


			full = False
			prev = best
			prev_needed = num_needed

			for sect in classes:
				if num_needed > 0:
					sect = sect[0]
					best.append(sect)
					if (not checkScheduleConflict(best)):
						num_needed -= 1
					else:
						best = best[:-1]
				else:
					master.append(best)
					best = prev
					num_needed = prev_needed
					full = True
			if not full:
				master.append(best)


	# len(best) > num_courses
	if len(best) > num_courses and (not checkScheduleConflict(best)):
		# too many total courses, need to remove some preferred courses
		num_removed = len(best) - num_courses
		master.append(best+preferred[:-(num_removed)])


	# best conflicts time, find non conflicting time

	# remove random preferred and check for something that works
	# once found a schedule with most courses that work call it best
	# worst case is down to required, because that should not conflict

	while (checkScheduleConflict(best)):
		best = required+preferred[:-1]

	num_needed = num_courses - len(best)

	if num_needed > 0:

		if len(geneds) > 0:
			# look for geneds that fit into schedule

			possible_gened_classes = []
			for gened in range(len(geneds)):

				classQuery = "SELECT section_id from GenEdFulfillments, GenEds where GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s"

				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str("'"+geneds[gened]+"'"))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				possible_gened_classes.append(classes)

				cursor.close()
				cnx.close()
				
			prev = best
			possible = []
			for ge in possible_gened_classes:
				# for HE, NW, etc

				if len(possible) > 0:
					for x in possible:
						
						best = x
						added = False
						for sect in ge:
							# section that is gened

							sect = sect[0]
							if not added:
								if num_needed > 0:
									best.append(sect)

									if (not checkScheduleConflict(best)):
										added = True
										num_needed -= 1
									else:
										best = best[:-1]
							else:
								if best not in master:
									if num_needed == 0:
										master.append(best)
									else:
										possible.append(best)
									best = best[:-1]
									added = False
									num_needed += 1

				else:

					added = False
					for sect in ge:
						# section that is gened

						sect = sect[0]
						if not added:
							if num_needed > 0:
								best.append(sect)

								if (not checkScheduleConflict(best)):
									added = True
									num_needed -= 1
								else:
									best = best[:-1]
						else:
							if best not in master:
								if num_needed == 0:
									master.append(best)
								else:
									possible.append(best)
								best = best[:-1]
								added = False
								num_needed += 1

		if division != None:
			# look for recommendations for division to fill schedule
			classes = []
			for i in range(num_needed):

				classQuery = "SELECT section_id from Sections, Courses, Recommendations where Courses.course_id = Recommendations.course_id and Courses.course_id = Sections.course_id and Recommendations.division_id = %s"
				
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				cursor.execute(classQuery % str(division))

				classes = []
				for (section_id) in cursor:
					classes.append(section_id)

				cursor.close()
				cnx.close()

			full = False
			prev = best
			prev_needed = num_needed

			for sect in classes:
				if num_needed > 0:
					sect = sect[0]
					best.append(sect)
					if (not checkScheduleConflict(best)):
						num_needed -= 1
					else:
						best = best[:-1]
				else:
					master.append(best)
					best = prev
					num_needed = prev_needed
					full = True
			if not full:
				master.append(best)

	return master



def verify(schedule):
	if checkScheduleConflict(schedule):
		return False

	if checkSameCourse(schedule):
		return False

	return True

	# check if a lab is needed, if so add it





def allCombos(required,preferred,geneds,num_courses,division = None):

	master = []


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


				combo = [best]
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


				combo = [best]
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



	final = []
	for schedule in all_combos:
		if verify(schedule):
			final.append(schedule)

	return final



def main():
	# print "*******************************"
	# print(checkScheduleConflict([409,211]))
	# print "*******************************"
	# print(checkScheduleConflict([400,500,700]))
	# print "*******************************"
	# print(checkScheduleConflict([200,300,400,500]))
	# print "*******************************"
	# print(checkScheduleConflict([211,213,223,227]))
	# print "*******************************"
	# print "*******************************"
	# print "*******************************"
	# print
	# print
	# print createSchedule([211,227],[],['HEPT',"NWL"],4,4)
	# print
	# print



	# print "*******************************"

	# print
	# print
	# print
	# m = createAllSchedules([211,227,213],[],['REL'],4,4)
	# print
	# print

	# for x in m:
	# 	print x
	# print
	# print

	# print "*******************************"

	# print
	# print
	# print
	# m = createAllSchedules([211],[227],['REL',"HEPT"],4,4)
	# print
	# print

	# for x in m:
	# 	print x
	# print
	# print



	# print "*******************************"

	# print
	# print
	# print
	# m = createAllSchedules([],[],['QUANT',"HB","REL","NWL"],4,4)
	# print
	# print

	# for x in m:
	# 	print x
	# print
	# print

	print
	print
	x = allCombos([211],[],['HE',"NWL"],3,4)
	for i in x:
		print i
	print
	print





if __name__ == '__main__':
	main()



