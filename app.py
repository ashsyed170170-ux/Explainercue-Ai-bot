import os
import pypdf  # Nayi library PDF parhne ke liye
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# API Key setup
load_dotenv()
client = OpenAI()

# text file ke bajaye PDF parhne ka naya function
def read_pdf_data(pdf_path="company_data.pdf"):
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = pypdf.PdfReader(file)
            # PDF ke har page par ja kar text nikaalna
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except FileNotFoundError:
        return "Filhal koi data available nahi hai."

# --- Baqi aapka Streamlit UI aur OpenAI ka logic nechy as it is rahega ---
# Bas jahan knowledge_base load ho raha tha, wahan yeh call karein:
# knowledge_base = read_pdf_data("company_data.pdf")
