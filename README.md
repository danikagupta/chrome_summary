# Chrome Page Summarizer App

A local app that summarizes the current Chrome tab using OpenAI GPT-4.1-mini, with a Streamlit UI.

## Features
- Summarizes the active Chrome page using GPT-4.1-mini
- User provides their OpenAI API key (stored locally)
- Clean, modern UI with Streamlit
- Chrome extension integration for page extraction

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```
3. Install the Chrome extension (instructions will be provided in the documentation).

## Security
- Your OpenAI API key is stored locally and never shared except with OpenAI.

## License
MIT
