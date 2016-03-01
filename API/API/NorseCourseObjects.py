# What a department object should contain
class DepartmentObject(object):
	def __init__(self, abbreviation = None, name = None, department_id = None, division_id = None):
		self.abbreviation = abbreviation
		self.name = name
		self.departmentId = department_id
		self.divisionId = division_id

# What a division object should contain
class DivisionObject(object):
	def __init__(self, name = None, division_id = None):
		self.name = name
		self.divisionId = division_id

# What a gen ed object should contain
class GenEdObject(object):
	def __init__(self, gen_ed_id = None, name = None, abbreviation = None, also_fulfills = None):
		self.genEdId = gen_ed_id
		self.name = name
		self.abbreviation = abbreviation
		self.alsoFulfills = also_fulfills

# What a course object should contain
class CourseObject(object):
	def __init__(self, title = None, course_id = None, description = None, same_as = None, name = None, department_id = None, relevance = None, requirements = None, recommendations = None):
		self.title = title
		self.courseId = course_id
		self.description = description
		self.sameAs = same_as
		self.name = name
		self.departmentId = department_id
		self.relevance = relevance					#Some number based on a keyword search
		self.requirements = requirements			#This will be a requirements object
		self.recommendations = recommendations		#This will be a relevance object

# What a requirement object should contain
class RequirementObject(object):
	def __init__(self, req_type = None, details = None):
		self.reqType = req_type
		self.details = details

# What a section object should contain
class SectionObject(object):
	def __init__(self, term = None, name = None, short_title= None, min_credits=None, max_credits=None, comments=None, seven_weeks=None, section_id = None, course_id = None,faculty=None,section_meetings=None,gen_ed_fulfillments=None):
		self.term = term
		self.name = name
		self.shortTitle = short_title
		self.minCredits = min_credits
		self.maxCredits = max_credits
		self.comments = comments
		self.sevenWeeks = seven_weeks
		self.id = section_id
		self.courseId = course_id
		self.faculty = faculty
		self.sectionMeetings = section_meetings
		self.genEdFulfillments = gen_ed_fulfillments

# What a faculty object should contain
class FacultyObject(object):
	def __init__(self, first_initial = None, last_name = None):
		self.firstInitial = first_initial
		self.lastName = last_name

# What a sectionMeeting object should contain
class SectionMeetingObject(object):
	def __init__(self, room_id = None, start_time = None, end_time = None,days=None,room=None):
		self.roomId = room_id
		self.startTime = start_time
		self.endTime = end_time
		self.days = days
		self.room = room

# What a room object should contain
class RoomObject(object):
	def __init__(self, id = None, number = None, building_name = None, building_abb = None):
		self.id = id
		self.number = number
		self.buildingName = building_name
		self.buildingAbbrevation = building_abb

# What a gened fulfillment object should contain
class GenEdFulfillmentObject(object):
	def __init__(self, id = None, comments = None, name = None, abbreviation = None, also_fulfills=None):
		self.id = id
		self.comments = comments
		self.name = name
		self.abbreviation = abbreviation
		self.alsoFulfills = also_fulfills

# Get potential schedules
class ScheduleCreationObject(object):
	def __init__(self, schedule = None, index=None):
		self.schedule = schedule
		self.index = index

# Get potential schedules
class ScheduleCreationObject2(object):
	def __init__(self, schedule = None, index=None):
		self.schedule = schedule
		self.index = index