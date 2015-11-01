

# Given a list of required sections and preferred sections, create a list of sections for schedules


# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config
import string

from flask import Flask, request
from flask.ext.restplus import Api, Resource


# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)




# sectionQuery = "SELECT name, short_title, comments, course_id FROM Sections WHERE section_id = %s"

# cnx = cnx_pool.get_connection()
# cursor = cnx.cursor()

# cursor.execute(sectionQuery % str(section_id))

# for (name, short_title, comments, course_id) in cursor:
# 	section_name = name
# 	section_short_title = short_title
# 	section_comments = comments
# 	section_course_id = course_id

# cursor.close()
# cnx.close()


def betweenTimes(original,check):
	original_start = original[0]
	original_end = original[1]

	if check[0] == original_start[0]:
		check_time = check[1:]
		check_hour_minute = check.split(':')
		check_hour = check_hour_minute[0]
		check_minute = check_hour_minute[1]

		original_start_time = original_start[1:]
		original_start_hour_minute = original_start.split(':')
		original_start_hour = original_start_hour_minute[0]
		original_start_minute = original_start_hour_minute[1]

		original_end_time = original_end[1:]
		original_end_hour_minute = original_end.split(':')
		original_end_hour = original_end_hour_minute[0]
		original_end_minute = original_end_hour_minute[1]

		if check_hour >= original_start_hour and check_hour <= original_end_hour:
			return True
		return False


def checkTimeConflict(one,two):
	start_one = one[0]
	start_two = two[0]
	end_one = one[1]
	end_two = two[1]

	if betweenTimes((start_one,start_two),end_one):
		return True
	if betweenTimes((start_one,start_two),end_two):
		return True

	return False


def checkScheduleConflict(section_ids):

	startQuery = "SELECT start_time FROM SectionMeetings GROUP BY start_time"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(startQuery)


	s_times = []

	for (start_time) in cursor:
		s_times.append(str(start_time[0]))

	endQuery = "SELECT end_time FROM SectionMeetings GROUP BY end_time"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(endQuery)

	e_times = []

	for (end_time) in cursor:
		e_times.append(str(end_time[0]))

	cursor.close()
	cnx.close()



	start_times = []

	for day in ['M','T','W','H','F']:
		for time in s_times:
			start_times.append(day+time)


	end_times = []

	for day in ['M','T','W','H','F']:
		for time in e_times:
			end_times.append(day+time)



	sections = []

	for section_id in section_ids:

		sectionQuery = "SELECT start_time, end_time, days FROM SectionMeetings WHERE section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(sectionQuery % str(section_id))

		for (start_time, end_time, days) in cursor:
			start_time = start_time
			end_time = end_time
			days = days


		section_start_times = []
		section_end_times = []
		for day in range(len(days)):
			section_start_times.append(str(days[day])+str(start_time))
			section_end_times.append(str(days[day])+str(end_time))


		cursor.close()
		cnx.close()

		sections.append((section_start_times,section_end_times,len(days)))

		

	# for section1 in range(len(sections)-1):
	# 	for section2 in range(section1,len(sections)-1):
	# 		if section1 != section2:

	# 			for time1 in range(sections[section1][-1]):
	# 				for time2 in range(sections[section2][-1]):

	# 					if checkTimeConflict(sections[section1][time1],sections[section2][time2]):
	# 						return True


	return False




def createSchedule(required,preferred,division):

	pass



def main():
	print(checkScheduleConflict([400,500,700]))





if __name__ == '__main__':
	main()



