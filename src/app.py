import streamlit as st
import os
import tempfile
import json
from Agents.jd_summarizer import summarize_jd
from Agents.cv_parser import extract_text_from_pdf, parse_cv
from Agents.match_scorer import calculate_match_score_nlp
from Agents.send_email import send_interview_email_rest_api



from datetime import datetime, timedelta, time as dtime

# Define auto scheduling slots (you can customize)
def generate_interview_slots(start_date, count):
    time_slots = [
        dtime(10, 0),
        dtime(11, 30),
        dtime(14, 0),
        dtime(15, 30)
    ]
    slots = []
    day = start_date
    i = 0
    while len(slots) < count:
        for t in time_slots:
            slots.append((day, t))
            if len(slots) == count:
                break
        day += timedelta(days=1)
    return slots


# Threshold for shortlisting
SHORTLIST_THRESHOLD = 80

st.set_page_config(page_title="Job Screening AI", layout="wide")
st.title("🤖 AI-Powered Job Screening System")

# Step 1: Upload JD
st.subheader("📄 Upload Job Description")
jd_file = st.file_uploader("Upload a Job Description (TXT)", type=["txt"])

# Step 2: Upload Resumes
st.subheader("👤 Upload Candidate CVs (PDF)")
cv_files = st.file_uploader("Upload one or more CVs", type=["pdf"], accept_multiple_files=True)

# Step 3: Run Matching
if jd_file and cv_files and st.button("Run Screening"):
    jd_text = jd_file.read().decode("utf-8")
    jd_summary = json.loads(summarize_jd(jd_text))
    st.write(jd_summary)
    st.success("✅ JD Summarized Successfully!")
    shortlisted = []
    for file in cv_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        cv_text = extract_text_from_pdf(tmp_path)
        candidate_data = json.loads(parse_cv(cv_text))
        score = calculate_match_score_nlp(jd_summary, candidate_data)
        candidate_data["match_score"] = score
        candidate_data["name"] = candidate_data.get("name", file.name.replace(".pdf", ""))

        st.markdown(f"### 🎯 Candidate: `{candidate_data['name']}`")

        if score >= SHORTLIST_THRESHOLD:
            shortlisted.append(candidate_data)
            st.success(f"✅ Shortlisted (Score: {score})")
        else:
            st.warning(f"❌ Not Shortlisted (Score: {score})")

    # Step 4: Schedule Interviews for Shortlisted Candidates
    # Step 4: Schedule Interviews for Shortlisted Candidates
    # Auto-generate interview slots starting from tomorrow

    auto_slots = generate_interview_slots(datetime.today().date() + timedelta(days=1), len(shortlisted))
    i = 0
    st.write(shortlisted)

    if shortlisted:
        st.subheader("📧 Schedule Interviews for Shortlisted Candidates")

        for candidate in shortlisted:
            auto_date, auto_time = auto_slots[i]
            i += 1

            email = candidate.get("email", "N/A")
            if email == "N/A":
                st.warning(f"❌ Candidate {candidate['name']} does not have a valid email.")
                continue

            platform = st.selectbox(f"Select Interview Platform for {candidate['name']}", ["Zoom", "Google Meet", "In-Person"])
            interviewer = st.text_input(f"Enter Interviewer Name for {candidate['name']}", "HR Team")

            interview_details = {
                "Candidate Name": candidate['name'],
                "Candidate Email": email,
                "Job Title": jd_summary.get("Job Title", "N/A"),
                "Interview Date": str(auto_date),
                "Interview Time": auto_time.strftime("%I:%M %p"),
                "Interview Format": "Virtual" if platform != "In-Person" else "In-Person",
                "Platform": platform,
                "Interviewer": interviewer
            }

            # Print all details for transparency/debug
            st.markdown("### 📄 Interview Details")
            for key, value in interview_details.items():
                st.write(f"**{key}:** {value}")

            success = send_interview_email_rest_api(
                candidate_name=interview_details["Candidate Name"],
                candidate_email="tharun.posa@gmail.com",
                job_title=interview_details["Job Title"],
                interview_date=interview_details["Interview Date"],
                interview_time=interview_details["Interview Time"],
                format_type=interview_details["Interview Format"],
                platform=interview_details["Platform"],
                interviewer_name=interview_details["Interviewer"]
            )

            if success:
                st.success("📨 Email sent successfully via Brevo API!")
            else:
                st.error("❌ Failed to send email using Brevo API. Check API key or sender email.")
