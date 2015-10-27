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
	def __init__(self, course_id = None, description = None, same_as = None, name = None, department_id = None, relevance = None, requirements = None, recommendations = None):
		self.course_id = course_id
		self.description = description
		self.same_as = same_as
		self.name = name
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

@courseAPI.route("/courses")
class Course(Resource):
	def getRequirements(self, course_id):
		requirementQuery = "SELECT req_type, details FROM Requirements WHERE course_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(requirementQuery % str(course_id))

		requirements = []
		for (req_type, details) in cursor:
			requirement = RequirementJSON(req_type, course_id, details)
			requirements.append(requirement.__dict__)

		cursor.close()
		cnx.close()

		if requirements:
			return requirements
		else:
			return None


	@courseApp.doc(
		params = {
			"departments": "Provide a comma separated list of department ids",
			"keywords": "Provide a comma separated list of keywords",
			"genEds": "Provide a comma separated list of gen ed ids",
			"fields": "Provide a comma separated list of fields"
		}
	)
	def get(self):
		courseQuery = "SELECT course_id, description, same_as, name, department_id FROM Courses GROUP BY (name);"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		###
		# SOME MORE CODE
		###

		cursor.execute(courseQuery)

		courses = []
		for (course_id, description, same_as, name, department_id) in cursor:
			requirements = self.getRequirements(course_id)
			if same_as == "nan":
				course = CourseJSON(course_id, description, None, name, department_id, None, requirements, None)
			else:
				course = CourseJSON(course_id, description, same_as, name, department_id, None, requirements, None)
			courses.append(course.__dict__)

		cursor.close()
		cnx.close()

		return courses


if __name__ == "__main__":
	app.debug = True
	app.run()













