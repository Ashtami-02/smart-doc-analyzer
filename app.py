import streamlit as st
import pypdf
from google import genai  # <-- New import for the AI

# 1. Page Configuration
st.set_page_config(page_title="Smart Doc Analyzer", page_icon="🤖")

# 2. Main Page Titles
st.title("🤖 Smart Document Analyzer")
st.write("Upload a PDF and ask questions about its content.")

# 3. Sidebar for API Key
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# 4. File Uploader Layout
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if the user has provided the API key yet
if api_key:
    # Initialize the Gemini Client using the new 2026 Google GenAI SDK
    client = genai.Client(api_key=api_key)

    # 5. Visual feedback and Text Extraction
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Initialize the PDF reader and extract text
        pdf_reader = pypdf.PdfReader(uploaded_file)
        document_text = ""
        for page in pdf_reader.pages:
            document_text += page.extract_text() + "\n"
        
        st.info(f"Successfully extracted {len(pdf_reader.pages)} pages of text.")

        # --- FINAL AI CODE STARTS HERE ---
        # 6. User Question Input Box
        user_question = st.text_input("Ask a question about this document:")

        if user_question:
            with st.spinner("Analyzing document and thinking..."):
                try:
                    # Constructing the RAG prompt (Instructing the LLM)
                    prompt = f"""
                    You are an expert document assistant. Below is the content of an uploaded document.
                    Use ONLY the provided document text to answer the user's question. If the answer cannot 
                    be found in the text, say "I cannot find the answer in the provided document."

                    Document Content:
                    \"\"\"
                    {document_text}
                    \"\"\"

                    User Question: {user_question}
                    """

                   # --- UPDATED AI CALL WITH FALLBACK ---
                    try:
                        # Attempt to use the primary model
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                        )
                    except Exception as flash_error:
                        # If Flash is down, fallback to the ultra-lightweight Flash-Lite model
                        st.warning("Primary model busy, switching to backup model...")
                        response = client.models.generate_content(
                            model='gemini-2.5-flash-lite',  # Light backup model
                            contents=prompt,
                        )
                    # --- END OF UPDATED SECTION ---
                    
                    
                    # 7. Display the AI's answer beautifully
                    st.subheader("Answer:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        # --- FINAL AI CODE ENDS HERE ---
else:
    st.sidebar.warning("Please enter your Gemini API Key to unlock the app!")