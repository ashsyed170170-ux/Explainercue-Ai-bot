import os
import pypdf
import streamlit as st
from google import genai  # Gemini ki library

# Streamlit secrets se key uthana
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

# Gemini client initialize karna
client = genai.Client(api_key=api_key)

# PDF read karne ka function
def read_pdf_data(pdf_path="company_data.pdf"):
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
        return "Filhal koi data available nahi hai."

# Data load karna
knowledge_base = read_pdf_data("company_data.pdf")

# --- Streamlit UI aur Chat Logic ---
st.title("Real Estate AI Assistant (Gemini)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Poochyein..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Gemini ke liye prompt design karna
    system_prompt = f"Aap ek professional Real Estate Assistant hain. Sirf is data ke mutabik Roman Urdu mein jawab dein: {knowledge_base}"
    
    # Gemini API ko call karna (2026 ka behtareen standard model)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[system_prompt, user_input]
    )
    
    answer = response.text
    
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
