import mysql.connector
import config


def createDB(cursor):
	try:
		cursor.execute("CREATE DATABASE TestNC2")

	except mysql.connector.Error as error:
		print("Failed to create the database: {}".format(error))
		exit(1)


def createTables(cursor):
	try:
		cursor.execute("USE TestNC2")
		cursor.execute("CREATE TABLE Divisions (division_id INT AUTO_INCREMENT, name VARCHAR(20) NOT NULL, PRIMARY KEY (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Departments (department_id INT AUTO_INCREMENT, abbreviation VARCHAR(10) NOT NULL, name VARCHAR(20) NOT NULL, division_id INT, PRIMARY KEY (department_id), FOREIGN KEY (division_id) REFERENCES Divisions (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Courses (course_id INT AUTO_INCREMENT, description VARCHAR(1000), same_as VARCHAR(20), number VARCHAR(10) NOT NULL, department_id INT, PRIMARY KEY (course_id), FOREIGN KEY (department_id) REFERENCES Departments (department_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Sections (section_id INT, term VARCHAR(2) CHECK (term IN ('FA', 'JT', 'SP', 'S1', 'S2')), name VARCHAR(20) NOT NULL, short_title VARCHAR(20) NOT NULL, min_credits INT NOT NULL, max_credits INT, comments VARCHAR(500), seven_weeks TINYINT NOT NULL CHECK (seven_weeks >= 0 AND seven_weeks <= 2), course_id INT, PRIMARY KEY (section_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Requirements (requirements_id INT AUTO_INCREMENT, type VARCHAR(3) CHECK (type IN ('CO', 'PRE', 'LAB')), target_course_id INT, req_course_id INT, PRIMARY KEY (requirements_id), FOREIGN KEY (target_course_id) REFERENCES Courses (course_id), FOREIGN KEY (req_course_id) REFERENCES Courses (course_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE GenEds (gen_ed_id INT AUTO_INCREMENT, name VARCHAR(50) NOT NULL, abbreviation VARCHAR(10) NOT NULL, also_fulfills VARCHAR(50), PRIMARY KEY (gen_ed_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE GenEdFulfillments (gen_ed_id INT AUTO_INCREMENT, course_id INT, comments VARCHAR(200), PRIMARY KEY (gen_ed_id, course_id), FOREIGN KEY (gen_ed_id) REFERENCES GenEds (gen_ed_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Recommendations (recommendation_id INT AUTO_INCREMENT, course_id INT, division_id INT, PRIMARY KEY (recommendation_id), FOREIGN KEY (course_id) REFERENCES Courses (course_id), FOREIGN KEY (division_id) REFERENCES Divisions (division_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Faculty (faculty_id INT AUTO_INCREMENT, first_initial CHAR(1) NOT NULL, last_name VARCHAR(20) NOT NULL, PRIMARY KEY (faculty_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Buildings (building_id INT AUTO_INCREMENT, name VARCHAR(50) NOT NULL, abbreviation VARCHAR(10) NOT NULL, PRIMARY KEY (building_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE Rooms (room_id INT AUTO_INCREMENT, building_id INT, number VARCHAR(10) NOT NULL, PRIMARY KEY (room_id), FOREIGN KEY (building_id) REFERENCES Buildings (building_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE SectionMeetings (room_id INT, section_id INT, start_time TIME NOT NULL, end_time TIME NOT NULL, days VARCHAR(5) NOT NULL, PRIMARY KEY (room_id, section_id), FOREIGN KEY (room_id) REFERENCES Rooms (room_id), FOREIGN KEY (section_id) REFERENCES Sections (section_id)) ENGINE = INNODB;")
		cursor.execute("CREATE TABLE FacultyAssignments (faculty_id INT AUTO_INCREMENT, section_id INT, PRIMARY KEY (faculty_id, section_id), FOREIGN KEY (faculty_id) REFERENCES Faculty (faculty_id), FOREIGN KEY (section_id) REFERENCES Sections (section_id)) ENGINE = INNODB;")

	except mysql.connector.Error as error:
		print("Failed to create the tables: {}".format(error))
		exit(1)


cnx_properties = config.db_cnx_config
cnx = mysql.connector.connect(autocommit = False, **cnx_properties)
cursor = cnx.cursor()

createDB(cursor)
createTables(cursor)

cursor.close()
cnx.close()










