
##############################################################################
# The purpose of this file is to take the two csv files given to us, and 
# create one more useable csv from them.  It creates a csv that has all the 
# information we want in one easier to use file so it will make populating
# the database easier.

# We can then run populateDB.py to use this created csv to populate our database
##############################################################################

import pandas as pd
import re


def main():

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
    meetings['building_abb'] = meetings['Csm Bldg']
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


    course_ids = {}
    cid = 0
    for idx,row in courses.iterrows():
        name = row['section_name'].split("-")[0]+"-"+row['section_name'].split("-")[1]
        if name not in course_ids:
            course_ids[name] = cid
            cid += 1


    for idx,row in meetings.iterrows():
        name = row['section_name'].split("-")[0]+"-"+row['section_name'].split("-")[1]
        if name not in course_ids:
            course_ids[name] = cid
            cid += 1


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
    # defines gen eds that also cover others
    also_geneds = {'HBSSM':'HB','HEPT':'HE','NWL':'NWNL'}

    # Define building name locations
    buildings_dict = {'GJER':"Gjerset House", 'CMPH':"Campus House", 'CART':"Center for the Arts", 'LARS':"Larson Hall",'ROCH':"Rock House",'REGE':"Regents Center", 'STOR':"Storre Theatre", 'LOYA':"Loyalty Hall", 'SAMP':"Sampson Hoffland Laboratories", 'KORE':"Koren", 'ARR':"To be Announced", 'VALD':"Valders Hall of Science", 'JENS':"Jenson-Noble Hall of Music", 'OCKH':"Ockham House", 'PREU':"Preus Library", 'OLIN':"Olin", 'MAIN':"Main Building"}

    # define acceptable characters in the comments for sections
    chars = set([' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','!','@','#','$','%','^','&','*','(',')','_','-','+','=','[',']','{','}','\\','/',';',':',',','.','<','>'])

    # initialize list to be new columns
    # these are the columns that are missing
    # or will need to be edited
    # in the new csv file
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
    pre_reqs = []
    co_reqs = []
    lab = []
    faculty_first = []
    faculty_last = []
    building_names = []
    course_id = []


    # iterate through all rows in the csv
    # making the necessary changes
    for idx,row in data.iterrows():

        ########################################################################
        # add course id to column of course_id
        ########################################################################

        name = row['section_name'].split("-")[0]+"-"+row['section_name'].split("-")[1]
        course_id.append(course_ids[name])



        ########################################################################
        # add building name to column of building_names
        ########################################################################
        building_names.append(buildings_dict[row['building_abb']])



        ########################################################################
        # set up facutly first initial and last name
        ########################################################################
        # if there is more than one professor listed
        if len(row['faculty_name'].split(','))>1:
            # create list of all professors teaching course
            profs = row['faculty_name'].split(',')
            lasts = []
            firsts = []
            # create list of first initials and last names of all professors
            for prof in profs:
                firsts.append(prof.split('.')[0]+", ")
                lasts.append(prof.split('.')[1]+", ")

            # add list of all first and last to specified columns
            faculty_first.append("".join(firsts)[:-2])
            faculty_last.append("".join(lasts)[:-2])

        # there is only one professor
        else:
            # add first and last name to column
            faculty_first.append(row['faculty_name'].split('.')[0])
            faculty_last.append(row['faculty_name'].split('.')[1])




        ########################################################################
        # add pre req column
        ########################################################################
        # check if there is a course description
        if pd.notnull(row['course_description']):

            # use regular expression to find pre req in course_description
            req = re.split(r'[P/p]re-?[R/r]equisites?:?',row['course_description'])

            # if no pre req was found, look for different match
            if len(req) == 1:
                # looks for pre req instead of pre requisite
                req = re.split(r'[P/p]re-?[R/r]eqs?:?',row['course_description'])

                # check if a pre req was found, if not it enters if statment and looks in comment sections
                if len(req) == 1:
                    #checks that there is a section comment
                    if pd.notnull(row['section_comments']):
                        req = re.split(r'[P/p]o-?[R/r]equisites?:?',row['section_comments'])

                        # once again checks if pre req was found, enters if when none is found
                        if len(req) == 1:
                            req = re.split(r'[P/p]re-?[R/r]eqs?:?',row['section_comments'])

            # checks if there was a pre req, enters if when there is a pre req
            if len(req)>1:
                # adds pre req to column
                req = req[1].split('.')
                req = req[0].replace('uisite:',"").replace(':',"")
                pre_reqs.append(req)

            # no pre req found
            else:
                # adds empty string in pre req column
                pre_reqs.append("")

        # there was no course description
        else:
            #checks that there is a section comment
            if pd.notnull(row['section_comments']):
                req = re.split(r'[P/p]o-?[R/r]equisites?:?',row['section_comments'])

                # once again checks if pre req was found, enters if when none is found
                if len(req) == 1:
                    req = re.split(r'[P/p]re-?[R/r]eqs?:?',row['section_comments'])

                # checks if there was a pre req, enters if when there is a pre req
                if len(req)>1:
                    # adds pre req to column
                    req = req[1].split('.')
                    req = req[0].replace('uisite:',"").replace(':',"")
                    pre_reqs.append(req)
                # if no pre req found
                else:
                    # adds empty string to pre req
                    pre_reqs.append("")

            # there was no comment section or course description
            else:
                # adds empty string to pre req
                pre_reqs.append("")





        ########################################################################
        # add co req column
        ########################################################################
        # checks if there is a section comment
        if pd.notnull(row['section_comments']):

            # use regular expression to find co req in section comments
            req = re.split(r'[C/c]o-?[R/r]equisites?:?',row['section_comments'])

            # if no co req was found, look for different match
            if len(req) == 1:

                # looks for co req instead of co requisite in sectin comments
                req = re.split(r'[C/c]o-?[R/r]eqs?:?',row['section_comments'])

                # if no co req found, looks in course description
                if len(req) == 1:

                    #checks if there is a course description
                    if pd.notnull(row['course_description']):

                        # uses regular expression to look
                        req = re.split(r'[C/c]o-?[R/r]equisites?:?',row['course_description'])

                        # if no co req found
                        if len(req) == 1:

                            # look for co req instead of co requisite
                            req = re.split(r'[C/c]o-?[R/r]eqs?:?',row['course_description'])

            # if co req found
            if len(req)>1:

                # add co req to column
                req = req[1].split('.')
                req = req[0].replace('uisite:',"").replace(':',"")
                co_reqs.append(req)

            # no co req found
            else:
                # add empty string to colunm
                co_reqs.append("")

        # if no section comment
        else:
            #checks if there is a course description
            if pd.notnull(row['course_description']):

                # uses regular expression to look
                req = re.split(r'[C/c]o-?[R/r]equisites?:?',row['course_description'])

                # if no co req found
                if len(req) == 1:

                    # look for co req instead of co requisite
                    req = re.split(r'[C/c]o-?[R/r]eqs?:?',row['course_description'])

                # if co req found
                if len(req)>1:
                    # add co req to column
                    req = req[1].split('.')
                    req = req[0].replace('uisite:',"").replace(':',"")
                    co_reqs.append(req)
                # no co req found
                else:
                    # append empty string to column
                    co_reqs.append("")
            # if no course description
            else:
                # append empty string to column
                co_reqs.append("")





        ########################################################################
        # check for lab
        ########################################################################

        if row['section_name'].split('-')[1][-1] != "L":
            lab_name = row['section_name'].split('-')[0]+"-"+row['section_name'].split('-')[1]+"L"
            labs = []
            for c in data['section_name']:
                temp = c.split('-')[0]+"-"+c.split('-')[1]
                if temp == lab_name:
                    labs.append(c)
                    
            # add course to lab column
            if len(labs)>0:
                lab.append(labs)
            else:
                lab.append("")
        # not a lab
        else:
            # add empty string to lab column
            lab.append("")




        ########################################################################
        # check for section comments
        ########################################################################
        # if section comment
        if pd.notnull(row['section_comments']):
            # remove all unwanted characters from comment
            new_comment = ""
            comment = list(row['section_comments'])
            for char in comment:
                if char in chars:
                    new_comment += char
            # add comment to comment column
            comments.append(new_comment)
        # no comments found
        else:
            # add empty string to comment column
            comments.append("")
        



        ########################################################################
        # check for lab
        ########################################################################
        # if L in section name
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
                
        


        ########################################################################
        # isolate the start and end dates of a section with no times
        ########################################################################
        start_dates.append(row['start_date'].split()[0])
        end_dates.append(row['end_date'].split()[0])
        
        

        ########################################################################
        # isolate the start and end times of a section with no dates
        ########################################################################
        # if there is no start/end time, add a blank string for that value
        # otherwise add the isolated start/end time
        if pd.isnull(row['start_time']):
            start_times.append("NA")
            end_times.append("NA")
        else:
            start_times.append((row['start_time'].split()[1])[:-3])
            end_times.append((row['end_time'].split()[1])[:-3])    
        


        ########################################################################
        # define term of course
        ########################################################################
        # get start and end date
        start = row['meeting_info'].split('-')[0]
        end = row['meeting_info'].split('-')[1].split()[0]
        
        # using the start/end times, define the term
        current_term = 0
        # if starts in september or ends in december, its fall
        if (start[:2] == '09') or (end[:2] == '12'):
            current_term = "Fall"
            # make the term Fall (year)
            term.append("Fall "+start[6:10]) 
        # if starts in jan, its JTerm
        if (start[:2] == '01'):
            current_term = "J-Term"
            term.append("J-Term "+start[6:10]) 
        # if starts in feb or ends in may, its spring
        if (start[:2] == '02') or (end[:2] == '05'):
            current_term = "Spring"
            term.append("Spring "+start[6:10])     
        


        ########################################################################
        # define seven week of course
        ########################################################################
        # 0 = no, 1 = first seven weeks, 2 = second seven weeks

        # if term is Fall
        if current_term == "Fall":
            # if full semester, it is neither seven weeks
            if (start[:2] == '09') and (end[:2] == '12'):
                seven_week.append(0)
            # starts in 9, but does not end in 12, its a first seven weeks
            elif (start[:2] == '09'):
                seven_week.append(1)
            # second seven weeks
            else:
                seven_week.append(2)

        # if term is JTerm
        elif current_term == "J-Term":
            # all jterms are not seven week courses
            seven_week.append(0)

        # if spring term
        elif current_term == "Spring":
            # if full semester, its not seven week course
            if (start[:2] == '02') and (end[:2] == '05'):
                seven_week.append(0)
            # if it starts 2, and does not end in 5, its a first seven week
            elif (start[:2] == '02'):
                seven_week.append(1)
            # it is a second seven week course
            else:
                seven_week.append(2)   
                


        ########################################################################
        # isolate the course number and add to new column
        ########################################################################
        num = row['section_name'].split('-')[1]
        nums.append(num)



        ########################################################################
        # isolate the department for the course
        ########################################################################    
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



        ########################################################################
        # edit gen ed column to two new columns, name and abbreviation
        ########################################################################
        new_geneds_ab = []
        new_geneds_name = []
        also = []

        # create a gen ed name column and an abbreviation one

        # if there are gen eds
        if type(row['gen_eds']) == str:
            # create list of all gen eds
            geneds = row['gen_eds'].split(',')
            # iterate through all gen eds
            for gened in geneds:
                # checks if it is a valid gen ed
                if gened in gen_eds_dict:

                    # check if it is a gen ed that covers another gen ed
                    if gened in also_geneds:
                        also.append(also_geneds[gened]+',')

                    # creates temp list of gen ed names and abbrevation
                    new_geneds_ab.append(gened+',')
                    new_geneds_name.append(gen_eds_dict[gened]+',')                  
                
        # add list of abb/name of gen eds to column
        gen_eds.append("".join(new_geneds_ab)[:-1])
        gen_eds_name.append("".join(new_geneds_name)[:-1])
        # add list of also fulfills to column
        also_fulfills.append("".join(also)[:-1])

    ########################################################################
    ########################################################################
    # end of going through csv
    ########################################################################
    ########################################################################


    ########################################################################
    # create new columns in csv with correct values
    # deleting any ones we are replacing
    ########################################################################

    data['building_names'] = building_names
    data['faculty_first'] = faculty_first
    data['faculty_last'] = faculty_last
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
    data['pre_reqs'] = pre_reqs
    data['co_reqs'] = co_reqs
    data['lab'] = lab
    data['c_id'] = course_id

    ########################################################################
    # writing all this data into one csv called data.csv
    ########################################################################
    data.to_csv("data.csv")


if __name__ == '__main__':
    main()




