import os
import streamlit as st
import google.generativeai as genai

# Streamlit secrets se key uthana aur configure karna
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Background mein file read karne ka function (.txt extension ke sath)
def read_knowledge_base(file_path="Company_data.pdf.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""

# GitHub par majood exact file name load karna
file_filename = "Company_data.pdf.txt"
knowledge_base = read_knowledge_base(file_filename)

# --- Streamlit UI aur Chat Logic ---
st.title("Arcturus Group AI Assistant")

# Sidebar status bar
if knowledge_base:
    st.sidebar.success("✅ Knowledge Base Loaded Successfully!")
else:
    st.sidebar.error("❌ ERROR: Company_data.pdf.txt not found in root folder!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything about Arcturus Group..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Fully English System Prompt for strict compliance
    system_prompt = f"""
    You are a professional Business & Real Estate Assistant. 
    Your task is to answer user queries strictly based on the provided Context Data below. 
    If the answer cannot be found in the context, politely state that you do not have this information.

    Context Data:
    {knowledge_base}
    
    CRITICAL CONSTRAINT: You must respond ONLY and strictly in the English language. Even if the user asks questions in Roman Urdu, Hindi, or any other language, your entire response must be written in clear, professional English. Do not use any non-English words (like 'Ji', 'Haan', 'Maaf kijiye') under any circumstances.
    """
    
    # Gemini 1.5 Flash Model configuration
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    response = model.generate_content(f"{system_prompt}\n\nUser Question: {user_input}")
    answer = response.text
    
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
