# Job-automatation-

Automation starter for job searching and applying.

## What is included

- A simple job-matching engine (`job_matcher.py`) that scores jobs against your profile.
- A Streamlit dashboard (`dashboard.py`) that asks for:
  - Years of experience
  - Job titles you are looking for
  - Core skill set
  - Whether visa sponsorship is required
  - Resume upload
- A jobs table showing only matches with **70%+ score**.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run dashboard.py
```

## Scoring logic

- 30%: title match
- 20%: experience match
- 35%: skill overlap
- 10%: visa sponsorship fit
- 5%: resume uploaded

You can replace `sample_jobs.json` with real scraped jobs later.
