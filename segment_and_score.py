#!/usr/bin/env python3
"""
Account Segmentation & Scoring
---------------------------------
Buckets accounts into segments by company size, then combines a segment
weight with an incoming buying-signal-strength score (see the
`buying-signals` project) into a single priority score -- so a rep opens
their day with a ranked list instead of an alphabetical one.

Segmentation and scoring are deliberately two different questions:
  - Segment: how big is this account / how big could the deal be?
  - Priority score: given size AND current buying intent, how much
    attention does this account deserve *this week*?

A big account with zero active signals still matters long-term, but
shouldn't out-rank a smaller account that is actively showing up right now
-- the scoring below reflects that.

Usage:
    python segment_and_score.py --input accounts.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Any, Dict, List

SEGMENT_THRESHOLDS = [
    (250, "Enterprise"),
    (50, "Mid-Market"),
    (0, "SMB"),
]

SEGMENT_WEIGHTS = {"Enterprise": 40, "Mid-Market": 25, "SMB": 10}
SIGNAL_MULTIPLIER = 5

PRIORITY_TIERS = [
    (50, "Priority A"),
    (25, "Priority B"),
    (0, "Priority C"),
]


@dataclass
class ScoredAccount:
    company: str
    industry: str
    employee_count: int
    segment: str
    signal_strength: float
    priority_score: float
    priority_tier: str


def load_accounts(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def segment_account(employee_count: int) -> str:
    for threshold, segment in SEGMENT_THRESHOLDS:
        if employee_count > threshold:
            return segment
    return "SMB"


def priority_tier(score: float) -> str:
    for threshold, tier in PRIORITY_TIERS:
        if score >= threshold:
            return tier
    return "Priority C"


def score_account(account: Dict[str, Any]) -> ScoredAccount:
    segment = segment_account(account["employee_count"])
    signal_strength = account.get("signal_strength", 0.0)
    score = SEGMENT_WEIGHTS[segment] + signal_strength * SIGNAL_MULTIPLIER
    return ScoredAccount(
        company=account["company"],
        industry=account["industry"],
        employee_count=account["employee_count"],
        segment=segment,
        signal_strength=signal_strength,
        priority_score=score,
        priority_tier=priority_tier(score),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Account Segmentation & Scoring")
    parser.add_argument("--input", default="accounts.json")
    args = parser.parse_args()

    accounts = load_accounts(args.input)
    scored = [score_account(a) for a in accounts]
    scored.sort(key=lambda a: a.priority_score, reverse=True)

    print(f"{'Company':18} {'Segment':12} {'Signal':7} {'Score':7} {'Tier'}")
    print("-" * 60)
    for a in scored:
        print(f"{a.company:18} {a.segment:12} {a.signal_strength:<7} {a.priority_score:<7} {a.priority_tier}")


if __name__ == "__main__":
    main()
