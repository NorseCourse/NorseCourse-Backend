# Import the needed packages
# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask, request
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a course object should contain
class CourseJSON(object):
	def __init__(self, course_id = None, description = None, same_as = None, number = None, department_id = None, relevance = None, requirements = None, recommendations = None):
		self.course_id = course_id
		self.description = description
		self.same_as = same_as
		self.number = number
		self.department_id = department_id
		self.relevance = relevance	#Some number based on a keyword search
		self.requirements = requirements	#This will be a requirements object
		self.recommendations = recommendations	#This will be a relevance object

# What a requirement object should contain
class RequirementJSON(object):
	def __init__(self, req_type = None, course_id = None, details = None):
		self.req_type = req_type
		self.course_id = course_id
		self.details = details

# What a recommendation object should contain
#A LITTLE UNSURE WHAT THIS IS SUPPOSED TO HAVE BASED IN DOCS????
# class RecommendationJSON(object):
# 	def __init__(self, gen_ed_id = None, name = None, abbreviation = None, also_fulfills = None):
# 		self.gen_ed_id = gen_ed_id
# 		self.name = name
# 		self.abbreviation = abbreviation
# 		self.also_fulfills = also_fulfills

app = Flask(__name__)
courseApp = Api(app)
courseAPI = courseApp.namespace('api', 'Root namespace for NorseCourse APIs')