

# Given a list of required sections and preferred sections, create a list of sections for schedules


# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config
import string
import time

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

		times = []
		for day in range(len(days)):

			d = str(days_dict[str(days[day])])

			st = time.strptime(str(start_time)+' '+d, '%H:%M %w')
			et = time.strptime(str(end_time)+' '+d, '%H:%M %w')
			times.append((st,et))

		cursor.close()
		cnx.close()

		sections.append((times,len(days)))

	for section1 in range(len(sections)):
		for section2 in range(section1,len(sections)):
			if section1 != section2:
				for time1 in range(sections[section1][-1]):
					for time2 in range(sections[section2][-1]):
						if checkTimeConflict(sections[section1][0][time1],sections[section2][0][time2]):
							return True

	return False




def createSchedule(required,preferred,division):

	pass



def main():
	print "*******************************"
	print(checkScheduleConflict([409,211]))
	print "*******************************"
	print(checkScheduleConflict([400,500,700]))
	print "*******************************"
	print(checkScheduleConflict([200,300,400,500]))
	print "*******************************"



if __name__ == '__main__':
	main()



