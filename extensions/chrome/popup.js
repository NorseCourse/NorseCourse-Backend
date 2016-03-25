// Action when 'Retreive Saved Schedule' button is clicked
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('getSavedSchedule');
  button.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {"message": "save_schedule"});
    });
  }, false);
}, false);


// Listen for returned schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.message === "returning_schedule") {
    var scheduleData = request.schedule;
    saveSchedule(scheduleData[0], scheduleData[1], scheduleData[2]);
  }
});


// Save the retreived schedyle to local storage
function saveSchedule(departments, courseNumbers, sectionNumbers) {
  chrome.storage.local.set({"departments": departments, "courseNumbers": courseNumbers, "sectionNumbers": sectionNumbers}, function() {
  });
}


// Action when 'Register Saved Schedule' button is clicked
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('registerSchedule');
  button.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {"message": "register_schedule"});
    });
  }, false);
}, false);