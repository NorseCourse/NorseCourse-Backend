// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
  // Send a message to the active tab
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, {"message": "clicked_browser_action"});
  });
});

// Listen for click, send message to content, which will send back
// the first URL on the page, then background will open new tab
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // if( request.message === "open_new_tab" ) {
    //   chrome.tabs.create({"url": request.url});
    // }
  }
);