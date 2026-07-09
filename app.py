import os
import pypdf
import streamlit as st
from google import genai

# Streamlit secrets se API key uthana
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

# 2026 Google Client Initialization
client = genai.Client(api_key=api_key)

# CACHING ADDED: Yeh function baar-baar run nahi hoga, sirf 1 dafa chalega
@st.cache_data(show_spinner="Loading Knowledge Base...")
def read_pdf_knowledge_base():
    file_path = "company_data.pdf"
    if os.path.exists(file_path):
        try:
            text = ""
            pdf_reader = pypdf.PdfReader(file_path)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    return ""

knowledge_base = read_pdf_knowledge_base()

# --- Streamlit UI Setup ---
st.title("ExplainerCue AI Assistant")

# Sidebar status validation
if knowledge_base and not knowledge_base.startswith("Error"):
    st.sidebar.success("✅ Knowledge Base Loaded Successfully!")
elif knowledge_base.startswith("Error"):
    st.sidebar.error(f"❌ {knowledge_base}")
else:
    st.sidebar.error("❌ ERROR: company_data.pdf not found in GitHub root folder!")
    knowledge_base = "Explainercue is a premier senior explainervideos advisory firm."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask anything about ExplainerCue..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    if not api_key:
        answer = "ERROR: GEMINI_API_KEY is missing in Streamlit Secrets!"
    elif not knowledge_base or knowledge_base.startswith("ExplainerCue is a premier"):
        answer = "I am sorry, but I cannot access the full company documentation right now. Please ensure company_data.pdf is uploaded to GitHub."
    else:
        system_prompt = f"""You are a professional Business & Explainer Video Assistant. 
Your task is to answer user queries strictly based on the provided Context Data below. 
If the answer cannot be found in the context, politely state that you do not have this information.

Context Data:
{knowledge_base}

CRITICAL CONSTRAINT: You must respond ONLY and strictly in the English language. Even if the user asks questions in Roman Urdu or Hindi, your entire response must be written in clear, professional English. Do not use any non-English words under any circumstances."""
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[system_prompt, user_input]
            )
            answer = response.text
        except Exception as e:
            # Agar rate limit aaye to user ko saaf batayein ke thoda ruk jayein
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                answer = "⚠️ *Google Free Tier Quota Alert:* Please wait 30-40 seconds before asking the next question so the free API limit can reset."
            else:
                answer = f"System Connection Alert: {str(e)}"
            
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
