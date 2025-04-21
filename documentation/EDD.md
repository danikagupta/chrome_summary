# Engineering Design Document (EDD): Chrome Page Summarizer App

## 1. Overview
This document details the technical design for a local application that summarizes the active Chrome tab using OpenAI's GPT-4.1-mini. It covers architecture, technology choices, Chrome integration, UI/UX, security, error handling, and implementation plan.

## 2. Architecture & Technology Choices
- **Frontend/UI**: Streamlit (Python-based web app framework, runs locally in browser)
- **Backend/Logic**: Python (runs Streamlit app and handles API calls)
- **Chrome Integration**: Chrome Extension (extracts active tab content and communicates with Streamlit app via local HTTP endpoint or WebSocket)
- **AI Integration**: OpenAI API (GPT-4.1-mini)
- **Local Storage**: Secure local file (for API key, e.g., using Python keyring or encrypted file)

## 3. Chrome Integration Approach
- **Chrome Extension**: 
    - Reads content, title, and URL from the active tab.
    - Sends this data to the Streamlit app via a local HTTP endpoint or WebSocket.
    - Requires user to install the extension and grant permissions.
- **Streamlit App**:
    - Exposes a local endpoint (HTTP/WebSocket) to receive messages from the extension.
    - Manages UI, API key storage, and summary generation.

## 4. UI/UX Design Overview
- **Main Window**:
    - Displays current page title and URL
    - Text area for summary (auto-filled after generation)
    - Button to trigger summary
    - Settings section for entering/updating API key
    - Error and status messages
- **Design Principles**:
    - Clean, modern, minimal
    - Responsive feedback for user actions

## 5. Security & API Key Handling
- API key is stored locally using Python's keyring library or an encrypted file
- API key is never logged or sent to any server except OpenAI
- No analytics or telemetry

## 6. Error Handling & Edge Cases
- **Invalid API Key**: Show clear error, prompt for correction
- **No Content/Unreadable Page**: Inform user and suggest retry
- **Network/API Errors**: Show status and retry option
- **Extension Not Installed**: Detect and prompt user to install

## 7. Sequence Diagram (Summary Generation)
1. User navigates to a page in Chrome
2. User clicks 'Summarize' in Electron app
3. Chrome Extension extracts page content and sends it to Electron app
4. Electron app sends content to OpenAI API using user's key
5. App receives summary and displays it in UI

## 8. Implementation Plan & Milestones
1. **Set up Streamlit app skeleton and UI**
2. **Build Chrome Extension for content extraction**
3. **Implement communication between extension and Streamlit app (local HTTP endpoint or WebSocket)**
4. **Integrate OpenAI API and summary logic**
5. **Secure API key storage and settings UI**
6. **Error handling and edge cases**
7. **Testing and polish**

## 9. Dependencies
- Streamlit
- Python 3.8+
- OpenAI Python package
- Chrome Extension APIs
- Secure storage (e.g., keyring, cryptography)
- Requests or httpx (for HTTP communication)
- WebSocket libraries (optional, for real-time communication)

## 10. Future Enhancements
- Windows/Linux support
- Support for other browsers
- Advanced summary options

---

Please review this EDD. Once approved, I will begin implementation according to this plan.
