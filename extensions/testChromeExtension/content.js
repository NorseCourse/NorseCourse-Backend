// alert("Hello from my Chrome extension!");

// var firstHref = $("a[href^='http']").eq(0).attr("href");
// console.log(firstHref);

// console.log("Hello, world!");
// angular.module("norseCourse").service("schedulesService").getSavedSchedules();

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
      var firstHref = $("a[href^='http']").eq(0).attr("href");
      // console.log(firstHref);
      chrome.runtime.sendMessage({"message": "open_new_tab", "url": firstHref});

      // var testing = $("md-list-item").get();
      // console.log(testing);

    }
  }
);