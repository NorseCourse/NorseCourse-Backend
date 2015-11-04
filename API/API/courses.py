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


@API.route("/courses", endpoint = "courses")
class Courses(Resource):
	# def getRequirements(self, course_id):
	# 	requirementQuery = "SELECT req_type, details FROM Requirements WHERE course_id = %s"

	# 	cnx = cnx_pool.get_connection()
	# 	cursor = cnx.cursor()

	# 	cursor.execute(requirementQuery % str(course_id))

	# 	requirements = []
	# 	for (req_type, details) in cursor:
	# 		requirement = RequirementObject(req_type, course_id, details)
	# 		requirements.append(requirement.__dict__)

	# 	cursor.close()
	# 	cnx.close()

	# 	if requirements:
	# 		return requirements
	# 	else:
	# 		return None

	# def getRecommendations(self, course_id):
	# 	recommendationQuery = "SELECT division_id, COUNT(division_id) AS count FROM Recommendations WHERE course_id = %s GROUP BY(division_id)"

	# 	cnx = cnx_pool.get_connection()
	# 	cursor = cnx.cursor()

	# 	cursor.execute(recommendationQuery % str(course_id))

	# 	recommendations = {}
	# 	for (division_id, count) in cursor:
	# 		recommendations[str(division_id)] = count

	# 	cursor.close()
	# 	cnx.close()

	# 	if recommendations:
	# 		return recommendations
	# 	else:
	# 		return None


	@NorseCourse.doc(
		params = {
			"departments": "Provide a comma separated list of department IDs",
			"keywords": "Provide a comma separated list of keywords",
			"genEds": "Provide a comma separated list of Gen Ed IDs",
			"fields": "Provide a comma separated list of fields you would like back"
		}
	)
	def get(self):
		courseQuery = "SELECT course_id, description, same_as, name, department_id FROM Courses GROUP BY (name);"

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
		courseQuery = "SELECT course_id, description, same_as, name, department_id FROM Courses WHERE course_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		#MORE CODE FOR FIELD LIMITING

		cursor.execute(courseQuery % str(courseId))

		returnCourse = None
		for (course_id, description, same_as, name, department_id) in cursor:
			requirements = getRequirements(course_id)
			recommendations = getRecommendations(course_id)

			if same_as == "nan":
				course = CourseObject(course_id, description, None, name, department_id, None, requirements, recommendations)
			else:
				course = CourseObject(course_id, description, same_as, name, department_id, None, requirements, recommendations)

			returnCourse = course.__dict__

		cursor.close()
		cnx.close()

		return returnCourse



