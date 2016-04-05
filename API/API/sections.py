from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import SectionObject, FacultyObject, SectionMeetingObject, RoomObject, GenEdFulfillmentObject



@API.route("/sections", endpoint='sections')
class Section(Resource):

	# Returns JSON dictionary of faculty for a given section
	def getFaculty(self, section_id):
		facultyQuery = "SELECT first_initial, last_name, Faculty.faculty_id FROM Faculty, FacultyAssignments WHERE Faculty.faculty_id = FacultyAssignments.faculty_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(facultyQuery % str(section_id))

		profs = []
		for (first_initial, last_name, faculty_id) in cursor:
			fi = first_initial.split(',')
			ln = last_name.split(',')
			fid = faculty_id
			for p in range(len(ln)):
				faculty = FacultyObject(fi[p], ln[p],fid,fi[p]+". "+ln[p])
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
			"fields": "Provide a comma separated list of fields you would like back",
			"facultyId": "Provide a comma separated list of faculty IDs",
			"facutlyName": "Provide the name of faculty Last_name,first_initial (Ex: Miller,B)"
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


		new_faculty_ids = []

		def multipleNames(prof):
			count = 0
			for letter in prof:
				if letter == " ":
					count += 1
			if count == 1:
				return False
			return True

		def getMultiple(fi,ln):
			more_ids = []
			for prof in allfaculty:
				if multipleNames(allfaculty[prof]):
					names = allfaculty[prof].split(" ")
					first = names[:len(names)//2]
					last = names[len(names)//2:]

					final_pos = 0
					pos = 0
					for l in first:
						l = l.replace(",","")
						if l == fi:
							final_pos = pos
						pos += 1
					pos = 0
					for n in last:
						n = n.replace(",","")
						if n == ln:
							if pos == final_pos:
								more_ids.append(prof)
						pos += 1

			return more_ids


		allFaculty = "SELECT faculty_id, first_initial, last_name FROM Faculty"
		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()
		cursor.execute(allFaculty)

		allfaculty = {}
		for (faculty_id, first_initial,last_name) in cursor:
			allfaculty[faculty_id] = str(first_initial)+" "+str(last_name)

		cursor.close()
		cnx.close()


		faculty_Query = "SELECT faculty_id, first_initial,last_name FROM Faculty"

		faculty_name = request.args.get("facutlyName")

		faculty_check = False

		if faculty_name != None:
			faculty_check = True
			n = faculty_name.split(",")
			faculty_Query += " WHERE first_initial = \'" + n[1] + "\' and last_name = \'" + n[0] + "\'"
		
		faculty_ids = request.args.get("facultyId")
		id_list = []

		if faculty_ids != None:

			faculty_check = True
			id_list = faculty_ids.split(",")
			id_list = list(map(str, id_list))

			faculty_Query += " WHERE faculty_id = %s"
			for i in range(len(id_list) - 1):
				faculty_Query += " OR faculty_id = %s"



		if faculty_check:
			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()
			if len(id_list) > 0:
				cursor.execute(faculty_Query, tuple(id_list))
			else:
				cursor.execute(faculty_Query)

			faculty = []
			more_ids = []
			for (faculty_id, first_initial,last_name) in cursor:
				new_faculty_ids.append(faculty_id)
				more_ids = (getMultiple(str(first_initial),str(last_name)))

			cursor.close() ########
			cnx.close()

			if len(more_ids) > 0:
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()

				for ids in more_ids:
					faculty_Query = "SELECT faculty_id, first_initial,last_name FROM Faculty WHERE faculty_id = " + str(ids)
					cnx = cnx_pool.get_connection()
					cursor = cnx.cursor()
					cursor.execute(faculty_Query)
					for (faculty_id, first_initial,last_name) in cursor:
						new_faculty_ids.append(faculty_id)

				cursor.close() ######
				cnx.close()



		faculty_ids = new_faculty_ids
		id_list2 = []


		facultyQuery = "SELECT section_id from FacultyAssignments"
		check = False

		if faculty_ids != None and faculty_ids != []:
			check = True
			#id_list2 = faculty_ids.split(",")
			id_list2 = list(map(str, faculty_ids))

			facultyQuery += " WHERE faculty_id = %s"
			for i in range(len(id_list2) - 1):
				facultyQuery += " OR faculty_id = %s"


			cnx = cnx_pool.get_connection()
			cursor = cnx.cursor()

			if len(id_list2) > 0:
				cursor.execute(facultyQuery, tuple(id_list2))
			else:
				cursor.execute(facultyQuery)

			sectIDS = []
			for (section_id) in cursor:
				sectIDS.append(section_id[0])

			cursor.close() ######
			cnx.close()



		# facultyQuery = "SELECT section_id from FacultyAssignments"

		# faculty_ids = request.args.get("facultyId")
		# id_list2 = []

		# check = False
		# if faculty_ids != None:
		# 	check = True
		# 	id_list2 = faculty_ids.split(",")
		# 	id_list2 = list(map(str, id_list2))

		# 	facultyQuery += " WHERE faculty_id = %s"
		# 	for i in range(len(id_list2) - 1):
		# 		facultyQuery += " OR faculty_id = %s"

		# 	cnx = cnx_pool.get_connection()
		# 	cursor = cnx.cursor()


		# 	if len(id_list2) > 0:
		# 		cursor.execute(facultyQuery, tuple(id_list2))
		# 	else:
		# 		cursor.execute(facultyQuery)

		# 	sectIDS = []
		# 	for (section_id) in cursor:
		# 		sectIDS.append(section_id[0])






		sectionQuery = "SELECT term, name, short_title, min_credits, max_credits, comments, seven_weeks, course_id, section_id FROM Sections"
		
		course = request.args.get("courses")
		id_list = []

		if course != None:
			id_list = course.split(",")
			id_list = list(map(str, id_list))

			sectionQuery += " WHERE course_id = %s"
			for i in range(len(id_list) - 1):
				sectionQuery += " OR course_id = %s"

			if check:
				sectionQuery += " and (section_id = %s"
				for i in range(len(sectIDS) - 1):
					sectionQuery += " OR section_id = %s"
				sectionQuery += ")"

				id_list += sectIDS
		else:
			if check:
				sectionQuery += " WHERE section_id = %s"
				for i in range(len(sectIDS) - 1):
					sectionQuery += " OR section_id = %s"

				id_list = sectIDS


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
		facultyQuery = "SELECT first_initial, last_name, Faculty.faculty_id FROM Faculty, FacultyAssignments WHERE Faculty.faculty_id = FacultyAssignments.faculty_id AND section_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		cursor.execute(facultyQuery % str(section_id))

		profs = []
		for (first_initial, last_name, faculty_id) in cursor:
			fi = first_initial.split(',')
			ln = last_name.split(',')
			fid = faculty_id
			for p in range(len(ln)):
				faculty = FacultyObject(fi[p], ln[p],fid,fi[p]+". "+ln[p])
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
			id_list = list(map(str, id_list))

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

