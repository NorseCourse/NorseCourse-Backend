import pandas as pd

# read in first csv we are given
courses = pd.DataFrame.from_csv('course.csv', sep=None,index_col=None)

# change all column names to more appropriate ones
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

#read in second csv file we are given
meetings = pd.DataFrame.from_csv('meeting.csv', sep=None,index_col=None)

# change all column names to more appropriate ones
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
meetings['building'] = meetings['Csm Bldg']
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

# merge together the two csv files
data = pd.merge(meetings, courses, how='inner', on=['course_id','section_name','start_date','end_date','section_status'])

# define the different divisions and their included departments
science = ['BIO','CHEM','CS','HLTH','MATH','NURS','PHYS','SCI','ACCTG','BIO','PE','ENVS','ATHTR']
social_science = ['AFRS','COMS', 'ECON', 'IS','EDUC','HIST','POLS','PSYC','SOC','ANTH','SW','GS','WGST','MGT','PHIL','INTS','MUST','JOUR']
humanities = ['CLAS','ENG','REL','RUS','SCST','SPAN','ART','MUS','LING','FREN','GER','LAT','CHIN','GRK','HEB','THE','DAN','PAID','ITAL']

# dictionary of department abbreviation to department name
department_dict = {'BIO':'Biology','CHEM':'Chemistry','CS':'Computer Science','HLTH':'Health','MATH':'Mathematics','NURS':'Nursing','PHYS':'Physics','SCI':'Science','ACCTG':'Accounting','PE':'Physical Education','ENVS':'Enviromental Studies','AFRS':'African Studies','COMS':'Communications', 'ECON':'Economics', 'IS':'Information Systems','EDUC':'Education','HIST':'History','POLS':'Political Science','PSYC':'Psychology','SOC':'Sociology','ANTH':'Anthropology','SW':'Social Work','GS':'Gender Studies','ATHTR':'Atheltic Training','WGST':"Women's Gender Studies",'MGT':'Management','PHIL':'Philosophy','INTS':'International Studies','MUST':'Museam Studies','JOUR':'Journalism','CLAS':'Classics','ENG':'English','REL':'Religion','RUS':'Russian','SCST':'Scandinavian Studies','SPAN':'Spanish','ART':'Art','MUS':'Music','LING':'Linguistics','FREN':'French','GER':'German','LAT':'Latin','CHIN':'Chinese','GRK':'Greek','HEB':'Hebrew','THE':'Theatre','DAN':'Dance','PAID':'Paideia','ITAL':'Italian'}

# dictionary of gen eds abbreviation and gen eds name
gen_eds_dict = {'BL':'Biblical Studies', 'HB': 'Human Behavior', 'HBSSM': 'Human Behavior Social Science Methods', 'HE': 'Human Expression', 'HEPT': 'Human Expression Primary Text', 'HIST': 'Historical', 'INTCL': 'Intercultural','NWL': 'Natural World Lab','NWNL': 'Natural World Non-Lab','QUANT': 'Quantitative','REL': 'Religion','SKL': 'Skills Course','WEL': 'Wellness Course'}
also_geneds = {'HBSSM':'HB','HEPT':'HE','NWL':'NWNL'}


chars = set([' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','_','-','+','=','[',']','{','}','\\','/',';',':',',','.','<','>'])

# initialize list to be new columns
# these are the columns that are missing
# or will need to be edited
divison = []
depts_abb = []
depts_name = []
nums = []
seven_week = []
term = []
start_dates = []
end_dates = []
start_times = []
end_times = []
gen_eds = []
gen_eds_name = []
same_as = []
max_credits = []
also_fulfills = []
comments = []


# iterate through all rows in the csv
for idx,row in data.iterrows():


    if pd.notnull(row['section_comments']):
        new_comment = ""
        comment = list(row['section_comments'])
        for char in comment:
            if char in chars:
                new_comment += char
        comments.append(new_comment)
    else:
        comments.append("")
    

    if pd.isnull(row['max_credits']):
        max_credits.append(0)
    else:
        max_credits.append(row['max_credits'])
    
    same = ""
    if type(row['course_description']) == str:
        find_same = row['course_description'].split("Same as ")
        if len(find_same) > 1:
            same = (find_same[1].replace(")","").replace(' and',',').replace('.',''))
    
    same_as.append(same)
            
    


    # isolate the start and end time of a section with no date
    start_dates.append(row['start_date'].split()[0])
    end_dates.append(row['end_date'].split()[0])
    
    # if there is no start/end time, add a blank string for that value
    # otherwise add the isolated start/end time
    if pd.isnull(row['start_time']):
        start_times.append("")
        end_times.append("")
    else:
        start_times.append((row['start_time'].split()[1])[:-3])
        end_times.append((row['end_time'].split()[1])[:-3])    
    
    # isolate the start/end date with no time
    start = row['meeting_info'].split('-')[0]
    end = row['meeting_info'].split('-')[1].split()[0]
    
    # using the start/end times, define the term
    current_term = 0
    if (start[:2] == '09') or (end[:2] == '12'):
        current_term = "Fall"
        term.append("Fall "+start[6:10]) 
    if (start[:2] == '01'):
        current_term = "J-Term"
        term.append("J-Term "+start[6:10]) 
    if (start[:2] == '02') or (end[:2] == '05'):
        current_term = "Spring"
        term.append("Spring "+start[6:10])     
    
    # define if it is a seven week course or not
    # 0 = no, 1 = first seven weeks, 2 = second seven weeks
    if current_term == "Fall":
        if (start[:2] == '09') and (end[:2] == '12'):
            seven_week.append(0)
        elif (start[:2] == '09'):
            seven_week.append(1)
        else:
            seven_week.append(2)
    elif current_term == "J-Term":
        seven_week.append(0)
    elif current_term == "Spring":
        if (start[:2] == '02') and (end[:2] == '05'):
            seven_week.append(0)
        elif (start[:2] == '02'):
            seven_week.append(1)
        else:
            seven_week.append(2)   
            
    # isolate the course number and add to new column
    num = row['section_name'].split('-')[1]
    nums.append(num)
    
    # isolate the department for the course
    # define which divison it is a part of
    dept = row['section_name'].split('-')[0]
    depts_abb.append(dept)
    depts_name.append(department_dict[dept])    
    if dept in science:
        divison.append("Sciences")
    if dept in social_science:
        divison.append("Social Sciences")
    if dept in humanities:
        divison.append("Humanities")


    # we need to edit the gen ed column
    new_geneds_ab = []
    new_geneds_name = []
    also = []

    # create a gen ed name column and an abbreviation one
    if type(row['gen_eds']) == str:
        geneds = row['gen_eds'].split(',')
        for gened in geneds:
            if gened in gen_eds_dict:
                if gened in also_geneds:
                    also.append(also_geneds[gened]+',')
                new_geneds_ab.append(gened+',')
                new_geneds_name.append(gen_eds_dict[gened]+',')                  
            
    # add list of abb/name of gen eds
    gen_eds.append("".join(new_geneds_ab)[:-1])
    gen_eds_name.append("".join(new_geneds_name)[:-1])
    also_fulfills.append("".join(also)[:-1])



# create new columns in csv with correct values
# deleting any ones we are replacing
data['division'] = divison
data['department_abbreviation'] = depts_abb
data['department_name'] = depts_name
data['course_num'] = nums
data['seven_week'] = seven_week
data['term'] = term

del data['start_date']
data['start_date'] = start_dates
del data['end_date']
data['end_date'] = end_dates

del data['start_time']
data['start_time'] = start_times
del data['end_time']
data['end_time'] = end_times


data['gen_ed_abb'] = gen_eds
data['gen_ed_names'] = gen_eds_name
del data['gen_eds']

data['same_as'] = same_as

del data['max_credits']
data['max_credits']= max_credits

data['also_fulfills'] = also_fulfills

del data['section_comments']
data['section_comments'] = comments

# writing all this data into one good csv
data.to_csv("data.csv")

