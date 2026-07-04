# Example run

```
$ python segment_and_score.py --input accounts.json

Company            Segment      Signal  Score   Tier
------------------------------------------------------------
Northwind Data     Mid-Market   8.5     67.5    Priority A
Ledgerline         Enterprise   0       40      Priority B
Fieldworks AI      SMB          4.5     32.5    Priority B
Colby Robotics     Mid-Market   0       25      Priority B
Barrow & Finch     SMB          0       10      Priority C
```

## Why Ledgerline (the biggest account) isn't ranked first

Ledgerline is the largest company in the list (340 employees, Enterprise
segment) but has zero active buying signals right now, so it lands in
Priority B, behind two smaller accounts that are actively showing intent
(Northwind Data's hiring + funding + tech-stack activity, Fieldworks AI's
tech-stack + hiring activity). That's intentional: segment answers "how
big could this deal be," while the combined priority score answers "how
much attention deserves this account *this week*." Ledgerline stays a
good target for a longer-cycle enterprise motion; it just shouldn't crowd
out accounts that are ready to talk now.

Signal-strength inputs here come straight from the `buying-signals`
project's output for Northwind Data and Fieldworks AI -- this project is
the next step in the pipeline after detection.
