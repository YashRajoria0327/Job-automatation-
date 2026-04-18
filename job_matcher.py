from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
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


_TITLE_ALIASES = {
    "oci": "oracle cloud infrastructure",
    "dba": "database administrator",
}


def _normalize_token(value: str) -> str:
    normalized = value.strip().lower().replace("_", " ").replace("-", " ")
    return " ".join(normalized.split())


def _normalize_tokens(items: Iterable[str]) -> set[str]:
    normalized = set()
    for item in items:
        if not item:
            continue
        token = _normalize_token(item)
        if token:
            normalized.add(token)
    return normalized


def _expand_aliases(token: str) -> set[str]:
    expanded = {token}
    words = token.split()
    for word in words:
        if word in _TITLE_ALIASES:
            expanded.add(_TITLE_ALIASES[word])
    if token in _TITLE_ALIASES:
        expanded.add(_TITLE_ALIASES[token])
    return expanded


def _title_match_score(target_titles: Sequence[str], job_title: str) -> float:
    if not target_titles:
        return 0.0

    normalized_job_title = _normalize_token(job_title)
    best_score = 0.0

    for raw_target in target_titles:
        target = _normalize_token(raw_target)
        for candidate in _expand_aliases(target):
            if candidate in normalized_job_title:
                best_score = max(best_score, 1.0)
                continue

            sequence_score = SequenceMatcher(None, candidate, normalized_job_title).ratio()
            target_words = set(candidate.split())
            job_words = set(normalized_job_title.split())
            overlap = len(target_words & job_words) / max(1, len(target_words))
            blended_score = max(sequence_score, overlap)
            best_score = max(best_score, blended_score)

    return min(best_score, 1.0)


def calculate_match(profile: CandidateProfile, job: JobPosting) -> MatchResult:
    score = 0.0

    title_score = _title_match_score(profile.target_titles, job.title)
    score += TITLE_WEIGHT * title_score

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
