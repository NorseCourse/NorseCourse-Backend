# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask, request
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a section object should contain
class SectionJSON(object):
	def __init__(self, term = None, name = None, short_title= None, min_credits=None, max_credits=None, comments=None, seven_weeks=None, section_id = None, course_id = None,faculty=None):
		self.term = term
		self.name = name
		self.shortTitle = short_title
		self.minCredits = min_credits
		self.maxCredits = max_credits
		self.comments = comments
		self.sevenWeeks = seven_weeks
		self.id = section_id
		self.courseId = course_id
		self.faculty = faculty


# What a requirement object should contain
class FacultyJSON(object):
	def __init__(self, first_initial = None, last_name = None):
		self.first_initial = first_initial
		self.last_name = last_name


app = Flask(__name__)
sectionApp = Api(app)
sectionAPI = sectionApp.namespace('api', 'Root namespace for NorseCourse APIs')


@sectionAPI.route("/sections")
class Section(Resource):

	def getFaculty(self, section_id):
		requirementQuery = "SELECT first_initial, last_name FROM Faculty, FacultyAssignments WHERE Faculty.faculty_id = FacultyAssignments.faculty_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(requirementQuery % str(section_id))

		profs = []
		for (first_initial, last_name) in cursor:
			faculty = FacultyJSON(first_initial, last_name)
			profs.append(faculty.__dict__)

		cursor.close()
		cnx.close()

		return profs


	@sectionApp.doc(
		params = {
			"course": "Provide a comma separated list of course IDs"
		}
	)
	def get(self):
		sectionQuery = "SELECT term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id FROM Sections"
		
		course = request.args.get("course")
		id_list = []
		if course != None:
			id_list = course.split(",")
			id_list = map(str, id_list)

			sectionQuery += " WHERE course_id = %s"
			for i in range(len(id_list) - 1):
				sectionQuery += " OR course_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		if len(id_list) > 0:
			cursor.execute(sectionQuery, tuple(id_list))
		else:
			cursor.execute(sectionQuery)

		sections = []
		for (term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id) in cursor:
			prof = self.getFaculty(section_id)
			sect = SectionJSON(term, name,short_title,min_credits,max_credits,comments,seven_weeks,section_id,course_id,prof)
			sections.append(sect.__dict__)

		cursor.close()
		cnx.close()

		return sections


if __name__ == "__main__":
	app.debug = True
	app.run()














