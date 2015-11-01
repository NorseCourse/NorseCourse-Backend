from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  NorseCourseObjects import DepartmentObject

@API.route("/departments")
class Departments(Resource):
	@NorseCourse.doc(
		params = {
			"divisionIds": "Provide a comma separated list of division IDs"
		}
	)
	def get(self):
		departmentQuery = "SELECT abbreviation, name, department_id, division_id FROM Departments"
		
		division_ids = request.args.get("divisionIds")
		id_list = []

		if division_ids != None:
			id_list = division_ids.split(",")
			id_list = map(str, id_list)

			departmentQuery += " WHERE division_id = %s"
			for i in range(len(id_list) - 1):
				departmentQuery += " OR division_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		if len(id_list) > 0:
			cursor.execute(departmentQuery, tuple(id_list))
		else:
			cursor.execute(departmentQuery)

		departments = []
		for (abbreviation, name, department_id, division_id) in cursor:
			dept = DepartmentObject(str(abbreviation), str(name), department_id, division_id)
			departments.append(dept.__dict__)

		cursor.close()
		cnx.close()

		return departments