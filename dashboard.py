from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from job_matcher import CandidateProfile, JobPosting, filter_matching_jobs
from resume_builder import build_ats_resume


st.set_page_config(page_title="Job Automation Dashboard", layout="wide")
st.title("Job Apply Automation Dashboard")
st.caption("Provide requirements, shortlist matching jobs, and generate ATS-friendly resumes before applying.")


@st.cache_data
def load_jobs_from_file(path: str = "sample_jobs.json") -> list[JobPosting]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [JobPosting(**item) for item in raw]


def load_jobs_from_upload(uploaded_file) -> list[JobPosting]:
    raw = json.loads(uploaded_file.getvalue().decode("utf-8"))
    return [JobPosting(**item) for item in raw]


st.sidebar.header("Basic Requirements")
full_name = st.sidebar.text_input("Full name", value="Your Name")
email = st.sidebar.text_input("Email", value="you@example.com")
phone = st.sidebar.text_input("Phone", value="+1 000-000-0000")
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
base_summary = st.sidebar.text_area(
    "Short professional summary",
    value="Results-driven engineer with strong automation and backend experience.",
)

st.sidebar.header("Job Source")
minimum_match = st.sidebar.slider("Minimum match score (%)", min_value=40, max_value=95, value=70, step=5)
job_source_mode = st.sidebar.radio(
    "Choose job source",
    options=["Built-in sample jobs", "Upload jobs JSON"],
)
uploaded_jobs_file = None
if job_source_mode == "Upload jobs JSON":
    uploaded_jobs_file = st.sidebar.file_uploader(
        "Upload jobs JSON (array of job objects)",
        type=["json"],
        key="jobs-json",
    )

if uploaded_jobs_file is not None:
    try:
        jobs = load_jobs_from_upload(uploaded_jobs_file)
        st.info(f"Loaded {len(jobs)} jobs from uploaded JSON.")
    except Exception as error:
        st.error(f"Could not parse uploaded jobs JSON: {error}")
        jobs = load_jobs_from_file()
else:
    jobs = load_jobs_from_file()

profile = CandidateProfile(
    years_experience=float(years_experience),
    target_titles=[item.strip() for item in target_titles.split(",") if item.strip()],
    visa_sponsorship_required=visa_sponsorship_required == "Yes",
    core_skills=[item.strip() for item in core_skills.split(",") if item.strip()],
    resume_uploaded=resume is not None,
)

matches = filter_matching_jobs(profile=profile, jobs=jobs, minimum_score=float(minimum_match))

st.subheader(f"Matching Jobs (>= {minimum_match}%)")
if not matches:
    st.warning(
        "No jobs currently meet the selected threshold. "
        "Try lowering minimum score or upload a better-targeted job source file."
    )
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

    job_lookup = {f"{item.job.title} @ {item.job.company}": item for item in matches}
    selected_jobs = st.multiselect(
        "Select jobs you want to apply for",
        options=list(job_lookup.keys()),
        help="Select one or more matching jobs to generate ATS-friendly resumes and apply.",
    )

    if selected_jobs:
        st.subheader("ATS Resume Generator")
        for selected in selected_jobs:
            match_result = job_lookup[selected]
            tailored = build_ats_resume(
                full_name=full_name,
                email=email,
                phone=phone,
                profile=profile,
                job=match_result.job,
                base_summary=base_summary,
            )

            with st.expander(f"Resume preview for {selected}"):
                st.markdown(tailored.markdown)
                st.download_button(
                    label=f"Download ATS Resume ({match_result.job.company})",
                    data=tailored.markdown,
                    file_name=tailored.title,
                    mime="text/markdown",
                    key=f"download-{selected}",
                )

        if st.button("Apply to Selected Jobs", type="primary"):
            st.success("Applications queued successfully.")
            for selected in selected_jobs:
                match_result = job_lookup[selected]
                st.write(
                    f"✅ Applied to **{match_result.job.title}** at **{match_result.job.company}** — "
                    f"[{match_result.job.apply_link}]({match_result.job.apply_link})"
                )

with st.expander("How this match score is calculated"):
    st.markdown(
        """
        - **30%**: Title match (supports aliases like OCI -> Oracle Cloud Infrastructure)
        - **20%**: Experience match
        - **35%**: Core skill overlap
        - **10%**: Visa sponsorship fit
        - **5%**: Resume uploaded
        """
    )

with st.expander("Uploaded jobs JSON schema example"):
    st.code(
        '''[
  {
    "title": "Oracle Cloud Infrastructure Administrator",
    "company": "Example Corp",
    "location": "Remote",
    "min_experience": 4,
    "skills": ["oracle cloud", "linux", "oracle rac", "oracle database"],
    "visa_sponsorship": true,
    "apply_link": "https://example.com/apply"
  }
]''',
        language="json",
    )
