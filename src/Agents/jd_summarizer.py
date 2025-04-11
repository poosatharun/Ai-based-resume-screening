import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_request import llm

from langchain.prompts import PromptTemplate
# Summarization function
def summarize_jd(jd_text):
    prompt = PromptTemplate.from_template("""
    Extract the following fields from the job description:

    - Job Title
    - Required Skills
    - Experience
    - Qualifications
    - Responsibilities

    Format the output strictly as **minified JSON** with double quotes and no markdown formatting
                                          Do not include any additional text or explanations BEFOR AND AFTER.
    Job Description: {jd_text}
    """)

    return llm.predict(prompt.format(jd_text=jd_text))
