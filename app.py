import os
import pypdf
import streamlit as st
import google.generativeai as genai  # Stable library integration

# Streamlit secrets se key uthana aur configure karna
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

# Gemini ko key ke sath configure karna
genai.configure(api_key=api_key)

# PDF read karne ka function
def read_pdf_data(pdf_path="Company_data.pdf"):
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except FileNotFoundError:
        return ""

pdf_filename = "Company_data.pdf"
knowledge_base = read_pdf_data(pdf_filename)

# --- Streamlit UI aur Chat Logic ---
st.title("Arcturus Group AI Assistant")

if knowledge_base:
    st.sidebar.success("✅ PDF Data Loaded Successfully!")
else:
    st.sidebar.error("❌ ERROR: Company_data.pdf not found!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything about Arcturus Group..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Fully English System Prompt
    system_prompt = f"""
    You are a professional Business & Real Estate Assistant. 
    Your task is to answer user queries strictly based on the provided Context Data below. 
    If the answer cannot be found in the context, politely state that you do not have this information.

    Context Data:
    {knowledge_base}
    
    CRITICAL CONSTRAINT: You must respond ONLY and strictly in the English language. Even if the user asks questions in Roman Urdu, Hindi, or any other language, your entire response must be written in clear, professional English. Do not use any non-English words (like 'Ji', 'Haan', 'Maaf kijiye') under any circumstances.
    """
    
    # Gemini API Call using the stable configuration
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # System instruction aur user input ko milakar bhejna
    response = model.generate_content(f"{system_prompt}\n\nUser Question: {user_input}")
    answer = response.text
    
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
