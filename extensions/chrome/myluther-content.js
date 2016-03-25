// Listen for message to register schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.message === "register_schedule") {
		chrome.storage.local.get(["departments", "courseNumbers", "sectionNumbers"], function(scheduleData) {
			var departments = scheduleData.departments;
			var courseNumbers = scheduleData.courseNumbers;
			var sectionNumbers = scheduleData.sectionNumbers;
			var numberOfCourses = departments.length;

			// Set the term value to the most recent term, this will wither be spring or fall
			$("#VAR1").val($("#VAR1 option:nth-child(2)").val());

			var subjectBox = "#LIST_VAR1_";
			var courseNumberBox = "#LIST_VAR3_";
			var sectionNumberBox = "#LIST_VAR4_";

			// Populate the form on my.luther with the saved schedule 
			for (var i = 1; i <= numberOfCourses; i++) {
				var iStr = i.toString();
				var idx = i - 1;
				$(subjectBox + iStr).val(departments[idx]);
				$(courseNumberBox + iStr).val(courseNumbers[idx]);
				$(sectionNumberBox + iStr).val(sectionNumbers[idx]);
			}
		});
	}
});