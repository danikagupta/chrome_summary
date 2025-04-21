# Requirements for Chrome Page Summarizer App

## Overview
A local application that interacts with the user's Chrome browser to retrieve the content of the currently active web page and provides a summary of that page using OpenAI's GPT-4.1-mini model.

## Functional Requirements
- The app must be able to access the content (text) of the currently active tab in the user's Chrome browser.
- The app must provide a user interface that allows the user to:
    - View the current web page's title and URL.
    - View a summary of the current web page.
    - Enter and store their OpenAI API key securely (locally, never sent to any server except OpenAI).
    - Trigger a summary generation for the current page.
- The app must use the OpenAI GPT-4.1-mini model to generate the summary.
- The summary should be concise and capture the main points of the web page.

## Non-Functional Requirements
- The app must run locally on the user's machine (macOS support required; cross-platform preferred).
- The API key must be stored securely and never logged or shared.
- The UI should be clean, modern, and user-friendly.
- Performance should be sufficient to generate a summary within a few seconds after user action.
- The app should handle errors gracefully (e.g., invalid API key, network errors, empty pages).

## Out of Scope
- No server-side storage or analytics.
- No support for browsers other than Chrome in the initial version.

## Future Considerations
- Support for other browsers (Safari, Firefox, Edge).
- Support for summarizing multiple tabs or history.
- Options for summary length or style.

## Security
- The OpenAI API key is only ever stored and used locally.
- No user data or browsing history is sent to any server except OpenAI for summary generation.
