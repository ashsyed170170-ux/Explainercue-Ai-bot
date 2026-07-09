import os
import pypdf
import streamlit as st
from google import genai  # Gemini official library

# Streamlit secrets se key uthana
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

# Gemini client initialize karna
client = genai.Client(api_key=api_key)

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

# GitHub par majood sahi file name (C is capital)
pdf_filename = "Company_data.pdf"
knowledge_base = read_pdf_data(pdf_filename)

# --- Streamlit UI aur Chat Logic ---
st.title("Arcturus Group AI Assistant")

# Sidebar mein status check dikhana ke file mili ya nahi
if knowledge_base:
    st.sidebar.success("✅ PDF Data Loaded Successfully!")
else:
    st.sidebar.error("❌ ERROR: Company_data.pdf not found in root folder!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything about Arcturus Group..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Strictly English response system prompt
    system_prompt = f"""
    Aap ek professional Business & Real Estate Assistant hain. 
    Aapko sirf aur sirf nechy diye gaye data (Context) ke mutabik jawab dena hai. 
    Agar data mein jawab na ho, to bol dein ke maloomat nahi hain.

    Context Data:
    {knowledge_base}
    
    CRITICAL INSTRUCTION: You must respond ONLY in English language. Even if the user asks questions in Roman Urdu, Hindi, or any other language, your response must strictly be in clear, professional English. Do not use Roman Urdu words like 'Ji', 'Haan', or 'Maaf kijiye' in your output.
    """
    
    # Gemini API Call using modern standard model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[system_prompt, user_input]
    )
    
    answer = response.text
    
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
