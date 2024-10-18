browser.browserAction.onClicked.addListener(() => {
  browser.sidebarAction.toggle();
  console.log("Extension icon clicked!");
});
