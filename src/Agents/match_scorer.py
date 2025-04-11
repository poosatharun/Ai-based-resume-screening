
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm_request import llm

from langchain.prompts import PromptTemplate

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def score1(jd, candidate):
    score = 0.0
    # ----------------- 1. Skill Matching ------------------
    jd_skills = jd.get("required_skills", [])
    cand_skills = candidate.get("skills", [])
    
    if jd_skills and cand_skills:
        # Batch encoding for performance
        jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)
        cand_embeddings = model.encode(cand_skills, convert_to_tensor=True)

        # Cosine similarity matrix (len(jd_skills) x len(cand_skills))
        sim_matrix = util.cos_sim(jd_embeddings, cand_embeddings)

        # Max similarity per JD skill
        max_similarities = sim_matrix.max(dim=1).values

        skill_score = (max_similarities.mean().item()) * 40  # Weighted as 40%
        score += skill_score

    # ----------------- 2. Experience Matching ------------------
    required_exp = jd.get("experience", 0)
    candidate_exp = candidate.get("experience", 0)

    if required_exp > 0:
        exp_score = min(candidate_exp / required_exp, 1.5)  # Cap at 1.5
        exp_score = min(exp_score * 25, 25)  # Max 25 points
        score += exp_score

    # ----------------- 3. Qualification Matching ------------------
    jd_quals = jd.get("qualifications", [])
    cand_edus = candidate.get("education", [])

    if jd_quals and cand_edus:
        qual_embeds = model.encode(jd_quals, convert_to_tensor=True)
        edu_embeds = model.encode(cand_edus, convert_to_tensor=True)

        sim_matrix = util.cos_sim(qual_embeds, edu_embeds)
        match_found = (sim_matrix > 0.7).any().item()

        if match_found:
            score += 20


    return round(score, 2)

# Summarization + Matching Prompt
import re

import re
from langchain.prompts import PromptTemplate

def score2(jd_text, resume_text):
    prompt = PromptTemplate.from_template("""
You are a resume screening expert.

Given:
- Job Description: {jd_text}
- Candidate Resume: {resume_text}

Evaluate how well the candidate's projects and skills align with the job description.

Consider:
- Relevance of technologies and tools
- Domain alignment and job responsibilities
- Quality, recency, and complexity of work experience

Respond with ONLY a number from 0 to 100 representing the overall match percentage.
Do not include any explanation, symbols, or text. Only a number.
""")

    raw_response = llm.predict(prompt.format(jd_text=jd_text, resume_text=resume_text))

    # Extract just the number
    match = re.search(r"\d+", raw_response)
    return int(match.group()) if match else 0



def calculate_match_score_nlp(jd, candidate):
    x=score1(jd, candidate)
    y=score2(jd, candidate)
    return y
