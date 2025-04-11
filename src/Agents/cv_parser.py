import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_request import llm

from langchain.prompts import PromptTemplate

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Summarization function
def parse_cv(text):
    prompt = PromptTemplate.from_template("""
Extract the following fields from the resume text:
- Name
- Email
- Skills
- Experience (in years)
- Qualifications
- Projects

Only respond with **strict, valid minified JSON** (no markdown, no explanation, no formatting).

Resume Text: {text}
""")
    raw = llm.predict(prompt.format(text=text))
    return raw
