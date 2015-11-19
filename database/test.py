import mysql.connector
import mysql.connector.pooling

import config


populate_db_properties = config.db_pool_config
cnx_pool = mysql.connector.pooling.MySQLConnectionPool(autocommit = False, **populate_db_properties)
cnx = cnx_pool.get_connection()
cursor = cnx.cursor()

req_geneds = ["HE","HB","QUANT"]
best = [106,118,800,463]
possible_gened_classes = {}
for gened in range(len(req_geneds)):

	classQuery = "SELECT section_id from GenEdFulfillments, GenEds where (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and abbreviation = %s) or (GenEds.gen_ed_id = GenEdFulfillments.gen_ed_id and also_fulfills = %s)"

	cnx = cnx_pool.get_connection()
	cursor = cnx.cursor()

	cursor.execute(classQuery % (str("'"+req_geneds[gened]+"'"),str("'"+req_geneds[gened]+"'")))

	classes = []
	for (section_id) in cursor:
		classes.append(section_id[0])

	possible_gened_classes[req_geneds[gened]] = classes

	cursor.close()
	cnx.close()

print possible_gened_classes

doubles = {}
keys = []

for ge in possible_gened_classes:
	for ge2 in possible_gened_classes:
		if ge != ge2:
			for class1 in possible_gened_classes[ge]:
				for class2 in possible_gened_classes[ge2]:
					if class1 == class2:
						key = ge+" "+ge2
						if key in doubles:
							doubles[key].append(class1)
						else:
							doubles[key] = [class1] 


print doubles

keys = []
for key in doubles:
	one,two = key.split()
	new = set((one,two))
	if new not in keys:
		keys.append(new)

print keys

for k in keys:
	delKey = list(k)[0] + " " + list(k)[1]
	del doubles[delKey]

print
print doubles




