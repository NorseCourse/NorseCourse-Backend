from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  NorseCourseObjects import SectionObject, FacultyObject, SectionMeetingObject, RoomObject, GenEdFulfillmentObject



@API.route("/sections", endpoint='sections')
class Section(Resource):

	# Returns JSON dictionary of faculty for a given section
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
				faculty = FacultyObject(fi[p], ln[p])
				profs.append(faculty.__dict__)

		cursor.close()
		cnx.close()

		return profs


	# Returns JSON dictionary of section Meeting info for a given section
	def getSectionMeeting(self,section_id):

		sectionMeetingQuery = "SELECT room_id, start_time, end_time, days FROM SectionMeetings WHERE section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(sectionMeetingQuery % str(section_id))

		meetings = []
		for (room_id, start_time, end_time, days) in cursor:
			room = self.getRoom(room_id)

			if start_time == "":
				start_time = None
			if end_time == "":
				end_time = None

			meet = SectionMeetingObject(room_id, start_time, end_time, days,room)
			meetings.append(meet.__dict__)

		cursor.close()
		cnx.close()

		return meetings


	# Returns JSON dictionary of room info for a given room
	def getRoom(self,room_id):
		roomQuery = "SELECT number, name, abbreviation FROM Rooms, Buildings WHERE Buildings.building_id = Rooms.building_id AND room_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(roomQuery % str(room_id))

		room = []
		for (number, name, abbreviation) in cursor:
			r = RoomObject(room_id, number, name, abbreviation)
			room.append(r.__dict__)

		cursor.close()
		cnx.close()

		return room


	# Returns JSON dictionary of gen ed fulfillments for a given section
	def getGenEdFulfillment(self,section_id):

		genedQuery = "SELECT GenEds.gen_ed_id, comments, name, abbreviation, also_fulfills FROM GenEdFulfillments, GenEds WHERE GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(genedQuery % str(section_id))


		ge = []
		for (gen_ed_id, comments, name, abbreviation, also_fulfills) in cursor:

			if also_fulfills == "":
				also_fulfills = None

			gef = GenEdFulfillmentObject(gen_ed_id, comments, name, abbreviation,also_fulfills)
			ge.append(gef.__dict__)

		cursor.close()
		cnx.close()

		return ge



	@NorseCourse.doc(
		params = {
			"courses": "Provide a comma separated list of course IDs",
			"fields": "Provide a comma separated list of fields you would like back"
		}
	)

	def get(self):

		# Get the URL params
		fields = request.args.get("fields")
		if fields == None:
			fields = ['comments','courseId','faculty','GenEdFulfillments','id','maxCredits','minCredits','name','sectionMeetings','sevenWeeks','shortTitle','term']
		else:
			f = fields.split(",")
			fields = []
			for i in f:
				fields.append(str(i).replace(" ",""))


		sectionQuery = "SELECT term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id FROM Sections"
		
		course = request.args.get("courses")
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

		obj = {
				'comments':None,
				'courseId':None,
				'faculty':None,
				'GenEdFulfillments':None,
				'id':None,
				'maxCredits':None,
				'minCredits':None,
				'name':None,
				'sectionMeetings':None,
				'sevenWeeks':None,
				'shortTitle':None,
				'term':None
				}

				
		sections = []

		for (term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id) in cursor:


			if "faculty" in fields:
				prof = self.getFaculty(section_id)
				obj['faculty'] = prof

			if "sectionMeetings" in fields:
				sect_meeting = self.getSectionMeeting(section_id)
				obj["sectionMeetings"] = sect_meeting

			if "GenEdFulfillments" in fields:
				gef = self.getGenEdFulfillment(section_id)
				obj['GenEdFulfillments'] = gef

			if "term" in fields:
				obj['term'] = term

			if "sevenWeeks" in fields:
				obj['sevenWeeks'] = seven_weeks

			if "id" in fields:
				obj['id'] = section_id

			if "courseId" in fields:
				obj['courseId'] = course_id

			if comments != "nan" and "comments" in fields:
				obj['comments'] = comments

			if name != "nan" and "name" in fields:
				obj['name'] = name

			if short_title != "nan" and "shortTitle" in fields:
				obj['shortTitle'] = short_title

			if min_credits != "nan" and "minCredits" in fields:
				obj['minCredits'] = min_credits

			if max_credits != "nan" and "maxCredits" in fields:
				obj['maxCredits'] = max_credits

				
			sect = SectionObject(
				obj['term'], 
				obj['name'],
				obj['shortTitle'],
				obj['minCredits'],
				obj['maxCredits'],
				obj['comments'],
				obj['sevenWeeks'],
				obj['id'],
				obj['courseId'],
				obj['faculty'],
				obj['sectionMeetings'],
				obj['GenEdFulfillments']
				)

			sections.append(sect.__dict__)

		cursor.close()
		cnx.close()

		return sections




@API.route("/sections/<sectionId>", endpoint = "sections/")
class Section(Resource):

	# Returns JSON dictionary of faculty for a given section
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
				faculty = FacultyObject(fi[p], ln[p])
				profs.append(faculty.__dict__)

		cursor.close()
		cnx.close()

		return profs


	# Returns JSON dictionary of section Meeting info for a given section
	def getSectionMeeting(self,section_id):

		sectionMeetingQuery = "SELECT room_id, start_time, end_time, days FROM SectionMeetings WHERE section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(sectionMeetingQuery % str(section_id))

		meetings = []
		for (room_id, start_time, end_time, days) in cursor:
			room = self.getRoom(room_id)

			if start_time == "":
				start_time = None
			if end_time == "":
				end_time = None

			meet = SectionMeetingObject(room_id, start_time, end_time, days,room)
			meetings.append(meet.__dict__)

		cursor.close()
		cnx.close()

		return meetings


	# Returns JSON dictionary of room info for a given room
	def getRoom(self,room_id):
		roomQuery = "SELECT number, name, abbreviation FROM Rooms, Buildings WHERE Buildings.building_id = Rooms.building_id AND room_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(roomQuery % str(room_id))

		room = []
		for (number, name, abbreviation) in cursor:
			r = RoomObject(room_id, number, name, abbreviation)
			room.append(r.__dict__)

		cursor.close()
		cnx.close()

		return room


	# Returns JSON dictionary of gen ed fulfillments for a given section
	def getGenEdFulfillment(self,section_id):

		genedQuery = "SELECT GenEds.gen_ed_id, comments, name, abbreviation, also_fulfills FROM GenEdFulfillments, GenEds WHERE GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(genedQuery % str(section_id))

		ge = []
		for (gen_ed_id, comments, name, abbreviation, also_fulfills) in cursor:

			if also_fulfills == "":
				also_fulfills = None

			gef = GenEdFulfillmentObject(gen_ed_id, comments, name, abbreviation,also_fulfills)
			ge.append(gef.__dict__)

		cursor.close()
		cnx.close()

		return ge



	@NorseCourse.doc(
		params = {
			"sectionId": "Provide a section ID to get all of the information related to that section",
			"fields": "Provide a comma separated list of fields you would like back"
		}
	)

	def get(self,sectionId):

		# Get the URL params
		fields = request.args.get("fields")
		if fields == None:
			fields = ['comments','courseId','faculty','GenEdFulfillments','id','maxCredits','minCredits','name','sectionMeetings','sevenWeeks','shortTitle','term']
		else:
			f = fields.split(",")
			fields = []
			for i in f:
				fields.append(str(i).replace(" ",""))


		sectionQuery = "SELECT term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id FROM Sections"
		
		section_id = sectionId

		id_list = []

		if section_id != None:
			id_list = section_id.split(",")
			id_list = map(str, id_list)

			sectionQuery += " WHERE section_id = %s"
			for i in range(len(id_list) - 1):
				sectionQuery += " OR section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		if len(id_list) > 0:
			cursor.execute(sectionQuery, tuple(id_list))
		else:
			cursor.execute(sectionQuery)

		obj = {
				'comments':None,
				'courseId':None,
				'faculty':None,
				'GenEdFulfillments':None,
				'id':None,
				'maxCredits':None,
				'minCredits':None,
				'name':None,
				'sectionMeetings':None,
				'sevenWeeks':None,
				'shortTitle':None,
				'term':None
				}

		sections = []

		for (term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id) in cursor:

			if "faculty" in fields:
				prof = self.getFaculty(section_id)
				obj['faculty'] = prof

			if "sectionMeetings" in fields:
				sect_meeting = self.getSectionMeeting(section_id)
				obj["sectionMeetings"] = sect_meeting

			if "GenEdFulfillments" in fields:
				gef = self.getGenEdFulfillment(section_id)
				obj['GenEdFulfillments'] = gef

			if "term" in fields:
				obj['term'] = term

			if "sevenWeeks" in fields:
				obj['sevenWeeks'] = seven_weeks

			if "id" in fields:
				obj['id'] = section_id

			if "courseId" in fields:
				obj['courseId'] = course_id

			if comments != "nan" and "comments" in fields:
				obj['comments'] = comments

			if name != "nan" and "name" in fields:
				obj['name'] = name

			if short_title != "nan" and "shortTitle" in fields:
				obj['shortTitle'] = short_title

			if min_credits != "nan" and "minCredits" in fields:
				obj['minCredits'] = min_credits

			if max_credits != "nan" and "maxCredits" in fields:
				obj['maxCredits'] = max_credits

				
			sect = SectionObject(
				obj['term'], 
				obj['name'],
				obj['shortTitle'],
				obj['minCredits'],
				obj['maxCredits'],
				obj['comments'],
				obj['sevenWeeks'],
				obj['id'],
				obj['courseId'],
				obj['faculty'],
				obj['sectionMeetings'],
				obj['GenEdFulfillments']
				)

			sections.append(sect.__dict__)

		cursor.close()
		cnx.close()

		return sections[0]

