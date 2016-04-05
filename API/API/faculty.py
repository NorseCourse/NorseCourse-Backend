from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import FacultyObject






@API.route("/faculty")
class Faculty(Resource):

	@NorseCourse.doc(
		params = {
			"facultyId": "Provide comma seperated faculty IDs",
			"facutlyName": "Provide the name of faculty Last_name,first_initial (Ex: Miller,B)"
		}
	)

	def get(self):

		def multipleNames(prof):
			count = 0
			for letter in prof:
				if letter == " ":
					count += 1
			if count == 1:
				return False
			return True

		def getMultiple(fi,ln):
			more_ids = []
			for prof in allfaculty:
				if (fi in allfaculty[prof]) and (ln in allfaculty[prof]) and multipleNames(allfaculty[prof]):
					more_ids.append(prof)
			return more_ids


		allFaculty = "SELECT faculty_id, first_initial, last_name FROM Faculty"
		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		cursor.execute(allFaculty)

		allfaculty = {}
		for (faculty_id, first_initial,last_name) in cursor:
			allfaculty[faculty_id] = str(first_initial)+" "+str(last_name)

		cursor.close()
		cnx.close()


		facultyQuery = "SELECT faculty_id, first_initial,last_name FROM Faculty"

		faculty_name = request.args.get("facutlyName")

		if faculty_name != None:
			n = faculty_name.split(",")
			facultyQuery += " WHERE first_initial = \'" + n[1] + "\' and last_name = \'" + n[0] + "\'"
			print("\n\n\n\n")
			print(facultyQuery)
			print("\n\n\n\n")
		
		faculty_ids = request.args.get("facultyId")
		id_list = []

		if faculty_ids != None:
			id_list = faculty_ids.split(",")
			id_list = list(map(str, id_list))

			facultyQuery += " WHERE faculty_id = %s"
			for i in range(len(id_list) - 1):
				facultyQuery += " OR faculty_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		if len(id_list) > 0:
			cursor.execute(facultyQuery, tuple(id_list))
		else:
			cursor.execute(facultyQuery)

		faculty = []
		# (fi,ln):[more_ids]
		more_ids = {}
		for (faculty_id, first_initial,last_name) in cursor:
			more_ids[(str(first_initial),str(last_name))] = getMultiple(str(first_initial),str(last_name))
			f = FacultyObject(str(first_initial), str(last_name),faculty_id,str(first_initial) + ". " + str(last_name))
			faculty.append(f.__dict__)

		cursor.close()
		cnx.close()

		# {ids: [fi,ln]}
		to_add = {}
		for x in more_ids:
			for more_i in more_ids[x]:
				to_add[more_i] = []

		for ids in to_add:
			facultyQuery = "SELECT faculty_id, first_initial,last_name FROM Faculty WHERE faculty_id = " + str(ids)
			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()
			cursor.execute(facultyQuery)
			for (faculty_id, first_initial,last_name) in cursor:
				f = FacultyObject(str(first_initial), str(last_name),faculty_id,str(first_initial) + ". " + str(last_name))
				faculty.append(f.__dict__)


		return faculty