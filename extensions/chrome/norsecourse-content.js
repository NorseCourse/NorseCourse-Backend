// Insert a div signaling that the extension has been installed
var isInstalledNode = document.createElement('div');
isInstalledNode.id = 'extension-is-installed';
document.body.appendChild(isInstalledNode);


// Formats the scrapped data, takes a string and returns an array
function formatSchedule(str) {
  str = str.replace(new RegExp(" ", "g"), "");
  str = str.replace(new RegExp("\n\n", "g"), ",");
  str = str.replace(new RegExp("\n", "g"), "");
  str = str.split(","); //Creates an array of departmetn abbreviation strings
  return str
} 


// Use JQuery to scrape schedule information
function getSavedSchedule() {
  var allSchedules = $(".data__schedule");
  var scheduleIndex = Number($("#currentSavedScheduleIndex").text());
  var currentSchedule = allSchedules[scheduleIndex];

  var departments = formatSchedule($($(currentSchedule).find(".data__schedule__section__department")).text());
  var courseNumbers = formatSchedule($($(currentSchedule).find(".data__schedule__section__course-number")).text());
  var sectionNumbers = formatSchedule($($(currentSchedule).find(".data__schedule__section__section-number")).text());

  return [departments, courseNumbers, sectionNumbers];
}


// Listen for message to return schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.message === "save_schedule") {
		console.log("Received save_schedule message...");
		chrome.runtime.sendMessage({"message": "returning_schedule", "schedule": getSavedSchedule()});
		console.log("Sent return schedule...");
	}
});