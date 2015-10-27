# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask, request
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a department object should contain
class DepartmentJSON(object):
	def __init__(self, abbreviation = None, name = None, department_id = None, division_id = None):
		self.abbreviation = abbreviation
		self.name = name
		self.department_id = department_id
		self.division_id = division_id

app = Flask(__name__)
departmentApp = Api(app)
departmentAPI = departmentApp.namespace('api', 'Root namespace for NorseCourse APIs')

@departmentAPI.route("/departments")
class Department(Resource):
	@departmentApp.doc(
		params = {
			"division_ids": "Provide a comma separated list of division IDs"
		}
	)
	def get(self):
		departmentQuery = "SELECT abbreviation, name, department_id, division_id FROM Departments"
		
		division_ids = request.args.get("division_ids")
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
			dept = DepartmentJSON(str(abbreviation), str(name), department_id, division_id)
			departments.append(dept.__dict__)

		cursor.close()
		cnx.close()

		return departments


if __name__ == "__main__":
	app.debug = True
	app.run()