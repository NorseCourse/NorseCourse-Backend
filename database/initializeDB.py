# Import packages.
import config
import mysql.connector
import re

# Create database based on name passed in, or default the 
# default value which is set as NorseCourse below.
def createDB(cnx, cursor, db_name):
	try:
		cursor.execute("CREATE DATABASE {}".format(db_name))
		cnx.commit()

	except mysql.connector.Error as error:
		print("Failed to create the database: {}".format(error))
		exit(1)


# Create the tables needed to run the NorseCourse site.
def createTables(cnx, cursor, db_name):
	try:
		cursor.execute("USE {}".format(db_name))
		cursor.execute("CREATE TABLE Divisions (division_id INT AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Departments (department_id INT AUTO_INCREMENT, abbreviation VARCHAR(10) NOT NULL, name VARCHAR(50) NOT NULL, division_id INT, PRIMARY KEY (department_id), FOREIGN KEY (division_id) REFERENCES Divisions (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Courses (course_id INT, description VARCHAR(10000), same_as VARCHAR(200), number VARCHAR(50) NOT NULL,name VARCHAR(50) NOT NULL, department_id INT, PRIMARY KEY (course_id), FOREIGN KEY (department_id) REFERENCES Departments (department_id)) ENGINE = INNODB;")
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


# Grab appropriate conection configuration from config file.
# Set autocommit to false, ensuring that either all or none of the SQL statements execute.
# In this case a connection pool is not needed, thus we simply create one connection
# and cursor to pass into our functions.
init_db_properties = config.init_db_config
cnx = mysql.connector.connect(autocommit = False, **init_db_properties)
cursor = cnx.cursor()

# Ask the user what the database name should be on their system, this is case sensitive.
# By default, this script is written to give the database a name of NorseCourse if nothind is entered.
db_name = str(input("Enter the name of the database you created earlier (We recommended NorseCourse): "))


# If requirements are met then create datase and tables.
createDB(cnx, cursor, db_name)
createTables(cnx, cursor, db_name)

#Close the cursor and connection.
cursor.close()
cnx.close()