import mysql.connector
import mysql.connector.pooling

import config

import pandas as pd


def populateDB(cursor, data):
	try:

		divisions = set()
		departments = set()
		courses = set()

		for idx,row in data.iterrows():
			if row['division'] not in divisions:
				divisions.add(row['division'])
				insert_division = "INSERT INTO Divisions (name) VALUES (%(name)s)"
				cursor.execute(insert_division, {"name": str(row['division'])})


		for idx,row in data.iterrows():
			if row['department_name'] not in departments:

				departments.add(row['department_name'])

				div_id_query = "SELECT division_id FROM Divisions WHERE name = %(name)s"
				cursor.execute(div_id_query,{'name':str(row['division'])})

				for (division_id) in cursor:
					div_id = int(division_id[0])


				insert_department = "INSERT INTO Departments (name,abbreviation,division_id) VALUES (%(name)s,%(abb)s,%(d_id)s)"
				cursor.execute(insert_department, {"name": str(row['department_name']),"abb": str(row['department_abbreviation']),"d_id": str(div_id)})
	


		t = 0
		for idx,row in data.iterrows():
			print(t)
			t+=1

			dept_id_query = "SELECT department_id FROM Departments WHERE name = %(name)s"
			cursor.execute(dept_id_query,{'name':str(row['department_name'])})

			for (department_id) in cursor:
				dept_id = int(department_id[0])


			insert_course = "INSERT INTO Courses (description,same_as,number,department_id) VALUES (%(desc)s,%(same_as)s,%(number)s,%(dept_id)s)"
			cursor.execute(insert_course,{'desc':str(row['course_description']),
											'same_as':str(row['same_as']),
											'number':str(row['section_name']),
											'dept_id':str(dept_id)
											})



		t = 0
		for idx,row in data.iterrows():

			print(t)
			t+=1

			course_num_query = "SELECT course_id FROM Courses WHERE number = %(num)s"
			cursor.execute(course_num_query,{'num':str(row['section_name'])})

			for (course_id) in cursor:
				course_id = int(course_id[0])


			insert_course = "INSERT INTO Sections (section_id,term,name,short_title,min_credits,max_credits,comments,seven_weeks,course_id) VALUES (%(sId)s,%(term)s,%(name)s,%(short_title)s,%(min_credits)s,%(max_credits)s,%(comments)s,%(seven_weeks)s,%(course_id)s)"
			cursor.execute(insert_course,{'sId':str(row['course_id']),
											'term':str(row['term']),
											'name':str(row['section_name']),
											'short_title':str(row['section_title']),
											'min_credits':str(row['min_credits']),
											'max_credits':str(row['max_credits']),
											'comments':str(row['course_description']),
											'seven_weeks':str(row['seven_week']),
											'course_id':str(course_id)
											})


		# change course to non auto increment, and section to auto 



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










