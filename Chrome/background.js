chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "CAPTIONS_EXTRACTED") {
      // Send the extracted captions to your local web app
      fetch("http://127.0.0.1:8080/WhoWantsToBeAGraduate/api/captions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ captions: message.captions })
      })
        .then(response => response.json())
        .then(data => {
          console.log("Captions sent successfully:", data);
          sendResponse({ status: "success", data });
        })
        .catch(error => {
          console.error("Error sending captions:", error);
          sendResponse({ status: "error", error: error.toString() });
        });
      return true; // Keeps the message channel open for the async response
    }
  });
  