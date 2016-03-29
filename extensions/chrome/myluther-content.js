// my.luther form id's 
var subjectBox = "#LIST_VAR1_";
var courseNumberBox = "#LIST_VAR3_";
var sectionNumberBox = "#LIST_VAR4_";


// Listen for message to register schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.message === "register_schedule") {
		console.log("Received register_schedule message...");
		chrome.storage.local.get(["departments", "courseNumbers", "sectionNumbers"], function(scheduleData) {
			var departments = scheduleData.departments;
			var courseNumbers = scheduleData.courseNumbers;
			var sectionNumbers = scheduleData.sectionNumbers;
			var numberOfCourses = departments.length;

			if (departments == "") {
				alert("No saved schedules have been retrieved.")
			} else {
				// Clear the form if there is anything there
				clearMyLutherForm();

				// Set the term value to the most recent term, this will wither be spring or fall
				$("#VAR1").val($("#VAR1 option:nth-child(2)").val());

				// Populate the form on my.luther with the saved schedule 
				for (var i = 1; i <= numberOfCourses; i++) {
					var iStr = i.toString();
					var idx = i - 1;
					$(subjectBox + iStr).val(departments[idx]);
					$(courseNumberBox + iStr).val(courseNumbers[idx]);
					$(sectionNumberBox + iStr).val(sectionNumbers[idx]);
				}
			}
		});
	}
});


function clearMyLutherForm() {
	// Set the term value as empty
	$("#VAR1").val($("#VAR1 option:nth-child(1)").val());

	for (var i = 1; i <= 5; i++) {
		var iStr = i.toString();

		var clearSubject = subjectBox + iStr;

		$(clearSubject).val($(clearSubject + " option:nth-child(1)").val());
		$(courseNumberBox + iStr).val("");
		$(sectionNumberBox + iStr).val("");
	}
}