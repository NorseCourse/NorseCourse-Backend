from NorseCourse import API, cnx_pool
from flask.ext.restplus import Resource

@API.route("/terms")
class Terms(Resource):
	def get(self):
		termQuery = "SELECT DISTINCT term FROM Sections"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(termQuery)

		terms = []
		for term in cursor:
			terms.append(str(term[0]))

		cursor.close()
		cnx.close()

		return terms