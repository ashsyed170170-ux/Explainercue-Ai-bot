import os
import streamlit as st
from google import genai

# Streamlit secrets se key uthana
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

# 2026 Google Official Client Initialization
client = genai.Client(api_key=api_key)

# Background mein file read karne ka tareeqa
def read_knowledge_base():
    possible_names = ["company_data", "Company_data", "Company_data.pdf.txt", "company_data.pdf.txt"]
    for name in possible_names:
        if os.path.exists(name):
            try:
                with open(name, "r", encoding="utf-8") as file:
                    return file.read()
            except Exception:
                pass
    return ""

knowledge_base = read_knowledge_base()

# --- Streamlit UI Setup ---
st.title("Arcturus Group AI Assistant")

if knowledge_base and len(knowledge_base) > 10:
    st.sidebar.success("✅ Knowledge Base Loaded Successfully!")
else:
    st.sidebar.warning("⚠️ Reading from backup storage...")
    knowledge_base = "Arcturus Group is a premier senior real estate advisory firm that maximizes value for its clients by providing independent analytical and strategic services to investors, lenders, and developers."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything about Arcturus Group..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if not api_key:
        answer = "ERROR: GEMINI_API_KEY is missing in Streamlit Secrets!"
    else:
        # Strict English Prompts
        system_prompt = f"""You are a professional Business & Real Estate Assistant. 
Your task is to answer user queries strictly based on the provided Context Data below. 
If the answer cannot be found in the context, politely state that you do not have this information.

Context Data:
{knowledge_base}

CRITICAL CONSTRAINT: You must respond ONLY and strictly in the English language. Even if the user asks questions in Roman Urdu or Hindi, your entire response must be written in clear, professional English. Do not use any non-English words."""
        
        try:
            # 2026 Naya model aur call format (No URL errors anymore)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[system_prompt, user_input]
            )
            answer = response.text
        except Exception as e:
            answer = f"System Connection Alert: {str(e)}"
            
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
