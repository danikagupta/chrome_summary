document.getElementById('sendBtn').onclick = async function() {
  document.getElementById('status').innerText = 'Extracting page...';
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.scripting.executeScript({
      target: {tabId: tabs[0].id},
      func: () => {
        // Extract main visible text content
        function getVisibleText() {
          let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
          let text = '';
          let node;
          while (node = walker.nextNode()) {
            if (node.parentNode.offsetParent !== null && node.nodeValue.trim()) {
              text += node.nodeValue.trim() + ' ';
            }
          }
          return text;
        }
        return {
          title: document.title,
          url: window.location.href,
          content: getVisibleText().slice(0, 10000) // limit for safety
        };
      }
    }, async (results) => {
      if (chrome.runtime.lastError || !results || !results[0]) {
        document.getElementById('status').innerText = 'Failed to extract page.';
        return;
      }
      const pageData = results[0].result;
      document.getElementById('status').innerText = 'Sending to app...';
      try {
        const resp = await fetch('http://localhost:8502/page_data', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(pageData)
        });
        if (resp.ok) {
          document.getElementById('status').innerText = 'Sent! Check the app.';
        } else {
          document.getElementById('status').innerText = 'App not running or error.';
        }
      } catch (e) {
        document.getElementById('status').innerText = 'Could not connect to app.';
      }
    });
  });
};
