import mysql.connector
import mysql.connector.pooling

import config

import pandas as pd


def populateDB(cursor, data):
	try:

		divisions = set()
		departments = set()
		courses = set()
		gen_eds = set()

		for idx,row in data.iterrows():
			if row['division'] not in divisions:
				divisions.add(row['division'])
				insert_division = "INSERT INTO Divisions (name) VALUES (%(name)s)"
				cursor.execute(insert_division, {"name": str(row['division'])})

		print('Divisions Table done')

		for idx,row in data.iterrows():
			if row['department_name'] not in departments:

				departments.add(row['department_name'])

				div_id_query = "SELECT division_id FROM Divisions WHERE name = %(name)s"
				cursor.execute(div_id_query,{'name':str(row['division'])})

				for (division_id) in cursor:
					div_id = int(division_id[0])

				insert_department = "INSERT INTO Departments (name,abbreviation,division_id) VALUES (%(name)s,%(abb)s,%(d_id)s)"
				cursor.execute(insert_department, {"name": str(row['department_name']),"abb": str(row['department_abbreviation']),"d_id": str(div_id)})
	
		print('Departments Table done')


		for idx,row in data.iterrows():

			if row['course_id'] not in courses:

				courses.add(row['course_id'])

				dept_id_query = "SELECT department_id FROM Departments WHERE name = %(name)s"
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

		print('Courses Table done')

		for idx,row in data.iterrows():

			course_num_query = "SELECT course_id FROM Courses WHERE number = %(num)s"
			cursor.execute(course_num_query,{'num':str(row['section_name'])})

			for (course_id) in cursor:
				course_id = int(course_id[0])

			insert_course = "INSERT INTO Sections (term,name,short_title,min_credits,max_credits,comments,seven_weeks,course_id) VALUES (%(term)s,%(name)s,%(short_title)s,%(min_credits)s,%(max_credits)s,%(comments)s,%(seven_weeks)s,%(course_id)s)"
			cursor.execute(insert_course,{'term':str(row['term']),
											'name':str(row['section_name']),
											'short_title':str(row['section_title']),
											'min_credits':str(row['min_credits']),
											'max_credits':str(row['max_credits']),
											'comments':str(row['course_description']),
											'seven_weeks':str(row['seven_week']),
											'course_id':str(course_id)
											})

		print('Sections Table done')

		gen_eds_dict = {'BL':'Biblical Studies', 'HB': 'Human Behavior', 'HBSSM': 'Human Behavior Social Science Methods', 'HE': 'Human Expression', 'HEPT': 'Human Expression Primary Text', 'HIST': 'Historical', 'INTCL': 'Intercultural','NWL': 'Natural World Lab','NWNL': 'Natural World Non-Lab','QUANT': 'Quantitative','REL': 'Religion','SKL': 'Skills Course','WEL': 'Wellness Course'}
		also_geneds = {'HBSSM':'HB','HEPT':'HE','NWL':'NWNL','BL':'', 'HB': '', 'HE': '', 'HIST': '', 'INTCL': '','NWNL': '','QUANT': '','REL': '','SKL': '','WEL': ''}

		for idx,row in data.iterrows():

			if type(row['gen_ed_abb']) == str:
				geneds = row['gen_ed_abb'].split(',')

				for ge in geneds:
					print(ge)
					if ge not in gen_eds:

						gen_eds.add(ge)

						insert_course = "INSERT INTO GenEds (name,abbreviation,also_fulfills) VALUES (%(name)s,%(abb)s,%(also)s)"
						cursor.execute(insert_course,{'name':str(gen_eds_dict[ge]),
														'abb':str(ge),
														'also':str(also_geneds[ge])
														})

		print('GenEds Table done')


		for idx,row in data.iterrows():
			if type(row['gen_ed_abb']) == str:
				geneds = row['gen_ed_abb'].split(',')
		        for gened in geneds:


		        	course_num_query = "SELECT course_id FROM Courses WHERE number = %(num)s"
		        	cursor.execute(course_num_query,{'num':str(row['section_name'])})

		        	for (course_id) in cursor:
		        		course_id = int(course_id[0])

		        	gened_id_query = "SELECT gen_ed_id FROM GenEds WHERE abbreviation = %(abb)s"
		        	cursor.execute(gened_id_query,{'abb':str(gened)})

		        	for (gid) in cursor:
		        		gened_id = int(gid[0])

		        	insert_course = "INSERT INTO GenEdFulfillment (gen_ed_id,course_id) VALUES (%(gid)s,%(cid)s)"
		        	cursor.execute(insert_course,{'gid':str(gened_id),
													'cid':str(course_id)
													})

		print("GenEdFulfillments Table done")



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










