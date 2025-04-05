// content.js
(() => {
  console.log("Panopto Caption Extractor: Script injected.");

  // Function to extract captions
  const extractCaptions = async () =>  {
    const captionElements = document.querySelectorAll(".event-tab-scroll-pane .index-event-row .event-text span");
    if (captionElements.length > 0) {
      const captions = Array.from(captionElements)
        .map(el => el.innerText.trim())
        .join('\n');
      console.log("Captions extracted:", captions);

      try {
        const summary = await summarizeCaptions(captions);
        console.log("Lecture Summary:", summary);

        // Display the summary to the user
        alert(`Lecture Summary:\n\n${summary}`);

        // Export the summary as a PDF
      } catch (error) {
        console.error("Error summarizing captions:", error);
        alert("Failed to generate summary. Please try again.");
      }
    } else {
      console.log("No captions found.");
      alert("No captions found.");
    }
  };

  // Function to summarize captions using OpenAI API
  const summarizeCaptions = async (captions) => {
    const apiKey = "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"; // Replace with your OpenAI API key
    const url = "https://api.openai.com/v1/chat/completions"; // OpenAI API endpoint

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
            model: "gpt-4o-mini", // Use the desired model
            messages: [
                {
                    role: "system",
                    content: "You are a helpful assistant that summarizes lecture captions into easy-to-understand summaries.",
                },
                {
                    role: "user",
                    content: `Your job is to add a structure to it and explain it, as well as giving different questions and answers so that I understand the topic in the best way possible. Here's are the captions:\n\n${captions}`,
                },
            ],
            // max_tokens: 1000000, // Adjust as needed
        }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0].message.content; // Return the summary
  };

  // Run the extraction function
  extractCaptions();
})();