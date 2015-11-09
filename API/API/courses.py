from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  NorseCourseObjects import CourseObject, RequirementObject

def getRequirements(course_id):
	requirementQuery = "SELECT req_type, details FROM Requirements WHERE course_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(requirementQuery % str(course_id))

	requirements = []
	for (req_type, details) in cursor:
		requirement = RequirementObject(req_type, course_id, details)
		requirements.append(requirement.__dict__)

	cursor.close()
	cnx.close()

	if requirements:
		return requirements
	else:
		return None


def getRecommendations(course_id):
	recommendationQuery = "SELECT division_id, COUNT(division_id) AS count FROM Recommendations WHERE course_id = %s GROUP BY(division_id)"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(recommendationQuery % str(course_id))

	recommendations = {}
	for (division_id, count) in cursor:
		recommendations[str(division_id)] = count

	cursor.close()
	cnx.close()

	if recommendations:
		return recommendations
	else:
		return None


coursesDict = {
	"courseId": "course_id",
	"description": "description",
	"sameAs": "same_as",
	"name": "name",
	"departmentId": "department_id"
	}


@API.route("/courses", endpoint = "courses")
class Courses(Resource):
	@NorseCourse.doc(
		params = {
			"departments": "Provide a comma separated list of department IDs",
			"keywords": "Provide a comma separated list of keywords",
			"genEds": "Provide a comma separated list of Gen Ed IDs",
			"fields": "Provide a comma separated list of fields you would like back"
		}
	)
	def get(self):
		courseQuery = "SELECT course_id, description, same_as, name, department_id FROM Courses GROUP BY (name)"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		###
		# SOME MORE CODE TO DEAL WITH ABOVE PARAMS
		# ALTER THE QUERY
		###

		cursor.execute(courseQuery)

		courses = []
		for (course_id, description, same_as, name, department_id) in cursor:
			requirements = getRequirements(course_id)
			recommendations = getRecommendations(course_id)

			if same_as == "nan":
				course = CourseObject(course_id, description, None, name, department_id, None, requirements, recommendations)
			else:
				course = CourseObject(course_id, description, same_as, name, department_id, None, requirements, recommendations)

			courses.append(course.__dict__)

		cursor.close()
		cnx.close()

		return courses


@API.route("/courses/<courseId>", endpoint = "courses/")
class Courses(Resource):
	@NorseCourse.doc(
		params = {
			"courseId": "Provide a courseId to get all of the information related to that coures",
			"fields": "Provide a comma separated list of fields you would like back"
		}
	)
	def get(self, courseId):
		# Get the URL params
		fields = request.args.get("fields")
		if fields == None:
			fields = ["courseId", "description", "sameAs", "name", "departmentId", "requirements", "recommendations", "relevance"]
		else:
			fields = fields.split(",")

		# Gather the terms for the course query.
		coursesTerms = []
		for field in fields:
			if field in coursesDict:
				coursesTerms.append(coursesDict[field])

		# Get a connecgtion and open up a cursor
		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		# Te,p object for storing the course info as the fields can be passed in in any order.
		tempObj = {
			"course_id": None,
			"description": None,
			"same_as": None,
			"name": None,
			"department_id": None
			}

		# Execute if there is anything needed from the course table
		if coursesTerms:
			# Build the course query
			courseQuery = "SELECT "
			termsLen = len(coursesTerms)
			addComma = termsLen - 1

			for i in range(termsLen):
				courseQuery += coursesTerms[i]
				if i < addComma:
					courseQuery += ", "
			courseQuery += " FROM Courses WHERE course_id = %s"

			# Execute the query
			cursor.execute(courseQuery % str(courseId))

			# Populate the temp object
			for result in cursor:
				print(result)
				for item, ct in zip(result, coursesTerms):
					tempObj[ct] = item
			if tempObj["same_as"] == "nan":
				tempObj["same_as"] = None

		# Get the relevance if asked for
		relevance = None
		if "relevance" in fields:
			pass

		# Get the requirements if asked for
		requirements = None
		if "requirements" in fields:
			requirements = getRequirements(courseId)

		# Get the recommendations is asked for
		recommendations = None
		if "recommendations" in fields:
			recommendations = getRecommendations(courseId)

		# Close the connection and cursor		
		cursor.close()
		cnx.close()

		# Build the object to be returned
		returnCourse = CourseObject(tempObj["course_id"], tempObj["description"], tempObj["same_as"], tempObj["name"], tempObj["department_id"], relevance, requirements, recommendations)
		return returnCourse.__dict__