# Import the needed packages
import mysql.connector
import mysql.connector.pooling

from API import config
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


def relevance(words):

	keywords = []
	for word in words:
		keywords.append(word.lower())

	section_name = []
	section_short_title = []
	section_comments = []
	course_description = []
	course_name = []
	course_number = []
	course_ids = []
	sect_course_ids = []

	sectionQuery = "SELECT course_id, name, short_title, comments FROM Sections"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(sectionQuery)

	for (course_id, name, short_title, comments) in cursor:
		sect_course_ids.append(str(course_id))
		section_name.append(str(name))
		section_short_title.append(str(short_title))
		section_comments.append(str(comments))


	courseQuery = "SELECT course_id, description, name, number FROM Courses"

	cursor.execute(courseQuery)

	for (course_id, description, name, number) in cursor:
		course_ids.append(str(course_id))
		course_description.append(str(description))
		course_name.append(str(name))
		course_number.append(str(number))

	cursor.close()
	cnx.close()

	cids = {}
	for c in course_ids:
		cids[c] = 0

	for sect_idx in range(len(section_name)):
		all_str = section_name[sect_idx] + " " + section_comments[sect_idx] + " " + section_short_title[sect_idx]
		str_dict = tf(all_str)

		for word in keywords:
			if word in str_dict:
				cids[sect_course_ids[sect_idx]] += str_dict[word]
			elif word in all_str:
				cids[sect_course_ids[sect_idx]] += 1


	for course_idx in range(len(course_name)):
		all_str = course_description[course_idx] + " " + course_name[course_idx] + " " + course_number[course_idx]
		str_dict = tf(all_str)

		for word in keywords:
			if word in str_dict:
				cids[course_ids[course_idx]] += str_dict[word]
			elif word in all_str:
				cids[course_ids[course_idx]] += 1


	final = []
	for cid in cids:
		if cids[cid] > 0:
			final.append((int(cid),cids[cid]))

	return final












