document.getElementById("extractCaptions").addEventListener("click", async () => {
    const statusDiv = document.getElementById("status");
    statusDiv.textContent = "Extracting captions...";
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ["content.js"]
    }, () => {
      statusDiv.textContent = "Extraction script executed.";
    });
  });
  