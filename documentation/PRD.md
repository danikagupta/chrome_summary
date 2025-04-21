# Product Requirements Document (PRD): Chrome Page Summarizer App

## 1. Purpose
To provide users with a local application that can access the currently active Chrome browser tab, extract its content, and generate a concise summary using OpenAI's GPT-4.1-mini model. The app will allow users to securely provide their OpenAI API key and will operate fully on the user's local machine.

## 2. Background & Motivation
With the increasing volume of information on the web, users often need quick summaries of web pages without reading the entire content. This app aims to streamline content consumption by leveraging state-of-the-art AI summarization, while ensuring user privacy and local control.

## 3. Features
### Core Features
- Retrieve the content (text) of the currently active tab in Chrome.
- Display the page title and URL.
- Summarize the page using OpenAI's GPT-4.1-mini model.
- Allow users to input and store their OpenAI API key securely (local-only storage).
- User interface to:
    - View web page info and summary
    - Enter/update API key
    - Trigger summary generation

### Error Handling
- Handle invalid API keys, network errors, and empty/unreadable pages with clear user feedback.

### Security
- API key is never transmitted or logged except for calls to OpenAI.
- No analytics or server-side data storage.

## 4. User Stories
- As a user, I want to summarize the page I'm viewing in Chrome with one click.
- As a user, I want to securely provide my OpenAI API key and know it is not shared.
- As a user, I want to see the summary, title, and URL of the current page in a clean UI.
- As a user, I want to be notified of errors (e.g., invalid API key, no page content).

## 5. Scope
### In Scope
- Chrome browser support (active tab only)
- macOS support (cross-platform preferred, but not required for v1)
- Local-only storage and processing
- UI for summary, API key, and error messages

### Out of Scope (v1)
- Other browsers (Safari, Firefox, Edge)
- Summarizing multiple tabs/history
- Server-side storage, analytics, or account systems

## 6. Success Metrics
- User can generate a summary for the active Chrome tab within 10 seconds
- No user data or API keys are leaked or stored externally
- Users report ease of use and satisfaction with summary quality

## 7. Future Considerations
- Support for other browsers
- Options for summary length/style
- Summarizing browsing history or multiple tabs

---

Please review and let me know if you would like any changes before I proceed to the Engineering Design Document.
