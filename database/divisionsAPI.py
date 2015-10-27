# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a division object should contain
class DivisionJSON(object):
	def __init__(self, name = None, division_id = None):
		self.name = name
		self.division_id = division_id

app = Flask(__name__)
divisionApp = Api(app)
divisionAPI = divisionApp.namespace('api', 'Root namespace for NorseCourse APIs')

@divisionAPI.route("/divisions")
class Division(Resource):
	@divisionApp.doc()
	def get(self):
		divisionQuery = "SELECT name, division_id FROM Divisions"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(divisionQuery)

		divisions = []
		for (name, division_id) in cursor:
			div = DivisionJSON(str(name), division_id)
			divisions.append(div.__dict__)

		cursor.close()
		cnx.close()

		return divisions


if __name__ == "__main__":
	app.debug = True
	app.run()