# Job-automatation-

Automation starter for job searching and applying.

## What this project does

This project helps you:
- Capture your job application preferences (experience, job title, skills, visa support, resume).
- Match your profile to available jobs using a weighted score.
- Show jobs using an adjustable match score threshold (default **70%**).
- Select matched jobs and click one button to apply.
- Generate ATS-friendly resumes customized for each selected job.

---

## How it works (end-to-end)

1. **Input profile & preferences** in the Streamlit sidebar:
   - Full name, email, phone
   - Years of experience
   - Desired job titles
   - Core skill set
   - Visa sponsorship requirement
   - Resume file upload
2. **Match engine runs** against available jobs from built-in sample data or uploaded JSON source.
3. **Dashboard filters results** based on your selected minimum score.
4. You **select jobs** you want to apply to.
5. The app **builds ATS-friendly resumes** for each selected role.
6. You click **Apply to Selected Jobs** to queue/apply.

---

## Match scoring formula

The scoring is weighted as follows:
- **30%** Title match
- **20%** Experience match
- **35%** Skill overlap
- **10%** Visa sponsorship fit
- **5%** Resume uploaded

Jobs below 70% are excluded from the final dashboard table.

---

## Project structure

```text
Job-automatation-/
├── dashboard.py         # Streamlit application UI and apply flow
├── job_matcher.py       # Candidate/job data models + match scoring
├── resume_builder.py    # ATS resume generation logic
├── sample_jobs.json     # Sample job dataset (replace with real jobs later)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

---

## Prerequisites

Before running the application, install:
- **Python 3.10+** (recommended 3.11+)
- **pip** (comes with Python in most installations)
- A terminal (Linux/macOS shell, or Windows PowerShell)

Optional but recommended:
- `venv` for isolated environment
- Git for version control

---

## Environment setup

From project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Run the application

Start Streamlit:

```bash
streamlit run dashboard.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

---

## How to use the dashboard

1. Fill all required profile and job preference fields in the sidebar.
2. Review the **Matching Jobs (>=70%)** table.
3. Select one or more jobs in **Select jobs you want to apply for**.
4. Expand each resume preview and download ATS resume if needed.
5. Click **Apply to Selected Jobs**.
6. Confirm application success entries in the output section.

---

## Data source and customization

By default jobs are loaded from `sample_jobs.json`.
You can also upload a custom JSON file in the sidebar (**Upload jobs JSON**) without restarting the app.

Tip: If you are not seeing relevant jobs, either upload a better source file or lower the minimum match slider to 60-65%.

Expected JSON fields per job:
- `title`
- `company`
- `location`
- `min_experience`
- `skills` (array)
- `visa_sponsorship` (true/false)
- `apply_link`

---

## Dependencies

- `streamlit`
- `pandas`

Installed from:

```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### 1) `streamlit: command not found`
Use:
```bash
python -m streamlit run dashboard.py
```

### 2) No jobs displayed
- Make sure your inputs are not too restrictive.
- Confirm that jobs in `sample_jobs.json` include your target skills/title.

### 3) Import errors
- Ensure virtual environment is activated.
- Reinstall dependencies:
```bash
pip install -r requirements.txt
```

---


## CI / Build checks

This repository now includes `pyproject.toml`, so GitHub Actions jobs that run `python -m build` (or package build checks) succeed on Python 3.9+ environments.

Local validation command:

```bash
python -m pip install --upgrade build
python -m build
```

---

## Next enhancements

- Integrate real-time job scraping from job boards.
- Persist applications to a database.
- Add status tracking (Applied / Interview / Rejected / Offer).
- Integrate email notifications and follow-up reminders.
