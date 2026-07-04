# Account Segmentation & Scoring

Buckets accounts into segments by company size (Enterprise / Mid-Market /
SMB), then combines a segment weight with an incoming buying-signal-strength
score into a single priority score -- so a rep opens their day with a
ranked list instead of an alphabetical one.

See [`example_output.md`](./example_output.md) for a full run, including a
worked example of why the single biggest account in the list isn't ranked
first.

## Segmentation vs. scoring

These are deliberately two different questions:

- **Segment** -- how big is this account / how big could the deal be?
- **Priority score** -- given size AND current buying intent, how much
  attention does this account deserve *this week*?

A big account with zero active signals still matters long-term, but
shouldn't out-rank a smaller account that is actively showing up right now.

## Install

No external dependencies beyond the Python standard library.

## Usage

```bash
python segment_and_score.py --input accounts.json
```

## Project structure

```
segment_and_score.py    -- segmentation + priority scoring + ranking
accounts.json            -- 5 example accounts spanning all three segments
example_output.md        -- full example run with reasoning
```

## Related projects

Signal-strength inputs are meant to come from
[`buying-signals`](https://github.com/highhsenberg/buying-signals) (the
detection layer). This project is the next step: turning raw signal
strength into a ranked, actionable worklist.

## Limitations / next steps

- Segment thresholds and weights are a simple, tunable rubric, not a
  trained model -- the natural next step is fitting them against
  historical won/lost deal data.
- Only employee count drives segmentation today; revenue estimate and
  industry vertical are captured in the data but not yet used in the
  scoring formula.
