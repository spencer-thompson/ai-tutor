chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

// // Store data // CHATGPT
// chrome.storage.local.set({ key: 'value' }, function() {
//     console.log('Data is stored.');
// });
//
// // Retrieve data
// chrome.storage.local.get(['key'], function(result) {
//     console.log('Value currently is ' + result.key);
// });
//
// // Remove data
// chrome.storage.local.remove('key', function() {
//     console.log('Data is removed.');
// });
//
// // Clear all data
// chrome.storage.local.clear(function() {
//     console.log('All data is cleared.');
// });
