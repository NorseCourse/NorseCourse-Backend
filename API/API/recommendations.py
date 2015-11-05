# Code to get and post recommendations
from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource

parser = NorseCourse.parser()
parser.add_argument(
	"recommendations", 
	type=list, 
	required=True, 
	help='{"recommendations": [{"courseId": cId, "divisionId": dId}, {"courseId": cId, ...}]} Strings must be quoted in double quotes', 
	location="json"
)

@API.route("/recommendations")
class Recommendations(Resource):
	@NorseCourse.doc(
		parser = parser
	)
	def post(self):
		insertRecommendation = "INSERT INTO Recommendations (course_id, division_id) VALUES (%s, %s)"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		
		args = parser.parse_args()
		recommendations = args["recommendations"]

		for recommendation in recommendations:
			cursor.execute(insertRecommendation % (recommendation["courseId"], recommendation["divisionId"]))

		cnx.commit()
		cursor.close()
		cnx.close()
		return "The recommendations have been recorded"