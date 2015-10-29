# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

from flask import Flask, request
from flask.ext.restplus import Api, Resource

# Grab the correct set of properties to use and create a connection pool
db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

# What a section object should contain
class SectionJSON(object):
	def __init__(self, term = None, name = None, short_title= None, min_credits=None, max_credits=None, comments=None, seven_weeks=None, section_id = None, course_id = None,faculty=None,section_meetings=None):
		self.term = term
		self.name = name
		self.shortTitle = short_title
		self.minCredits = min_credits
		self.maxCredits = max_credits
		self.comments = comments
		self.sevenWeeks = seven_weeks
		self.id = section_id
		self.courseId = course_id
		self.faculty = faculty
		self.sectionMeetings = section_meetings


# What a faculty object should contain
class FacultyJSON(object):
	def __init__(self, first_initial = None, last_name = None):
		self.first_initial = first_initial
		self.last_name = last_name

# What a sectionMeeting object should contain
class SectionMeetingJSON(object):
	def __init__(self, room_id = None, start_time = None, end_time = None,days=None,room=None):
		self.roomId = room_id
		self.startTime = start_time
		self.endTime = end_time
		self.days = days
		self.room = room

# What a room object should contain
class RoomJSON(object):
	def __init__(self, id = None, number = None, building_name = None, building_abb = None):
		self.id = id
		self.number = number
		self.buildingName = building_name
		self.buildingAbbrevation = building_abb


app = Flask(__name__)
sectionApp = Api(app)
sectionAPI = sectionApp.namespace('api', 'Root namespace for NorseCourse APIs')


@sectionAPI.route("/sections")
class Section(Resource):

	def getFaculty(self, section_id):
		facultyQuery = "SELECT first_initial, last_name FROM Faculty, FacultyAssignments WHERE Faculty.faculty_id = FacultyAssignments.faculty_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(facultyQuery % str(section_id))

		profs = []
		for (first_initial, last_name) in cursor:
			fi = first_initial.split(',')
			ln = last_name.split(',')
			for p in range(len(ln)):
				faculty = FacultyJSON(fi[p], ln[p])
				profs.append(faculty.__dict__)

		cursor.close()
		cnx.close()

		return profs


	def getSectionMeeting(self,section_id):

		sectionMeetingQuery = "SELECT room_id, start_time, end_time, days FROM SectionMeetings WHERE section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(sectionMeetingQuery % str(section_id))

		meetings = []
		for (room_id, start_time, end_time, days) in cursor:
			room = self.getRoom(room_id)

			meet = SectionMeetingJSON(room_id, start_time, end_time, days,room)
			meetings.append(meet.__dict__)

		cursor.close()
		cnx.close()

		return meetings

	def getRoom(self,room_id):
		roomQuery = "SELECT number, name, abbreviation FROM Rooms, Buildings WHERE Buildings.building_id = Rooms.building_id AND room_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(roomQuery % str(room_id))

		room = []
		for (number, name, abbreviation) in cursor:
			r = RoomJSON(room_id, number, name, abbreviation)
			room.append(r.__dict__)

		cursor.close()
		cnx.close()

		return room


	@sectionApp.doc(
		params = {
			"course": "Provide a comma separated list of course IDs"
		}
	)
	def get(self):
		sectionQuery = "SELECT term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id FROM Sections"
		
		course = request.args.get("course")
		id_list = []
		if course != None:
			id_list = course.split(",")
			id_list = map(str, id_list)

			sectionQuery += " WHERE course_id = %s"
			for i in range(len(id_list) - 1):
				sectionQuery += " OR course_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		if len(id_list) > 0:
			cursor.execute(sectionQuery, tuple(id_list))
		else:
			cursor.execute(sectionQuery)

		sections = []
		printcount = 0
		for (term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id) in cursor:
			print(printcount)
			printcount+=1
			prof = self.getFaculty(section_id)
			sect_meeting = self.getSectionMeeting(section_id)

			if comments == "nan":
				sect = SectionJSON(term, name,short_title,min_credits,max_credits,None,seven_weeks,section_id,course_id,prof,sect_meeting)
			else:
				sect = SectionJSON(term, name,short_title,min_credits,max_credits,comments,seven_weeks,section_id,course_id,prof,sect_meeting)

			sections.append(sect.__dict__)

		cursor.close()
		cnx.close()

		return sections


if __name__ == "__main__":
	app.debug = True
	app.run()














