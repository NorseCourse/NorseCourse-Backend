from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import CourseObject, RequirementObject
from API.relevance import relevance


def getRequirements(course_id):
	requirementQuery = "SELECT req_type, details FROM Requirements WHERE course_id = %s"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(requirementQuery % str(course_id))

	requirements = []
	for (req_type, details) in cursor:
		requirement = RequirementObject(req_type, details)
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


def buildCoursesJSON(cursor, coursesTerms, showRelevance, relevantNums, relevantCount, showRequirements, showRecommendations, showCourseId):
	courses = []
	for result in cursor:
		# Temp object for storing the course info as the fields can be passed in in any order.
		tempObj = {
			"short_title": None,
			"course_id": None,
			"description": None,
			"same_as": None,
			"name": None,
			"department_id": None
			}

		for (item, ct) in zip(result, coursesTerms):
			tempObj[ct] = item
		if tempObj["same_as"] == "nan":
			tempObj["same_as"] = None


		relevance = None
		if showRelevance:
			if relevantNums != []:
				relevance = relevantNums[relevantCount]
			else:
				relevance = "Must provide keywords in order to see relevance"

		requirements = None
		if showRequirements:
			requirements = getRequirements(tempObj["course_id"])

		recommendations = None
		if showRecommendations:
			recommendations = getRecommendations(tempObj["course_id"])

		if showCourseId:
			course = CourseObject(tempObj["short_title"], tempObj["course_id"], tempObj["description"], tempObj["same_as"], tempObj["name"], tempObj["department_id"], relevance, requirements, recommendations)
		else:
			course = CourseObject(tempObj["short_title"], None, tempObj["description"], tempObj["same_as"], tempObj["name"], tempObj["department_id"], relevance, requirements, recommendations)

		courses.append(course.__dict__)

	if len(courses) > 1:
		return courses
	else:
		return course.__dict__


coursesDict = {
	"title": "short_title",
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
		departments = request.args.get("departments")
		if departments == None:
			courseIdsByDept = []
		else:
			departments = departments.split(",")
			getCoursesByDeptQuery = "SELECT course_id FROM Courses WHERE department_id = %s"
			deptsLen = len(departments)
			if deptsLen > 1:
				for i in range(deptsLen - 1):
					getCoursesByDeptQuery += " OR department_id = %s"
			
			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			courseIdsByDept = []
			cursor.execute(getCoursesByDeptQuery % tuple(departments))
			for res in cursor:
				courseIdsByDept.append(res[0])
 
			cursor.close()
			cnx.close()

		genEds = request.args.get("genEds")
		if genEds == None:
			courseIdsByGenEd = []
		else:
			genEds = genEds.split(",")
			getCoursesByGenEdQuery = "SELECT DISTINCT (Courses.course_id) FROM Courses, Sections, GenEdFulfillments, GenEds WHERE (GenEds.gen_ed_id = %s"
			genEdsLen = len(genEds)
			if genEdsLen > 1:
				for i in range(genEdsLen - 1):
					getCoursesByGenEdQuery += " OR GenEds.gen_ed_id = %s"
			getCoursesByGenEdQuery += ") AND GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id AND GenEdFulfillments.section_id = Sections.section_id AND Sections.course_id = Courses.course_id"
			
			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			courseIdsByGenEd = []
			cursor.execute(getCoursesByGenEdQuery % tuple(genEds))
			for res in cursor:
				courseIdsByGenEd.append(res[0])

			cursor.close()
			cnx.close()


		keywords = request.args.get("keywords")
		if keywords == None:
			coursesByKeyword = []
		else:
			keywords = keywords.split(",")
			relevantCourses = relevance(keywords)
			coursesByKeyword = [result[0] for result in relevantCourses]
			relevanceNumber = [result[1] for result in relevantCourses]

		# Logic to decide how which courses whould be searched for
		useFilter = True
		courseIdsIntersection = []
		relevantNums = []
		if departments != None and genEds != None and keywords != None:
			deptSet = set(courseIdsByDept)
			genEdSet = set(courseIdsByGenEd)
			courseIdsIntersection = deptSet.intersection(genEdSet)
			courseIdsIntersection = list(courseIdsIntersection.intersection(coursesByKeyword))
			for cId in courseIdsIntersection:
				relevantNums.append(relevanceNumber[coursesByKeyword.index(cId)])

		elif departments != None and genEds != None:
			deptSet = set(courseIdsByDept)
			genEdSet = set(courseIdsByGenEd)
			courseIdsIntersection = list(deptSet.intersection(genEdSet))

		elif departments != None and keywords != None:
			deptSet = set(courseIdsByDept)
			kwSet = set(coursesByKeyword)
			courseIdsIntersection = list(deptSet.intersection(kwSet))
			for cId in courseIdsIntersection:
				relevantNums.append(relevanceNumber[coursesByKeyword.index(cId)])

		elif genEds != None and keywords != None:
			genEdSet = set(courseIdsByGenEd)
			kwSet = set(coursesByKeyword)
			courseIdsIntersection = list(genEdSet.intersection(kwSet))
			for cId in courseIdsIntersection:
				relevantNums.append(relevanceNumber[coursesByKeyword.index(cId)])

		elif departments != None:
			courseIdsIntersection = courseIdsByDept

		elif genEds != None:
			courseIdsIntersection = courseIdsByGenEd

		elif keywords != None:
			courseIdsIntersection = coursesByKeyword
			relevantNums = relevanceNumber
			
		else:
			useFilter = False


		# Get the URL params
		fields = request.args.get("fields")
		if fields == None:
			showCourseId = True
			fields = ["title", "courseId", "description", "sameAs", "name", "departmentId", "requirements", "recommendations", "relevance"]
		else:
			fields = fields.split(",")
			if "courseId" not in fields and ("relevance" in fields or "recommendations" in fields or "requirements" in fields):
				showCourseId = False
				fields.append("courseId")
			else:
				showCourseId = True

		# Gather the terms for the course query.
		coursesTerms = []
		for field in fields:
			if field in coursesDict:
				coursesTerms.append(coursesDict[field])

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
			if useFilter:
				courseQuery += " FROM Courses WHERE course_id = %s"
			else:
				courseQuery += " FROM Courses"


		showRelevance = False
		if "relevance" in fields:
			showRelevance = True

		showRequirements = False
		if "requirements" in fields:
			showRequirements = True

		showRecommendations = False
		if "recommendations" in fields:
			showRecommendations = True;


		# Get a connecgtion and open up a cursor and execute the query
		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		relevantCount = 0
		if useFilter:
			courses = []
			for cId in courseIdsIntersection:
				cursor.execute(courseQuery % str(cId))
				courses.append(buildCoursesJSON(cursor, coursesTerms, showRelevance, relevantNums, relevantCount, showRequirements, showRecommendations, showCourseId))
				relevantCount += 1

		else: 
			cursor.execute(courseQuery)
			courses = buildCoursesJSON(cursor, coursesTerms, showRelevance, relevantNums, relevantCount, showRequirements, showRecommendations, showCourseId)


		# Close connection and cursor, then return the courses
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
			fields = ["title","courseId", "description", "sameAs", "name", "departmentId", "requirements", "recommendations", "relevance"]
		else:
			fields = fields.split(",")

		# Gather the terms for the course query.
		coursesTerms = []
		for field in fields:
			if field in coursesDict:
				coursesTerms.append(coursesDict[field])

		# Te,p object for storing the course info as the fields can be passed in in any order.
		tempObj = {
			"short_title": None,
			"course_id": None,
			"description": None,
			"same_as": None,
			"name": None,
			"department_id": None
			}

		# Get a connecgtion and open up a cursor and execute the query
		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

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

			cursor.execute(courseQuery % str(courseId))

			# Populate the temp object
			for result in cursor:
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
		returnCourse = CourseObject(tempObj["short_title"], tempObj["course_id"], tempObj["description"], tempObj["same_as"], tempObj["name"], tempObj["department_id"], relevance, requirements, recommendations)
		return returnCourse.__dict__