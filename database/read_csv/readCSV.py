import pandas as pd

courses = pd.DataFrame.from_csv('course.csv', sep=None,index_col=None)

courses['course_id'] = courses['Course Sections Id']
del courses['Course Sections Id']
courses['section_name'] = courses['Sec Name']
del courses['Sec Name']
courses['section_title'] = courses['Sec Short Title']
del courses['Sec Short Title']
courses['min_credits'] = courses['Sec Min Cred']
del courses['Sec Min Cred']
courses['max_credits'] = courses['Sec Max Cred']
del courses['Sec Max Cred']
courses['faculty_name'] = courses['Faculty First Initial & Last CSV']
del courses['Faculty First Initial & Last CSV']
courses['start_date'] = courses['Sec Start Date']
del courses['Sec Start Date']
courses['end_date'] = courses['Sec End Date']
del courses['Sec End Date']
courses['section_status'] = courses['Sec Status']
del courses['Sec Status']
courses['section_comments'] = courses['Sec Printed Comments']
del courses['Sec Printed Comments']
courses['meeting_info'] = courses['Sec Meeting Info']
del courses['Sec Meeting Info']
courses['course_description'] = courses['Crs Desc']
del courses['Crs Desc']
courses['gen_eds'] = courses['Course Types CSV']
del courses['Course Types CSV']


meetings = pd.DataFrame.from_csv('meeting.csv', sep=None,index_col=None)

meetings['course_id'] = meetings['Course Sections Id']
del meetings['Course Sections Id']
meetings['section_name'] = meetings['Sec Name']
del meetings['Sec Name']
meetings['meeting_id'] = meetings['Course Sec Meeting Id']
del meetings['Course Sec Meeting Id']
meetings['start_date'] = meetings['Csm Start Date']
del meetings['Csm Start Date']
meetings['end_date'] = meetings['Csm End Date']
del meetings['Csm End Date']
meetings['bulding'] = meetings['Csm Bldg']
del meetings['Csm Bldg']
meetings['room'] = meetings['Csm Room']
del meetings['Csm Room']
meetings['start_time'] = meetings['Csm Start Time']
del meetings['Csm Start Time']
meetings['end_time'] = meetings['Csm End Time']
del meetings['Csm End Time']
meetings['monday'] = meetings['Csm Monday']
del meetings['Csm Monday']
meetings['tuesday'] = meetings['Csm Tuesday']
del meetings['Csm Tuesday']
meetings['wednesday'] = meetings['Csm Wednesday']
del meetings['Csm Wednesday']
meetings['thursday'] = meetings['Csm Thursday']
del meetings['Csm Thursday']
meetings['friday'] = meetings['Csm Friday']
del meetings['Csm Friday']
meetings['saturday'] = meetings['Csm Saturday']
del meetings['Csm Saturday']
meetings['sunday'] = meetings['Csm Sunday']
del meetings['Csm Sunday']
meetings['frequency'] = meetings['Csm Frequency']
del meetings['Csm Frequency']
meetings['section_status'] = meetings['Sec Status']
del meetings['Sec Status']
meetings['days'] = meetings['Csm Days']
del meetings['Csm Days']


science = ['BIO','CHEM','CS','HLTH','MATH','NURS','PHYS','SCI','ACCTG','BIO','PE','ENVS']
social_science = ['AFRS','COMS', 'ECON', 'IS','EDUC','HIST','POLS','PSYC','SOC','ANTH','SW','GS','ATHTR','WGST','MGT','PHIL','INTS','MUST','JOUR']
humanities = ['CLAS','ENG','REL','RUS','SCST','SPAN','ART','MUS','LING','FREN','GER','LAT','CHIN','GRK','HEB','THE','DAN','PAID','ITAL']

divison = []
depts_abb = []

for idx,row in courses.iterrows():
    dept = row['section_name'].split('-')[0]
    if dept in science:
        divison.append("science")
        depts_abb.append(dept)
    if dept in social_science:
        divison.append("social_science")
        depts_abb.append(dept)
    if dept in humanities:
        divison.append("humanities")
        depts_abb.append(dept)

courses['divison'] = divison
courses['department_abbreviation'] = depts_abb
print(courses.head(20))


