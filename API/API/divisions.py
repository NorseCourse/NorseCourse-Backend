from API import API, cnx_pool
from flask.ext.restplus import Resource
from  NorseCourseObjects import DivisionObject

@API.route("/divisions")
class Divisions(Resource):
	def get(self):
		divisionQuery = "SELECT name, division_id FROM Divisions"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(divisionQuery)

		divisions = []
		for (name, division_id) in cursor:
			div = DivisionObject(str(name), division_id)
			divisions.append(div.__dict__)

		cursor.close()
		cnx.close()

		return divisions