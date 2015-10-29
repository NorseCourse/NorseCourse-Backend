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


def tf(st):
	st = st.split()

	doc_dict = {}
	for word in st:
		word = word.lower()
		if len(word.split('-')) > 1:
			words = word.split('-')
			for word in words:
				if word in doc_dict:
					doc_dict[word] = doc_dict[word] + 1
				else:
					doc_dict[word] = 1
		else:
			if word in doc_dict:
				doc_dict[word] = doc_dict[word] + 1
			else:
				doc_dict[word] = 1
	
	return doc_dict




def relevance(word,section_id):

	word = word.lower()

	sectionQuery = "SELECT term, name, short_title, comments, course_id FROM Sections WHERE section_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(sectionQuery % str(section_id))

	for (term, name, short_title, comments, course_id) in cursor:
		section_term = term
		section_name = name
		section_short_title = short_title
		section_comments = comments
		section_course_id = course_id

	cursor.close()
	cnx.close()



	courseQuery = "SELECT description, same_as, name, number, department_id FROM Courses WHERE course_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(courseQuery % str(section_course_id))

	for (description, same_as, name, number, department_id) in cursor:
		course_description = description
		course_same_as = same_as
		course_name = name
		course_number = number
		course_dept_id = department_id

	cursor.close()
	cnx.close()


	deptQuery = "SELECT abbreviation, name, division_id FROM Departments WHERE department_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(deptQuery % str(course_dept_id))

	for (abbreviation, name, division_id) in cursor:
		dept_abb = abbreviation
		dept_name = name
		dept_div_id = division_id

	cursor.close()
	cnx.close()


	divQuery = "SELECT name FROM Divisions WHERE division_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(divQuery % str(dept_div_id))

	for (name) in cursor:
		div_name = name

	cursor.close()
	cnx.close()




	facultyQuery = "SELECT faculty_id FROM FacultyAssignments WHERE section_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(facultyQuery % str(section_id))

	for (faculty_id) in cursor:
		faculty_id = faculty_id

	cursor.close()
	cnx.close()



	faculty2Query = "SELECT last_name FROM Faculty WHERE faculty_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(faculty2Query % str(faculty_id)[:-2][1:])

	for (last_name) in cursor:
		faculty_last_name = last_name

	cursor.close()
	cnx.close()



	sectionMeetingQuery = "SELECT room_id, days FROM SectionMeetings WHERE section_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(sectionMeetingQuery % str(section_id))

	for (room_id,days) in cursor:
		room_id = room_id
		section_days = days

	cursor.close()
	cnx.close()


	roomQuery = "SELECT building_id, number FROM Rooms WHERE room_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(roomQuery % str(room_id))

	for (building_id,number) in cursor:
		building_id = building_id
		room_number = number

	cursor.close()
	cnx.close()



	buildingQuery = "SELECT name, abbreviation FROM Buildings WHERE building_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(buildingQuery % str(building_id))

	for (name,abbreviation) in cursor:
		building_name = name
		building_abb = abbreviation

	cursor.close()
	cnx.close()



	gen_ed_id = None

	geFQuery = "SELECT gen_ed_id, comments FROM GenEdFulfillments WHERE section_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(geFQuery % str(section_id))

	for (gen_ed_id, comments) in cursor:
		gen_ed_id = gen_ed_id
		gen_ed_comments = comments

	cursor.close()
	cnx.close()


	if gen_ed_id != None:

		geQuery = "SELECT name, abbreviation, also_fulfills FROM GenEds WHERE gen_ed_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(geQuery % str(gen_ed_id))

		for (name, abbreviation, also_fulfills) in cursor:
			gen_ed_name = name
			gen_ed_abb = abbreviation
			gen_ed_also = also_fulfills

		cursor.close()
		cnx.close()


	if gen_ed_id != None:
		lst_of_details = [section_term, section_name,section_short_title,section_comments,course_description,course_same_as,course_name,course_number,dept_abb,dept_name,div_name,faculty_last_name,section_days,building_name,building_abb,gen_ed_comments,gen_ed_name,gen_ed_abb,gen_ed_also]
	else:
		lst_of_details = [section_term, section_name,section_short_title,section_comments,course_description,course_same_as,course_name,course_number,dept_abb,dept_name,div_name,faculty_last_name,section_days,building_name,building_abb]
	

	string_of_all = ""

	for thing in lst_of_details:
		if type(thing) == tuple:
			thing = thing[0]
		string_of_all += str(thing) + " "

	string_dict = tf(string_of_all)

	if word in string_dict:
		return string_dict[word]
	if word in string_of_all:
		return 1
	return 0




print(relevance("oboe",100))
print(relevance("oboe",101))















