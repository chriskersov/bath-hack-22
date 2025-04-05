document.getElementById('extractCaptions').addEventListener('click', async () => {
  // Get the active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // Inject the content script into the active tab
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ['content.js']
  });
});