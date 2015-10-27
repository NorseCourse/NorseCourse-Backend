# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)


app = Flask(__name__)
termApp = Api(app)
termAPI = termApp.namespace('api', 'Root namespace for NorseCourse APIs')

@termAPI.route("/terms")
class Division(Resource):
	@termApp.doc()
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


if __name__ == "__main__":
	app.debug = True
	app.run()