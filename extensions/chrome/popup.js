// Angular Material App Javascript
var app = angular.module('PopupApp', ['ngMaterial'])
  .controller('PopupCtrl', function($scope) {

  })
  .config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('indigo')
      .accentPalette('pink')
      .warnPalette('amber')
  });


// red, pink, purple, deep-purple, indigo, blue, light-blue, cyan, teal, green, light-green, lime, yellow, amber, orange, deep-orange, brown, grey, blue-grey


// Action when 'Retreive Saved Schedule' button is clicked
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('getSavedSchedule');
  button.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {"message": "save_schedule"});
      console.log("Sent save_schedule message...");
    });
  }, false);
}, false);


// Listen for returned schedule
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.message === "returning_schedule") {
    console.log("Received return schedule...");
    var scheduleData = request.schedule;
    saveSchedule(scheduleData[0], scheduleData[1], scheduleData[2]);
  }
});


// Save the retreived schedyle to local storage
function saveSchedule(departments, courseNumbers, sectionNumbers) {
  chrome.storage.local.set({"departments": departments, "courseNumbers": courseNumbers, "sectionNumbers": sectionNumbers}, function() {
    console.log("Schedule has been saved to local memory...");
  });
}


// Action when 'Register Saved Schedule' button is clicked
document.addEventListener('DOMContentLoaded', function() {
  var button = document.getElementById('registerSchedule');
  button.addEventListener('click', function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {"message": "register_schedule"});
      console.log("Sent register_schedule message...");
    });
  }, false);
}, false);