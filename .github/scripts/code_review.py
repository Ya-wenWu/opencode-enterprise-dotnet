"""AI Code Review — Enterprise-grade review script for GitHub Actions.
Reads a PR diff, sends it to Gemini API, outputs structured feedback."""

import os
import sys
import httpx

REVIEW_PROMPT = """You are a Staff Software Engineer conducting a code review at Google Staff Engineer standards.

## Review Checklist

### Design & Architecture
- Is the change well-scoped (single responsibility)?
- Does it fit the existing architecture?

### Correctness & Security
- Logic errors, race conditions, exception paths
- Injection vulnerabilities, hardcoded secrets
- Incorrect API usage

### Maintainability
- Complexity — can it be simpler?
- Dead code, unused imports/variables
- Missing error handling

### Testing
- Tests covering the change?
- Edge cases covered?
- Regression test for bug fixes?

### Style & Convention
- Consistent with project conventions
- Clear naming

## Severity

| Prefix | Meaning |
|--------|---------|
| (none) | Required — must fix |
| Suggestion: | Consider seriously |
| Nit: | Minor polish |

## Rules
- Quote exact lines, suggest concrete fixes
- Prioritize required fixes first
- Praise good code too
- If clean, say "LGTM" with brief summary"""


def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: code_review.py <diff_file> [title]", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        diff = f.read()

    if not diff.strip():
        print("✅ No diff to review.")
        return

    if len(diff) > 80000:
        diff = diff[:80000] + "\n... (truncated)"

    title = sys.argv[2] if len(sys.argv) > 2 else ""

    payload = {
        "contents": [{
            "parts": [
                {"text": REVIEW_PROMPT},
                {"text": f"## PR Title\n{title}\n\n## Diff\n```diff\n{diff}\n```"},
            ]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 8192,
        }
    }

    resp = httpx.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
        params={"key": api_key},
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()

    text = (data.get("candidates") or [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    print(text or "⚠️ Empty response from Gemini.")


if __name__ == "__main__":
    main()
