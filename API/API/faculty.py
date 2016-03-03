from API import API, cnx_pool
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import DivisionObject

@API.route("/faculty")
class Faculty(Resource):

	@NorseCourse.doc(
		params = {
			"facultyId": "Provide comma seperated faculty IDs"
		}
	)

	def get(self):
		facultyQuery = "SELECT faculty_id, first_initial,last_name FROM Faculty"

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

		cursor.execute(facultyQuery)

		faculty = []
		for (faculty_id, first_initial,last_name) in cursor:
			f = FacultyObjectID(str(first_initial), str(last_name),faculty_id)
			faculty.append(f.__dict__)

		cursor.close()
		cnx.close()

		return faculty