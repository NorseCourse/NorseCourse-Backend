import mysql.connector
import mysql.connector.pooling

import config

import pandas as pd


def populateDB(cursor, data):
	try:

		divisions = set()
		departments = set()
		courses = set()
		courses2 = set()
		gen_eds = set()
		buildings = set()
		rooms = set()
		profs = set()


		numberPrint = 0
		for idx,row in data.iterrows():
			print(numberPrint)
			numberPrint+=1

			#division table

			if row['division'] not in divisions:
				divisions.add(row['division'])
				insert_division = "INSERT INTO Divisions (name) VALUES (%(name)s)"
				cursor.execute(insert_division, {"name": str(row['division'])})


			# department table

			if row['department_name'] not in departments:

				departments.add(row['department_name'])

				div_id_query = "SELECT MAX(division_id) FROM Divisions WHERE name=%(name)s"
				cursor.execute(div_id_query,{'name':str(row['division'])})

				for (division_id) in cursor:
					div_id = int(division_id[0])

				insert_department = "INSERT INTO Departments (name,abbreviation,division_id) VALUES (%(name)s,%(abb)s,%(d_id)s)"
				cursor.execute(insert_department, {"name": str(row['department_name']),"abb": str(row['department_abbreviation']),"d_id": str(div_id)})
	



			# course table
				
			if row['course_id'] not in courses:

				courses.add(row['course_id'])

				dept_id_query = "SELECT department_id FROM Departments WHERE name=%(name)s"
				cursor.execute(dept_id_query,{'name':str(row['department_name'])})

				for (department_id) in cursor:
					dept_id = int(department_id[0])

				insert_course = "INSERT INTO Courses (course_id,description,same_as,number,department_id) VALUES (%(cid)s,%(desc)s,%(same_as)s,%(number)s,%(dept_id)s)"
				cursor.execute(insert_course,{'cid':str(row['course_id']),
												'desc':str(row['course_description']),
												'same_as':str(row['same_as']),
												'number':str(row['section_name']),
												'dept_id':str(dept_id)
												})	



			# section table

			course_num_query = "SELECT course_id FROM Courses WHERE number=%(num)s"
			cursor.execute(course_num_query,{'num':str(row['section_name'])})

			for (course_id) in cursor:
				course_id = int(course_id[0])


			insert_course = "INSERT INTO Sections (term,name,short_title,min_credits,max_credits,comments,seven_weeks,course_id) VALUES (%(term)s,%(name)s,%(short_title)s,%(min_credits)s,%(max_credits)s,%(comments)s,%(seven_weeks)s,%(course_id)s)"
			cursor.execute(insert_course,{'term':str(row['term']),
											'name':str(row['section_name']),
											'short_title':str(row['section_title']),
											'min_credits':str(row['min_credits']),
											'max_credits':str(row['max_credits']),
											'comments':str(row['section_comments']),
											'seven_weeks':str(row['seven_week']),
											'course_id':str(course_id)
											})


			# gen eds table

			gen_eds_dict = {'BL':'Biblical Studies', 'HB': 'Human Behavior', 'HBSSM': 'Human Behavior Social Science Methods', 'HE': 'Human Expression', 'HEPT': 'Human Expression Primary Text', 'HIST': 'Historical', 'INTCL': 'Intercultural','NWL': 'Natural World Lab','NWNL': 'Natural World Non-Lab','QUANT': 'Quantitative','REL': 'Religion','SKL': 'Skills Course','WEL': 'Wellness Course'}
			also_geneds = {'HBSSM':'HB','HEPT':'HE','NWL':'NWNL','BL':'', 'HB': '', 'HE': '', 'HIST': '', 'INTCL': '','NWNL': '','QUANT': '','REL': '','SKL': '','WEL': ''}


			if type(row['gen_ed_abb']) == str:
				geneds = row['gen_ed_abb'].split(',')

				for ge in geneds:
					if ge not in gen_eds:

						gen_eds.add(ge)

						insert_course = "INSERT INTO GenEds (name,abbreviation,also_fulfills) VALUES (%(name)s,%(abb)s,%(also)s)"
						cursor.execute(insert_course,{'name':str(gen_eds_dict[ge]),
														'abb':str(ge),
														'also':str(also_geneds[ge])
														})

			# Geneds Fulfillment table

			if type(row['gen_ed_abb']) == str:
				geneds = row['gen_ed_abb'].split(',')
				for gened in geneds:


					section_num_query = "SELECT MAX(section_id) FROM Sections"
					cursor.execute(section_num_query)

					for (section_id) in cursor:
						section_id = int(section_id[0])

					gened_id_query = "SELECT gen_ed_id FROM GenEds WHERE abbreviation=%(abb)s"
					cursor.execute(gened_id_query,{'abb':str(gened)})

					for (gid) in cursor:
						gened_id = int(gid[0])

					insert_course = "INSERT INTO GenEdFulfillments (gen_ed_id,section_id) VALUES (%(gid)s,%(sid)s)"
					cursor.execute(insert_course,{'gid':str(gened_id),
													'sid':str(section_id)
													})


			# Requriments table

			if row['course_id'] not in courses2:
				courses2.add(row['course_id'])

				if type(row['co_reqs']) == str:
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['co_reqs']),
												'type':"CO",
												'course':str(row['course_id'])
												})

				if type(row['pre_reqs']) == str:
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['pre_reqs']),
												'type':"PRE",
												'course':str(row['course_id'])
												})

				if type(row['lab']) == str:
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['lab']),
												'type':"LAB",
												'course':str(row['course_id'])
												})


			# faculty table

			if (row['faculty_first'],row['faculty_last']) not in profs:
				profs.add((row['faculty_first'],row['faculty_last']))
				insert_req = "INSERT INTO Faculty (first_initial,last_name) VALUES (%(first)s,%(last)s)"
				cursor.execute(insert_req,{'first':str(row['faculty_first']),
											'last':str(row["faculty_last"])
											})



			# faculty assignment table

			fid_query = "SELECT faculty_id FROM Faculty where first_initial=%(first)s and last_name=%(last)s"
			cursor.execute(fid_query,{'first':str(row['faculty_first']),'last':str(row['faculty_last'])})

			for (faculty_id) in cursor:
				fid = int(faculty_id[0])

			sid_query = "SELECT MAX(section_id) FROM Sections"
			cursor.execute(sid_query)

			for (section_id) in cursor:
				sid = int(section_id[0])

			insert_req = "INSERT INTO FacultyAssignments (faculty_id,section_id) VALUES (%(fid)s,%(sid)s)"
			cursor.execute(insert_req,{'fid':str(fid),
										'sid':str(sid)
										})


			# buildings table

			if row['building_abb'] not in buildings:
				buildings.add(row['building_abb'])
				insert_req = "INSERT INTO Buildings (name,abbreviation) VALUES (%(name)s,%(abb)s)"
				cursor.execute(insert_req,{'name':str(row['building_names']),
											'abb':str(row['building_abb'])
											})

			# rooms tables

			if (row['building_abb'],row['room']) not in rooms:
				rooms.add((row['building_abb'],row['room']))

				building_id_query = "SELECT building_id FROM Buildings WHERE abbreviation=%(abb)s"
				cursor.execute(building_id_query,{'abb':str(row['building_abb'])})

				for (bid) in cursor:
					bid = int(bid[0])

				insert_req = "INSERT INTO Rooms (building_id,number) VALUES (%(bid)s,%(num)s)"
				cursor.execute(insert_req,{'bid':str(bid),
											'num':str(row['room'])
											})


			# Sections meeting table

			building_id_query = "SELECT building_id FROM Buildings WHERE abbreviation=%(abb)s"
			cursor.execute(building_id_query,{'abb':str(row['building_abb'])})

			for (bid) in cursor:
				bid = int(bid[0])

			rid_query = "SELECT room_id FROM Rooms where building_id=%(bid)s and number=%(room)s"
			cursor.execute(rid_query,{'bid':str(bid),'room':str(row['room'])})

			for (room_id) in cursor:
				rid = int(room_id[0])

			sid_query = "SELECT MAX(section_id) FROM Sections"
			cursor.execute(sid_query)

			for (section_id) in cursor:
				sid = int(section_id[0])

			insert_req = "INSERT INTO SectionMeetings (room_id,section_id,start_time,end_time,days) VALUES (%(rid)s,%(sid)s,%(st)s,%(et)s,%(d)s)"
			cursor.execute(insert_req,{'rid':str(rid),
										'sid':str(sid),
										'st':str(row['start_time']),
										'et':str(row['end_time']),
										'd':str(row['days'])
										})


		print("done")



	except mysql.connector.Error as error:
		print("Failed to populate the database: {}".format(error))
		exit(1)


##############################################################################


data = pd.DataFrame.from_csv('data.csv', sep=None,index_col=None)

populate_db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(autocommit = False, **populate_db_properties)
cnx = cnx_pool.get_connection()
cursor = cnx.cursor()

populateDB(cursor, data)

cnx.commit()

cursor.close()
cnx.close()










