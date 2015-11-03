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

	sectionQuery = "SELECT name, short_title, comments, course_id FROM Sections WHERE section_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(sectionQuery % str(section_id))

	for (name, short_title, comments, course_id) in cursor:
		section_name = name
		section_short_title = short_title
		section_comments = comments
		section_course_id = course_id


	courseQuery = "SELECT description, name, number FROM Courses WHERE course_id = %s"

	cursor.execute(courseQuery % str(section_course_id))

	for (description, name, number) in cursor:
		course_description = description
		course_name = name
		course_number = number

	cursor.close()
	cnx.close()



	lst_of_details = [section_name,section_short_title,section_comments,course_description,course_name,course_number]
	

	string_of_all = ""

	for thing in lst_of_details:
		if type(thing) == tuple:
			thing = thing[0]
		string_of_all += str(thing) + " "

	string_dict = tf(string_of_all)


	if word in string_dict:
		print(section_name)
		return string_dict[word]
	if word in string_of_all:
		print(section_name)
		return 1
	
	return 0

