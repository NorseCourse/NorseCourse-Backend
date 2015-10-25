

##############################################################################
# The purpose of this file is to use the data.csv file created from readCSV.py
# to populate our database.  It iterrates through the csv file and connects 
# to our database and adds the necessary information, so we can access it later
# for use with the website.
##############################################################################

import mysql.connector
import mysql.connector.pooling

import config

import pandas as pd


def populateDB(cursor, data):

	# try populating database
	try:
		# create sets to keep track of what has already been added to database
		divisions = set()
		departments = set()
		courses = set()
		courses2 = set()
		gen_eds = set()
		buildings = set()
		rooms = set()
		profs = set()


		########################################################################
		# iterrate through all rows in data
		########################################################################
		for idx,row in data.iterrows():


			########################################################################
			# Divisions table
			########################################################################
			# checks if division has already been added or not, enters if statement when not already added
			if row['division'] not in divisions:
				# add divison to check set
				divisions.add(row['division'])
				# SQL statement to insert Division into Divisions table in database
				insert_division = "INSERT INTO Divisions (name) VALUES (%(name)s)"
				cursor.execute(insert_division, {"name": str(row['division'])})



			########################################################################
			# Departments table
			########################################################################
			# checks if department has not already been added
			if row['department_name'] not in departments:
				# add department to check set
				departments.add(row['department_name'])

				# SQL statement to find the divison_id from Divisions 
				div_id_query = "SELECT division_id FROM Divisions WHERE name=%(name)s"
				cursor.execute(div_id_query,{'name':str(row['division'])})

				# define its divison as div_id
				for (division_id) in cursor:
					div_id = int(division_id[0])


				# SQL statement to insert Department into Departments table in database
				insert_department = "INSERT INTO Departments (name,abbreviation,division_id) VALUES (%(name)s,%(abb)s,%(d_id)s)"
				cursor.execute(insert_department, {"name": str(row['department_name']),"abb": str(row['department_abbreviation']),"d_id": str(div_id)})
	


			########################################################################
			# Courses table
			########################################################################
			# if course not already added to database
			if row['course_id'] not in courses:
				# add course to check set
				courses.add(row['course_id'])


				# SQL statement to find department id of current deparment
				dept_id_query = "SELECT department_id FROM Departments WHERE name=%(name)s"
				cursor.execute(dept_id_query,{'name':str(row['department_name'])})

				# defines current department as dept_id
				for (department_id) in cursor:
					dept_id = int(department_id[0])


				# SQL insert statement of Courses
				insert_course = "INSERT INTO Courses (course_id,description,same_as,number,department_id) VALUES (%(cid)s,%(desc)s,%(same_as)s,%(number)s,%(dept_id)s)"
				cursor.execute(insert_course,{'cid':str(row['course_id']),
												'desc':str(row['course_description']),
												'same_as':str(row['same_as']),
												'number':str(row['section_name']),
												'dept_id':str(dept_id)
												})	



			########################################################################
			# Sections table
			########################################################################

			# SQL statement to find the course_id of the section
			course_num_query = "SELECT course_id FROM Courses WHERE number=%(num)s"
			cursor.execute(course_num_query,{'num':str(row['section_name'])})

			# define course as course_id
			for (course_id) in cursor:
				course_id = int(course_id[0])


			# SQL statement to insert into Sections
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



			########################################################################
			# GenEds table
			########################################################################

			# define GenEd names from abbreviation, and what gends cover others
			gen_eds_dict = {'BL':'Biblical Studies', 'HB': 'Human Behavior', 'HBSSM': 'Human Behavior Social Science Methods', 'HE': 'Human Expression', 'HEPT': 'Human Expression Primary Text', 'HIST': 'Historical', 'INTCL': 'Intercultural','NWL': 'Natural World Lab','NWNL': 'Natural World Non-Lab','QUANT': 'Quantitative','REL': 'Religion','SKL': 'Skills Course','WEL': 'Wellness Course'}
			also_geneds = {'HBSSM':'HB','HEPT':'HE','NWL':'NWNL','BL':'', 'HB': '', 'HE': '', 'HIST': '', 'INTCL': '','NWNL': '','QUANT': '','REL': '','SKL': '','WEL': ''}

			# if there is a gen ed
			if type(row['gen_ed_abb']) == str:
				# create list of all gen eds of section
				geneds = row['gen_ed_abb'].split(',')

				# iterate through all gen eds
				for ge in geneds:
					# check if the gen ed has already been added to database
					# gen_eds is check set
					if ge not in gen_eds:
						# add gen ed to check set
						gen_eds.add(ge)

						# SQL statement to insert in GenEds table the gen ed
						insert_course = "INSERT INTO GenEds (name,abbreviation,also_fulfills) VALUES (%(name)s,%(abb)s,%(also)s)"
						cursor.execute(insert_course,{'name':str(gen_eds_dict[ge]),
														'abb':str(ge),
														'also':str(also_geneds[ge])
														})



			########################################################################
			# GenEdFulfuillments table
			########################################################################

			# if section has a gen ed
			if type(row['gen_ed_abb']) == str:
				# create list of all geneds of section
				geneds = row['gen_ed_abb'].split(',')
				# iterate through list
				for gened in geneds:
					# SQL statement to find the current section id
					section_num_query = "SELECT MAX(section_id) FROM Sections"
					cursor.execute(section_num_query)

					# define section id as section_id
					for (section_id) in cursor:
						section_id = int(section_id[0])

					# SQL statement to find gen ed id from GenEds table
					gened_id_query = "SELECT gen_ed_id FROM GenEds WHERE abbreviation=%(abb)s"
					cursor.execute(gened_id_query,{'abb':str(gened)})

					# Define gen ed id as gened_id
					for (gid) in cursor:
						gened_id = int(gid[0])

					# SQL statement to insert into GenEdFulfillments 
					insert_course = "INSERT INTO GenEdFulfillments (gen_ed_id,section_id) VALUES (%(gid)s,%(sid)s)"
					cursor.execute(insert_course,{'gid':str(gened_id),
													'sid':str(section_id)
													})



			########################################################################
			# Requirements table
			########################################################################

			# check if course co/pre reqs are already added for that given course
			if row['course_id'] not in courses2:
				# add course to course2 check set, so it wont be added again
				courses2.add(row['course_id'])

				# check if there is a co req
				if type(row['co_reqs']) == str:
					# SQL statement to insert into Requirments the co req
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['co_reqs']),
												'type':"CO",
												'course':str(row['course_id'])
												})

				# check if there is a pre req
				if type(row['pre_reqs']) == str:
					# SQL statement to insert into Requirments the pre req
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['pre_reqs']),
												'type':"PRE",
												'course':str(row['course_id'])
												})

				# check if there is a lab
				if type(row['lab']) == str:
					# SQL statement to insert into Requirments the lab
					insert_req = "INSERT INTO Requirements (details,type,course_id) VALUES (%(detail)s,%(type)s,%(course)s)"
					cursor.execute(insert_req,{'detail':str(row['lab']),
												'type':"LAB",
												'course':str(row['course_id'])
												})


			########################################################################
			# Faculty table
			########################################################################
			# checks if faculty has already been added or not with check set
			if (row['faculty_first'],row['faculty_last']) not in profs:
				# add faculty to check set, so it wont be added again
				profs.add((row['faculty_first'],row['faculty_last']))

				# SQL statement to insert into Faculty the faculty of the section
				insert_req = "INSERT INTO Faculty (first_initial,last_name) VALUES (%(first)s,%(last)s)"
				cursor.execute(insert_req,{'first':str(row['faculty_first']),
											'last':str(row["faculty_last"])
											})


			########################################################################
			# FacultyAssignments table
			########################################################################
			# SQL statement to find faculty_id from Faculty
			fid_query = "SELECT faculty_id FROM Faculty where first_initial=%(first)s and last_name=%(last)s"
			cursor.execute(fid_query,{'first':str(row['faculty_first']),'last':str(row['faculty_last'])})

			# define faculty id as fid
			for (faculty_id) in cursor:
				fid = int(faculty_id[0])

			# SQL statement to get section id from Sections
			sid_query = "SELECT MAX(section_id) FROM Sections"
			cursor.execute(sid_query)

			# define section id as sid
			for (section_id) in cursor:
				sid = int(section_id[0])

			# SQL statement to insert into FacultyAssignments
			insert_req = "INSERT INTO FacultyAssignments (faculty_id,section_id) VALUES (%(fid)s,%(sid)s)"
			cursor.execute(insert_req,{'fid':str(fid),
										'sid':str(sid)
										})


			########################################################################
			# Buildings table
			########################################################################
			# check if building has already been added to database with check set
			if row['building_abb'] not in buildings:
				# add building to check set so it will not be added again
				buildings.add(row['building_abb'])

				# SQL statement to insert into Buildings
				insert_req = "INSERT INTO Buildings (name,abbreviation) VALUES (%(name)s,%(abb)s)"
				cursor.execute(insert_req,{'name':str(row['building_names']),
											'abb':str(row['building_abb'])
											})



			########################################################################
			# Rooms table
			########################################################################
			# check if room has not already been added
			if (row['building_abb'],row['room']) not in rooms:
				# add room and building to room set to make sure it isn't added again
				rooms.add((row['building_abb'],row['room']))

				# SQL statement to find building id for room
				building_id_query = "SELECT building_id FROM Buildings WHERE abbreviation=%(abb)s"
				cursor.execute(building_id_query,{'abb':str(row['building_abb'])})

				# define building id as bid
				for (bid) in cursor:
					bid = int(bid[0])

				# SQL statement to insert into Rooms
				insert_req = "INSERT INTO Rooms (building_id,number) VALUES (%(bid)s,%(num)s)"
				cursor.execute(insert_req,{'bid':str(bid),
											'num':str(row['room'])
											})


			########################################################################
			# SectionMeetings table
			########################################################################

			# SQL statement to find building id from Buildings
			building_id_query = "SELECT building_id FROM Buildings WHERE abbreviation=%(abb)s"
			cursor.execute(building_id_query,{'abb':str(row['building_abb'])})

			# define building id as bid
			for (bid) in cursor:
				bid = int(bid[0])

			# SQL statement to find room id from Rooms
			rid_query = "SELECT room_id FROM Rooms where building_id=%(bid)s and number=%(room)s"
			cursor.execute(rid_query,{'bid':str(bid),'room':str(row['room'])})

			# define room id as rid
			for (room_id) in cursor:
				rid = int(room_id[0])

			# SQL statement to find the section id
			sid_query = "SELECT MAX(section_id) FROM Sections"
			cursor.execute(sid_query)

			# define section id as sid
			for (section_id) in cursor:
				sid = int(section_id[0])

			# SQL statment to insert in SectionMeetings
			insert_req = "INSERT INTO SectionMeetings (room_id,section_id,start_time,end_time,days) VALUES (%(rid)s,%(sid)s,%(st)s,%(et)s,%(d)s)"
			cursor.execute(insert_req,{'rid':str(rid),
										'sid':str(sid),
										'st':str(row['start_time']),
										'et':str(row['end_time']),
										'd':str(row['days'])
										})




	########################################################################
	# If a problem occurs during database population then the try will fail 
	# and it will go to this expect and print the error message
	########################################################################
	except mysql.connector.Error as error:
		print("Failed to populate the database: {}".format(error))
		exit(1)


##############################################################################
##############################################################################
##############################################################################

# open data.csv file to get data to populate database with
data = pd.DataFrame.from_csv('data.csv', sep=None,index_col=None)

# set up database connection
populate_db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(autocommit = False, **populate_db_properties)
cnx = cnx_pool.get_connection()
cursor = cnx.cursor()

# call database population function defined above
populateDB(cursor, data)

# commit all changes to database, so either all changes are made, or none are
cnx.commit()

# close all connections
cursor.close()
cnx.close()


