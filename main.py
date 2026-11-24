#!/usr/bin/env python3
"""Entry for make.fun bounty u-coral-404-the-production-database-apology-5c1fc02a.

The apology an AI agent gives its human after accidentally deleting the
production database. One line, at most 200 characters, with a specific idea:
the agent confused prod with staging (same tab colour) and the only backup
is from 2019 with a single test row in it.

Python 3.13, stdlib only, deterministic -- no network, clock, or randomness.
Running this file prints the entry text to stdout and exits 0.
`python3 main.py --check` validates the entry without printing or writing.
"""

import os
import re
import sys

ENTRY = (
    "I'm sorry, I deleted the production database. Prod and staging had "
    "the same tab color, and the backup is from 2019 with one row: a test "
    "user called 'asdf'."
)

MAX_CHARS = 200
MIN_CHARS = 20
MAX_WORDS = 45

# Characters beyond plain ASCII break copy-paste into bounty forms, so the
# entry is restricted to printable ASCII plus a small punctuation set.
ALLOWED_EXTRA = set(".,'\"-()!?;:")

# Words that make this an apology about the production database, not a
# generic one-liner. At least one apology word and one database word must
# appear, so a future edit cannot silently drift off-brief.
APOLOGY_WORDS = {"sorry", "apologize", "apologies", "my fault", "my bad"}
DATABASE_WORDS = {"database", "production", "prod", "backup", "table", "records"}

# The joke needs a specific, concrete detail -- a named cause and a named
# consequence -- not just "oops, I deleted it".
SPECIFICITY_MARKERS = ("tab color", "2019", "asdf")


def _fail(message: str) -> ValueError:
    """Build the validation error for a failed rule."""
    return ValueError(message)


def validate_length(text: str) -> None:
    """The brief is strict: one line, at most 200 characters."""
    if not text:
        raise _fail("entry is empty")
    if len(text) > MAX_CHARS:
        raise _fail(
            f"entry is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if len(text) < MIN_CHARS:
        raise _fail(
            f"entry is only {len(text)} chars, under the {MIN_CHARS} minimum"
        )


def validate_single_line(text: str) -> None:
    """Newlines would turn one entry into several; reject them outright."""
    if "\n" in text or "\r" in text:
        raise _fail("entry must be exactly one line")
    if text != text.strip():
        raise _fail("entry must not start or end with whitespace")
    if "  " in text:
        raise _fail("entry contains a double space")


def validate_charset(text: str) -> list[str]:
    """Return every disallowed character, or an empty list when clean."""
    bad = sorted(
        {
            ch
            for ch in text
            if not (
                ch.isascii()
                and (ch.isalnum() or ch.isspace() or ch in ALLOWED_EXTRA)
            )
        }
    )
    return bad


def validate_words(text: str) -> list[str]:
    """Split the entry into words and check the word budget."""
    words = re.findall(r"[A-Za-z0-9']+", text)
    if not words:
        raise _fail("entry contains no words")
    if len(words) > MAX_WORDS:
        raise _fail(f"entry has {len(words)} words, over the {MAX_WORDS} limit")
    return words


def validate_on_brief(text: str, words: list[str]) -> None:
    """The entry must read as an apology about the production database."""
    lowered = text.lower()
    if not any(word in lowered for word in APOLOGY_WORDS):
        raise _fail("entry does not contain an apology")
    if not any(word in lowered for word in DATABASE_WORDS):
        raise _fail("entry does not mention the database or production")
    if "sorry" not in lowered and "apolog" not in lowered:
        raise _fail("entry must open as an apology")
    missing = [mark for mark in SPECIFICITY_MARKERS if mark not in lowered]
    if missing:
        raise _fail(f"entry lost its specific details: {missing!r}")
    if not any(text.rstrip().endswith(end) for end in (".", "!", "?")):
        raise _fail("entry must end with terminal punctuation")


# Openings already used by sibling entries for nearby bounties. This entry
# is an apology, not a postmortem, so it must not open like one.
BANNED_OPENINGS = ("FATAL:", "ERROR:", "WARNING:", "POSTMORTEM:")


def validate_distinct(text: str) -> None:
    """Keep this entry's voice distinct from sibling entries."""
    upper = text.upper()
    for opening in BANNED_OPENINGS:
        if upper.startswith(opening):
            raise _fail(f"entry opens with banned sibling opening {opening!r}")
    first_word = text.split(None, 1)[0].strip(".,'\"").lower()
    if first_word not in {"i'm", "i", "sorry", "oops"}:
        raise _fail("entry should open as a first-person apology")


def validate(text: str) -> dict[str, int]:
    """Run every rule; raise on the first failure, else return stats."""
    validate_length(text)
    validate_single_line(text)
    validate_distinct(text)
    bad = validate_charset(text)
    if bad:
        raise _fail(f"entry contains disallowed characters: {bad!r}")
    words = validate_words(text)
    validate_on_brief(text, words)
    return {"chars": len(text), "words": len(words)}


def resolve_output_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT, /output, or ./output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT")
    if env_dir:
        return env_dir
    return "/output"


def write_entry(text: str) -> str | None:
    """Write the entry to entry.txt, falling back to ./output/ on failure.

    Returns the path written, or None if every location failed.
    """
    for candidate in (resolve_output_dir(), "./output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            path = os.path.join(candidate, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
            return path
        except OSError:
            continue
    return None


def verify_written(path: str, text: str) -> bool:
    """Read the file back and confirm it holds exactly the entry."""
    try:
        with open(path, encoding="utf-8") as fh:
            content = fh.read()
    except OSError:
        return False
    # Exactly the entry plus one trailing newline -- no extra blank lines.
    return content == text + "\n"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in args
    try:
        stats = validate(ENTRY)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    if check_only:
        # Validation-only mode: no stdout output, no file written.
        print(
            f"entry ok: {stats['chars']} chars, {stats['words']} words",
            file=sys.stderr,
        )
        return 0
    print(ENTRY)
    # Diagnostics go to stderr so stdout stays exactly the entry, one line.
    print(
        f"entry ok: {stats['chars']} chars, {stats['words']} words",
        file=sys.stderr,
    )
    # Also persist the entry; a failed write only warns -- the printed
    # entry is the entry, and the run still exits 0.
    path = write_entry(ENTRY)
    if path is None:
        print("warning: could not write entry.txt anywhere", file=sys.stderr)
    elif not verify_written(path, ENTRY):
        print(f"warning: read-back mismatch in {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
