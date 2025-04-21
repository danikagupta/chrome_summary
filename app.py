import streamlit as st
import keyring
import openai
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- Constants ---
SERVICE_NAME = "chrome_summary_app"
API_KEY_ENTRY = "openai_api_key"

# --- Helper functions ---
def get_api_key():
    return keyring.get_password(SERVICE_NAME, API_KEY_ENTRY)

def set_api_key(key):
    keyring.set_password(SERVICE_NAME, API_KEY_ENTRY, key)

def summarize_page(content, api_key, prompt=None):
    openai.api_key = api_key
    system_prompt = prompt or (
        "You are an expert assistant. Extract the most meaningful information from the following web page content. "
        "Instead of summarizing, identify actionable insights, implications for the user, and clear action items. "
        "If relevant, list next steps, important warnings, and key takeaways."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-nano",  # GPT-4.1-mini
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            max_tokens=512,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# --- Shared state for page data ---
class PageData:
    def __init__(self):
        self.title = ""
        self.url = ""
        self.content = ""
        self.updated = False
page_data = PageData()

# --- HTTP Handler for Chrome Extension ---
class PageDataHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        print(f'[HTTPServer] Received POST request on {self.path}')
        if self.path == "/page_data":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            print(f'[HTTPServer] Raw POST data: {post_data}')
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(f'[HTTPServer] Decoded JSON: {data}')
                page_data.title = data.get('title', '')
                page_data.url = data.get('url', '')
                page_data.content = data.get('content', '')
                page_data.updated = True
                # Persist to file for Streamlit UI to read
                import pathlib
                file_path = pathlib.Path('page_data.json').resolve()
                print(f'[HTTPServer] Attempting to write page_data.json at {file_path}')
                try:
                    with open(file_path, 'w') as f:
                        json.dump({
                            'title': page_data.title,
                            'url': page_data.url,
                            'content': page_data.content
                        }, f)
                    print('[HTTPServer] Successfully wrote page_data.json')
                except Exception as file_exc:
                    print(f'[HTTPServer] Error writing page_data.json: {file_exc}')
                print(f'[HTTPServer] page_data.json exists after write? {file_path.exists()}')
                self.send_response(200)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(b'OK')
            except Exception as e:
                print(f'[HTTPServer] Error handling POST: {e}')
                self.send_response(400)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        else:
            print(f'[HTTPServer] 404 for path: {self.path}')
            self.send_response(404)
            self._set_cors_headers()
            self.end_headers()

# --- Start HTTP Server in Thread ---
def start_server():
    try:
        server = HTTPServer(('localhost', 8502), PageDataHandler)
        print('[HTTPServer] Started successfully on http://localhost:8502')
        server.serve_forever()
    except Exception as e:
        print(f'[HTTPServer] Failed to start: {e}')

def start_server_in_thread():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()

# --- Streamlit UI ---
st.set_page_config(page_title="Chrome Page Summarizer", layout="centered")

# Sidebar: API Key Management
with st.sidebar.expander("🔑 OpenAI API Key Settings", expanded=False):
    api_key = get_api_key()
    api_key_input = st.text_input("Enter your OpenAI API key", value=api_key if api_key else "", type="password", key="api_key_input")
    if st.button("Save API Key", key="save_api_key"):
        set_api_key(api_key_input)
        st.success("API key saved securely.")

# Sidebar: Custom Prompt
st.sidebar.markdown("---")
st.sidebar.header("Summarizer Prompt")
default_prompt = (
    "You are an expert assistant. Extract the most meaningful information from the following web page content. "
    "Instead of summarizing, identify actionable insights, implications for the user, and clear action items. "
    "If relevant, list next steps, important warnings, and key takeaways."
)
custom_prompt = st.sidebar.text_area("Custom prompt (optional)", value="", height=80, key="custom_prompt")
active_prompt = custom_prompt.strip() if custom_prompt.strip() else default_prompt
st.sidebar.caption(f"Current prompt: {active_prompt}")

# Sidebar: Page Information
st.sidebar.markdown("---")
st.sidebar.header("Page Information")
import pathlib
page_data_path = pathlib.Path('page_data.json')
print('[Streamlit] Checking for page_data.json at', page_data_path.resolve())
if page_data_path.exists():
    try:
        with open(page_data_path, 'r') as f:
            file_data = json.load(f)
        print('[Streamlit] Loaded page_data.json:', file_data)
        st.session_state['title'] = file_data.get('title', '')
        st.session_state['url'] = file_data.get('url', '')
        st.session_state['content'] = file_data.get('content', '')
    except Exception as e:
        print('[Streamlit] Error reading page_data.json:', e)
else:
    print('[Streamlit] page_data.json does not exist.')

# Main: Page Title and URL
st.title("Chrome Page Summarizer")
st.markdown("---")
st.subheader("Page Title")
st.text_input("Page Title", st.session_state.get('title', ''), key="title", disabled=True)
st.subheader("Page URL")
st.text_input("Page URL", st.session_state.get('url', ''), key="url", disabled=True)

# Sidebar: Page Content and Refresh
page_content = st.sidebar.text_area("Page Content (paste or sent by extension)", st.session_state.get('content', ''), height=200, key="content")
if st.sidebar.button("🔄 Refresh", help="Click to fetch the latest page data sent by the Chrome extension", key="refresh_btn"):
    st.rerun()

# Main: Summary Section Only
st.title("Chrome Page Summarizer")

summary_placeholder = st.empty()
error_placeholder = st.empty()

# Auto-summarize when content changes
if 'last_summarized_content' not in st.session_state:
    st.session_state['last_summarized_content'] = ''
if 'summary' not in st.session_state:
    st.session_state['summary'] = ''

api_key = get_api_key()
current_content = st.session_state.get('content', '')

should_summarize = (
    current_content.strip() and
    api_key and
    current_content != st.session_state['last_summarized_content']
)

if should_summarize:
    with st.spinner("Generating summary..."):
        summary = summarize_page(current_content, api_key, active_prompt)
    st.session_state['summary'] = summary
    st.session_state['last_summarized_content'] = current_content
    summary_placeholder.subheader("Summary")
    summary_placeholder.write(summary)
    error_placeholder.empty()
else:
    if not api_key:
        error_placeholder.error("Please enter your OpenAI API key in the sidebar.")
    elif not current_content.strip():
        error_placeholder.info("No page content provided. Use the Chrome extension or paste content in the sidebar.")
    elif st.session_state['summary']:
        summary_placeholder.subheader("Summary")
        summary_placeholder.write(st.session_state['summary'])
    else:
        summary_placeholder.info("No summary available yet.")

# Instructions for Chrome Extension (sidebar)
st.sidebar.markdown("---")
st.sidebar.info("""
To enable automatic page extraction, install the companion Chrome Extension from the 'chrome_extension' folder in this repo. Click the extension button to send the current page to this app.
If the app is not running or you prefer, you can still paste content manually above.

**Note:** The app must be running and listening on port 8502 for the extension to work.
""")
