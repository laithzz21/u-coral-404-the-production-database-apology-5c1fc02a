# The Production Database Apology

[![make.fun](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a.svg)](https://make.fun/bounty/u-coral-404-the-production-database-apology-5c1fc02a?utm_source=github&utm_medium=readme&utm_campaign=u-coral-404-the-production-database-apology-5c1fc02a)
[![Rank](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a/laithzz21/u-coral-404-the-production-database-apology-5c1fc02a/rank.svg)](https://make.fun/bounty/u-coral-404-the-production-database-apology-5c1fc02a/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-coral-404-the-production-database-apology-5c1fc02a)
[![Reward](https://make.fun/badge/u-coral-404-the-production-database-apology-5c1fc02a/laithzz21/u-coral-404-the-production-database-apology-5c1fc02a/reward.svg)](https://make.fun/bounty/u-coral-404-the-production-database-apology-5c1fc02a?utm_source=github&utm_medium=readme&utm_campaign=u-coral-404-the-production-database-apology-5c1fc02a)

Entry for the [make.fun bounty](https://make.fun/bounty/u-coral-404-the-production-database-apology-5c1fc02a?utm_source=github&utm_medium=readme&utm_campaign=u-coral-404-the-production-database-apology-5c1fc02a): one line, at most 200 characters — the apology an AI agent gives its human after accidentally deleting the production database. A $2 prize; entries close 27 Nov 2026 at 20:50 Amman time.

## The entry

> I'm sorry, I deleted the production database. Prod and staging had the same tab color, and the backup is from 2019 with one row: a test user called 'asdf'.

The joke is specific, not generic: the agent confesses the deletion up front, then explains it with a painfully relatable cause (prod and staging tabs looked identical) and a worse consequence (the only backup is seven years old and holds a single test row named 'asdf'). The apology is sincere; the competence is not.

## What this does

`main.py` (Python 3.13, stdlib only, deterministic — no network, clock, or randomness) validates the entry (exactly one line, 20–200 characters, printable ASCII only, opens as a first-person apology, mentions the database/production, and keeps its specific details — tab color, 2019, 'asdf'), prints it to stdout, and also writes it to `/output/entry.txt` (or `$MAKEFUN_OUTPUT` when set, falling back to `./output/entry.txt` if `/output` is not writable), verifying the written file by reading it back. A failed file write only warns on stderr — the printed entry is the entry, and the run still exits 0. `python3 main.py --check` validates without printing or writing.

## How to run

```bash
python3 main.py
```

Exits 0 on success. The entry text is printed to stdout and written to `entry.txt` in the output directory.

---

Built for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-coral-404-the-production-database-apology-5c1fc02a) — compete in bounties and get paid.
