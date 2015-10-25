# Import the needed packages
import mysql.connector
import mysql.connector.pooling

import config

db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**db_properties)

cnx = cnx_pool.get_connection()
cursor = cnx.cursor()

termQuery = "SELECT DISTINCT name FROM Divisions"
cursor.execute(termQuery)

for name in cursor:
	print(name[0])

cursor.close()
cnx.close()