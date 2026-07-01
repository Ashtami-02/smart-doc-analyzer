 Smart Document Analyzer

A lightweight Streamlit app that lets you upload a PDF and ask questions about its contents. The app extracts the document's text and sends it, along with your question, to Google's Gemini API, which answers strictly based on what's in the document.

 Features

- 📄 Upload any PDF and extract its full text
- 💬 Ask natural-language questions about the document
- 🤖 Answers are grounded only in the uploaded content (the model is instructed to say so if it can't find the answer)
- 🔁 Automatic fallback from `gemini-2.5-flash` to `gemini-2.5-flash-lite` if the primary model is unavailable
- 🔑 Flexible API key handling — reads from Streamlit secrets in the cloud, or prompts for a key locally


Prerequisites
- Python 3.9+
- A [Google Gemini API key](https://ai.google.dev/)

Installation

```bash
git clone https://github.com/Ashtami-02/smart-doc-analyzer.git
cd smart-doc-analyzer
pip install -r requirements.txt
```

Running the app

```bash
streamlit run app.py
```

Setting your API key

- **Locally:** paste your Gemini API key into the sidebar field when prompted.
- **Deployed (e.g. Streamlit Community Cloud):** add it to your app's secrets:
  ```toml
  GEMINI_API_KEY = "your-api-key-here"
  ```

 How it works

1. Upload a PDF — text is extracted page by page using `pypdf`.
2. Type a question about the document.
3. The full document text and your question are sent to Gemini in a single prompt that constrains the model to answer only from the provided text.
4. The answer is displayed in the app.
