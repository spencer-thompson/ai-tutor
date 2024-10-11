if (typeof chrome !== "undefined") {
  // Chrome-specific code
  chrome.sidePanel
    .setPanelBehavior({ openPanelOnActionClick: true })
    .catch((error) => console.error(error));
} else if (typeof browser !== "undefined") {
  // Firefox-specific code
  browser.browserAction.onClicked.addListener(() => {
    browser.sidebarAction.toggle();
    console.log("Extension icon clicked!");
  });
}

// Allows users to open the side panel by clicking on the action toolbar icon
