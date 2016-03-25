// Formats the scrapped data, takes a string and returns an array
function formatSchedule(str) {
  str = str.replace(new RegExp(" ", "g"), "");
  str = str.replace(new RegExp("\n\n", "g"), ",");
  str = str.replace(new RegExp("\n", "g"), "");
  str = str.split(",");
  return str
} 


// Use JQuery to scrape schedule information
function getSavedSchedule() {
  var departments = $(".data__schedule__section__department").text();
  departments = formatSchedule(departments);

  var courseNumbers = $(".data__schedule__section__course-number").text();
  courseNumbers = formatSchedule(courseNumbers);

  var sectionNumbers = $(".data__schedule__section__section-number").text();
  sectionNumbers = formatSchedule(sectionNumbers);

  return [departments, courseNumbers, sectionNumbers];
}


// Listen for message to return schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.message === "save_schedule") {
		chrome.runtime.sendMessage({"message": "returning_schedule", "schedule": getSavedSchedule()});
	}
});