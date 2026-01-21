"""Simplified log cleaning helpers for the covering-tracks phase."""

from __future__ import annotations

from typing import Dict, Iterable, List


def detect_log_entries(log_lines: Iterable[str], *, keywords: Iterable[str]) -> List[str]:
    """Return suspicious log lines containing any of the provided keywords."""

    lowered = [keyword.lower() for keyword in keywords]
    flagged: List[str] = []
    for line in log_lines:
        if any(keyword in line.lower() for keyword in lowered):
            flagged.append(line)
    return flagged


def clean_log_entries(log_lines: Iterable[str], *, keywords: Iterable[str]) -> Dict[str, object]:
    """Remove lines matching keywords and return a summary structure."""

    original = list(log_lines)
    flagged = detect_log_entries(original, keywords=keywords)
    cleaned = [line for line in original if line not in flagged]

    return {
        "removed": flagged,
        "cleaned_logs": cleaned,
        "original_count": len(original),
        "removed_count": len(flagged),
    }


__all__ = ["detect_log_entries", "clean_log_entries"]

