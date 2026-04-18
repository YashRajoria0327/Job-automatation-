from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class CandidateProfile:
    years_experience: float
    target_titles: Sequence[str]
    visa_sponsorship_required: bool
    core_skills: Sequence[str]
    resume_uploaded: bool


@dataclass
class JobPosting:
    title: str
    company: str
    location: str
    min_experience: float
    skills: Sequence[str]
    visa_sponsorship: bool
    apply_link: str


@dataclass
class MatchResult:
    job: JobPosting
    score: float
    matched_skills: List[str]


TITLE_WEIGHT = 0.30
EXPERIENCE_WEIGHT = 0.20
SKILLS_WEIGHT = 0.35
VISA_WEIGHT = 0.10
RESUME_WEIGHT = 0.05


def _normalize_tokens(items: Iterable[str]) -> set[str]:
    normalized = set()
    for item in items:
        if not item:
            continue
        token = item.strip().lower()
        if token:
            normalized.add(token)
    return normalized


def calculate_match(profile: CandidateProfile, job: JobPosting) -> MatchResult:
    score = 0.0

    title_tokens = _normalize_tokens(profile.target_titles)
    job_title = job.title.lower()
    if title_tokens and any(token in job_title for token in title_tokens):
        score += TITLE_WEIGHT

    if profile.years_experience >= job.min_experience:
        score += EXPERIENCE_WEIGHT

    candidate_skills = _normalize_tokens(profile.core_skills)
    job_skills = _normalize_tokens(job.skills)
    matched = sorted(candidate_skills.intersection(job_skills))
    if job_skills:
        score += SKILLS_WEIGHT * (len(matched) / len(job_skills))

    if profile.visa_sponsorship_required:
        if job.visa_sponsorship:
            score += VISA_WEIGHT
    else:
        score += VISA_WEIGHT

    if profile.resume_uploaded:
        score += RESUME_WEIGHT

    return MatchResult(job=job, score=round(score * 100, 2), matched_skills=matched)


def filter_matching_jobs(
    profile: CandidateProfile,
    jobs: Sequence[JobPosting],
    minimum_score: float = 70.0,
) -> list[MatchResult]:
    results = [calculate_match(profile, job) for job in jobs]
    filtered = [result for result in results if result.score >= minimum_score]
    return sorted(filtered, key=lambda item: item.score, reverse=True)
