from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Sequence

from job_matcher import CandidateProfile, JobPosting


@dataclass
class TailoredResume:
    title: str
    markdown: str


def build_ats_resume(
    full_name: str,
    email: str,
    phone: str,
    profile: CandidateProfile,
    job: JobPosting,
    base_summary: str,
) -> TailoredResume:
    """Generate a simple ATS-focused resume in markdown format."""
    prioritized_skills = [skill for skill in job.skills if skill.lower() in {s.lower() for s in profile.core_skills}]
    missing_skills = [skill for skill in job.skills if skill not in prioritized_skills]

    skills_section = prioritized_skills + missing_skills

    headline = f"{job.title} | {profile.years_experience}+ Years Experience"
    summary = (
        f"{base_summary.strip()} Experienced professional targeting {job.title} roles "
        f"with focus on {', '.join(skills_section[:4])}."
    )

    markdown = "\n".join(
        [
            f"# {full_name}",
            f"**Email:** {email}  ",
            f"**Phone:** {phone}  ",
            f"**Date:** {date.today().isoformat()}  ",
            "",
            f"## Professional Headline\n{headline}",
            "",
            f"## Professional Summary\n{summary}",
            "",
            "## Core Skills",
            *[f"- {skill}" for skill in skills_section],
            "",
            "## Target Role Alignment",
            f"- Job Title: {job.title}",
            f"- Company: {job.company}",
            f"- Required Experience: {job.min_experience}+ years",
            f"- Visa Sponsorship Needed: {'Yes' if profile.visa_sponsorship_required else 'No'}",
            "",
            "## Experience Highlights",
            "- Built and maintained automation workflows to increase process efficiency.",
            "- Collaborated with teams to deliver reliable, scalable job-related tooling.",
            "- Improved quality by implementing test coverage and monitoring.",
            "",
            "## Education",
            "- Add your degree/certification details here.",
        ]
    )

    title = f"ATS_Resume_{job.company.replace(' ', '_')}_{job.title.replace(' ', '_')}.md"
    return TailoredResume(title=title, markdown=markdown)
