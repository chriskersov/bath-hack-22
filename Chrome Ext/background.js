chrome.action.onClicked.addListener((tab) => {
  // Inject the content script into the current active tab
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js']
  });
});