# Deployment Guide: Chrome Page Summarizer

This guide will help you set up and use the Chrome Page Summarizer system, including both the Streamlit app and the Chrome extension.

---

## 1. Streamlit App Setup

### A. Clone the Repository
```bash
git clone <repo-url>
cd chrome_summary
```

### B. Create and Activate a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### C. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### D. Run the Streamlit App
```bash
streamlit run app.py
```
- The app will be available at [http://localhost:8501](http://localhost:8501).
- The app will also start a local HTTP server on port 8502 for communication with the Chrome extension.

### E. Enter Your OpenAI API Key
- In the Streamlit sidebar, expand the "OpenAI API Key Settings" section.
- Enter your API key and save it securely. The key is stored locally using the `keyring` library and never leaves your machine.

---

## 2. Chrome Extension Setup

### A. Load the Unpacked Extension in Chrome
1. Open Chrome and go to `chrome://extensions`.
2. Enable "Developer mode" (toggle in the top right).
3. Click "Load unpacked" and select the `chrome_extension` folder from this repository.
4. You should see the extension appear in your toolbar.

### B. Using the Extension
- Navigate to any page you want to summarize.
- Click the Chrome Page Summarizer extension icon.
- Click the button to send the current page's content to the Streamlit app.
- You should see a message like "Sent. Check the App." in the extension popup.

---

## 3. Workflow
1. Start the Streamlit app and ensure it is running.
2. Use the Chrome extension to send page data.
3. Click the "Refresh" button in the Streamlit sidebar to fetch the latest page data.
4. The summary will appear automatically in the main section.

---

## 4. Troubleshooting

- **Extension says "Could not connect to the App":**
  - Ensure the Streamlit app is running and the HTTP server is listening on port 8502.
  - Make sure nothing else is using port 8502 (`lsof -i :8502`).
  - Check firewall or security settings that might block localhost connections.

- **No summary appears after clicking Refresh:**
  - Check the terminal running the Streamlit app for error messages.
  - Ensure your OpenAI API key is entered and valid.
  - Confirm that `page_data.json` is being created in the app directory.

- **Other Issues:**
  - Try restarting both the Streamlit app and Chrome.
  - Reload the extension from `chrome://extensions` if it appears unresponsive.

---

## 5. Security Notes
- Your OpenAI API key is stored locally and never sent to any server except OpenAI.
- All summarization is performed locally; no page content or keys are sent externally.
- The file `page_data.json` is used for communication between the extension and the app and is ignored by git (see `.gitignore`).

---

## 6. Uninstallation
- To remove the extension, go to `chrome://extensions` and click "Remove" for Chrome Page Summarizer.
- To remove the app, simply delete the project folder from your machine.

---

## 7. Support
If you encounter issues or have suggestions, please open an issue in the repository or contact the maintainer.
