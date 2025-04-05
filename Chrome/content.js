(() => {
    console.log("Panopto Caption Extractor: Script injected.");
  
    // Adjust the selector as needed for the Panopto caption elements
    const captionElements = document.querySelectorAll(".event-tab-scroll-pane .index-event-row .event-text span");
  
    if (captionElements.length > 0) {
      const captions = Array.from(captionElements)
        .map(el => el.innerText.trim())
        .join("\n");
      console.log("Captions extracted:", captions);
  
      // Send the extracted captions to the background script
      chrome.runtime.sendMessage({ type: "CAPTIONS_EXTRACTED", captions });
    } else {
      console.log("No captions found on this page.");
      alert("No captions found on this page.");
    }
  })();
  