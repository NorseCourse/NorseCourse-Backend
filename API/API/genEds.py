from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import GenEdObject

@API.route("/genEds")
class GenEds(Resource):
	@NorseCourse.doc(
		params = {
			"alsoFulfills": "Provide a comma separated list of Gen Ed abbreviations"
		}
	)
	def get(self):
		genEdQuery = "SELECT gen_ed_id, name, abbreviation, also_fulfills FROM GenEds"

		gen_ed_abbreviations = request.args.get("alsoFulfills")
		abbreviation_list = []

		if gen_ed_abbreviations != None:
			abbreviation_list = gen_ed_abbreviations.split(",")
			abbreviation_list = list(map(str, abbreviation_list))

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
				genEd = GenEdObject(gen_ed_id, str(name), str(abbreviation), None)
			else:
				genEd = GenEdObject(gen_ed_id, str(name), str(abbreviation), str(also_fulfills))
			genEds.append(genEd.__dict__)

		cursor.close()
		cnx.close()

		return genEds