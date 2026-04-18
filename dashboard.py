from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from job_matcher import CandidateProfile, JobPosting, filter_matching_jobs


st.set_page_config(page_title="Job Automation Dashboard", layout="wide")
st.title("Job Apply Automation Dashboard")
st.caption("Provide your requirements and view jobs that match at least 70%.")


@st.cache_data
def load_jobs(path: str = "sample_jobs.json") -> list[JobPosting]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [JobPosting(**item) for item in raw]


jobs = load_jobs()

st.sidebar.header("Basic Requirements")
years_experience = st.sidebar.number_input(
    "Years of experience", min_value=0.0, max_value=30.0, value=2.0, step=0.5
)
target_titles = st.sidebar.text_input(
    "Job title looking for (comma separated)", value="Python Automation Engineer, QA Automation"
)
core_skills = st.sidebar.text_area(
    "Core skill set (comma separated)", value="Python, Playwright, SQL, API"
)
visa_sponsorship_required = st.sidebar.radio(
    "Apply only for visa sponsored jobs?", options=["Yes", "No"], horizontal=True
)
resume = st.sidebar.file_uploader("Upload resume (PDF/DOC/DOCX)", type=["pdf", "doc", "docx"])

profile = CandidateProfile(
    years_experience=float(years_experience),
    target_titles=[item.strip() for item in target_titles.split(",") if item.strip()],
    visa_sponsorship_required=visa_sponsorship_required == "Yes",
    core_skills=[item.strip() for item in core_skills.split(",") if item.strip()],
    resume_uploaded=resume is not None,
)

matches = filter_matching_jobs(profile=profile, jobs=jobs, minimum_score=70.0)

st.subheader("Matching Jobs (>= 70%)")
if not matches:
    st.warning("No jobs currently meet the 70% threshold. Try adjusting skills or title preferences.")
else:
    rows = []
    for result in matches:
        rows.append(
            {
                "Match %": result.score,
                "Job Title": result.job.title,
                "Company": result.job.company,
                "Location": result.job.location,
                "Min Experience": result.job.min_experience,
                "Visa Sponsorship": "Yes" if result.job.visa_sponsorship else "No",
                "Matched Skills": ", ".join(result.matched_skills),
                "Apply Link": result.job.apply_link,
            }
        )

    frame = pd.DataFrame(rows)
    st.dataframe(frame, use_container_width=True)
    st.metric("Total matching jobs", len(rows))

with st.expander("How this match score is calculated"):
    st.markdown(
        """
        - **30%**: Title match
        - **20%**: Experience match
        - **35%**: Core skill overlap
        - **10%**: Visa sponsorship fit
        - **5%**: Resume uploaded
        """
    )
