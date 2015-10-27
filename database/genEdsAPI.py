# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask, request
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a gen ed object should contain
class GenEdJSON(object):
	def __init__(self, gen_ed_id = None, name = None, abbreviation = None, also_fulfills = None):
		self.gen_ed_id = gen_ed_id
		self.name = name
		self.abbreviation = abbreviation
		self.also_fulfills = also_fulfills

app = Flask(__name__)
genEdApp = Api(app)
genEdAPI = genEdApp.namespace('api', 'Root namespace for NorseCourse APIs')

@genEdAPI.route("/gen_eds")
class GenEd(Resource):
	@genEdApp.doc(
		params = {
			"fulfills": "Provide a comma separated list of gen ed abbreviations"
		}
	)
	def get(self):
		genEdQuery = "SELECT gen_ed_id, name, abbreviation, also_fulfills FROM GenEds"

		gen_ed_abbreviations = request.args.get("fulfills")
		abbreviation_list = []
		if gen_ed_abbreviations != None:
			abbreviation_list = gen_ed_abbreviations.split(",")
			abbreviation_list = map(str, abbreviation_list)

			genEdQuery += " WHERE also_fulfills = %s"
			for i in range(len(abbreviation_list) - 1):
				genEdQuery += " OR also_fulfills = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		if len(abbreviation_list) > 0:
			cursor.execute(genEdQuery, tuple(abbreviation_list))
		else:
			cursor.execute(genEdQuery)

		genEds = []
		for (gen_ed_id, name, abbreviation, also_fulfills) in cursor:
			if also_fulfills == "":
				genEd = GenEdJSON(gen_ed_id, str(name), str(abbreviation))
			else:
				genEd = GenEdJSON(gen_ed_id, str(name), str(abbreviation), str(also_fulfills))
			genEds.append(genEd.__dict__)

		cursor.close()
		cnx.close()

		return genEds

if __name__ == "__main__":
	app.debug = True
	app.run()