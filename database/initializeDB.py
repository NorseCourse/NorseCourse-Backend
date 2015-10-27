# Import needed packakes.
import mysql.connector
import re

import config


# Function to creater a databaes based on the name that is passed in.
def createDB(cnx, cursor, db_name):
	try:
		cursor.execute("CREATE DATABASE {}".format(db_name))
		cnx.commit()

	except mysql.connector.Error as error:
		print("Failed to create the database: {}".format(error))
		exit(1)


# Function to create the tables needed to run NorseCourse.
def createTables(cnx, cursor, db_name):
	try:
		cursor.execute("USE {}".format(db_name))
		cursor.execute("CREATE TABLE Divisions (division_id INT AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Departments (department_id INT AUTO_INCREMENT, abbreviation VARCHAR(10) NOT NULL, name VARCHAR(50) NOT NULL, division_id INT, PRIMARY KEY (department_id), FOREIGN KEY (division_id) REFERENCES Divisions (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Courses (course_id INT, description VARCHAR(10000), same_as VARCHAR(50), number VARCHAR(50) NOT NULL,name VARCHAR(50) NOT NULL, department_id INT, PRIMARY KEY (course_id), FOREIGN KEY (department_id) REFERENCES Departments (department_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Sections (section_id INT AUTO_INCREMENT, term VARCHAR(20) CHECK (term IN ('FA', 'JT', 'SP', 'S1', 'S2')), name VARCHAR(50) NOT NULL, short_title VARCHAR(100) NOT NULL, min_credits INT NOT NULL, max_credits INT, comments VARCHAR(10000), seven_weeks TINYINT NOT NULL CHECK (seven_weeks >= 0 AND seven_weeks <= 2), course_id INT, PRIMARY KEY (section_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Requirements (requirements_id INT AUTO_INCREMENT, details VARCHAR(200), req_type VARCHAR(3) CHECK (req_type IN ('CO', 'PRE', 'LAB')), course_id INT, PRIMARY KEY (requirements_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE GenEds (gen_ed_id INT AUTO_INCREMENT, name VARCHAR(200) NOT NULL, abbreviation VARCHAR(100) NOT NULL, also_fulfills VARCHAR(50), PRIMARY KEY (gen_ed_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE GenEdFulfillments (gen_ed_id INT AUTO_INCREMENT, section_id INT, comments VARCHAR(200), PRIMARY KEY (gen_ed_id, section_id), FOREIGN KEY (gen_ed_id) REFERENCES GenEds (gen_ed_id), FOREIGN KEY (section_id) REFERENCES Sections (section_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Recommendations (recommendation_id INT AUTO_INCREMENT, course_id INT, division_id INT, PRIMARY KEY (recommendation_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id), FOREIGN KEY (division_id) REFERENCES Divisions (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Faculty (faculty_id INT AUTO_INCREMENT, first_initial VARCHAR(50) NOT NULL, last_name VARCHAR(300) NOT NULL, PRIMARY KEY (faculty_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Buildings (building_id INT AUTO_INCREMENT, name VARCHAR(50) NOT NULL, abbreviation VARCHAR(10) NOT NULL, PRIMARY KEY (building_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Rooms (room_id INT AUTO_INCREMENT, building_id INT, number VARCHAR(10) NOT NULL, PRIMARY KEY (room_id), FOREIGN KEY (building_id) REFERENCES Buildings (building_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE SectionMeetings (room_id INT, section_id INT, start_time VARCHAR(10) NOT NULL, end_time VARCHAR(10) NOT NULL, days VARCHAR(5) NOT NULL, PRIMARY KEY (room_id, section_id), FOREIGN KEY (room_id) REFERENCES Rooms (room_id), FOREIGN KEY (section_id) REFERENCES Sections (section_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE FacultyAssignments (faculty_id INT AUTO_INCREMENT, section_id INT, PRIMARY KEY (faculty_id, section_id), FOREIGN KEY (faculty_id) REFERENCES Faculty (faculty_id), FOREIGN KEY (section_id) REFERENCES Sections (section_id)) ENGINE = INNODB;")
		cnx.commit()

	except mysql.connector.Error as error:
		print("Failed to create the tables: {}".format(error))
		exit(1)


# Grab the appropriate conection configuration from the congig file.
# Set autocommit to false so we can ensure that either all or none of the SQL statements execute.
# In this case we do not need a connection pool, thus we simply create one connection and a cursor to pass into our functions.
init_db_properties = config.init_db_config
cnx = mysql.connector.connect(autocommit = False, **init_db_properties)
cursor = cnx.cursor()

# Ask the user what the database name should be on their system, this is case sensitive.
# By default, we this file is written to give the database the name of NorseCourse if nothind is entered.
db_name = str(raw_input("Enter a name for the new database (case sensitive), or return for default (NorseCourse): "))
create_db = True

# Setting the defaule if a database name is not provided.
# Adding validation to generate a error if the name provided does not comply with the rules for how a database can be named.
if db_name == "":
	db_name = "NorseCourse"
else:
	if re.match(r"[A-Za-z0-9$_]", db_name):
		print("Since you did not use the defalt database name, be sure to change the database proberty under db_pool_config in the config.py file in order for your installation to run correctly")
	else:
		create_db = False
		print("You have entered and invalid database name")

# If requirements are met then create the datase and the tables.
if create_db:
	createDB(cnx, cursor, db_name)
	createTables(cnx, cursor, db_name)

#Close the cursor and connection.
cursor.close()
cnx.close()










