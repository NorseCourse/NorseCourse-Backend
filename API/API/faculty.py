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
		for (faculty_id, first_initial,last_name,name) in cursor:
			f = FacultyObject(str(first_initial), str(last_name),faculty_id,str(first_initial) + ". " + str(last_name))
			faculty.append(f.__dict__)

		cursor.close()
		cnx.close()

		return faculty