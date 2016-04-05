from API import NorseCourse, API, cnx_pool
from flask import request
from flask.ext.restplus import Resource
from  API.NorseCourseObjects import FacultyObject






@API.route("/faculty")
class Faculty(Resource):

	@NorseCourse.doc(
		params = {
			"facultyId": "Provide comma seperated faculty IDs",
			"facutlyName": "Provide the name of faculty Last_name,first_initial (Ex: Miller,B)"
		}
	)

	def get(self):

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


		facultyQuery = "SELECT faculty_id, first_initial,last_name FROM Faculty"

		faculty_name = request.args.get("facutlyName")

		if faculty_name != None:
			n = faculty_name.split(",")
			facultyQuery += " WHERE first_initial = \'" + n[1] + "\' and last_name = \'" + n[0] + "\'"
		
		faculty_ids = request.args.get("facultyId")
		id_list = []

		if faculty_ids != None:
			id_list = faculty_ids.split(",")
			id_list = list(map(str, id_list))

			facultyQuery += " WHERE faculty_id = %s"
			for i in range(len(id_list) - 1):
				facultyQuery += " OR faculty_id = %s"

		cnx = cnx_pool.get_connection()
		cursor = cnx.cursor()

		if len(id_list) > 0:
			cursor.execute(facultyQuery, tuple(id_list))
		else:
			cursor.execute(facultyQuery)


		faculty = []
		more_ids = []
		for (faculty_id, first_initial,last_name) in cursor:
			more_ids = (getMultiple(str(first_initial),str(last_name)))
			f = FacultyObject(str(first_initial), str(last_name),faculty_id,str(first_initial) + ". " + str(last_name))
			faculty.append(f.__dict__)

		cursor.close()
		cnx.close()


		if len(more_ids) > 0:

			for ids in more_ids:
				facultyQuery = "SELECT faculty_id, first_initial,last_name FROM Faculty WHERE faculty_id = " + str(ids)
				cnx = cnx_pool.get_connection()
				cursor = cnx.cursor()
				cursor.execute(facultyQuery)
				for (faculty_id, first_initial,last_name) in cursor:
					f = FacultyObject(str(first_initial), str(last_name),faculty_id,str(first_initial) + ". " + str(last_name))
					faculty.append(f.__dict__)

			cursor.close()
			cnx.close()



		return faculty