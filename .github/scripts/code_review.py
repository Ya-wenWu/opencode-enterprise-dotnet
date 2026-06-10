"""AI Code Review — Enterprise-grade review script for GitHub Actions."""

import os
import sys

import httpx

PROMPT = """You are a Staff Software Engineer conducting code review \
at Google Staff Engineer standards.

## Checklist
- Design: well-scoped, fits architecture
- Correctness: logic errors, edge cases, race conditions
- Security: injection, hardcoded secrets
- Maintainability: can it be simpler? dead code?
- Testing: test coverage, edge cases
- Style: naming, conventions

## Severity
- (none): Required — must fix
- Suggestion: Consider seriously
- Nit: Minor polish

Quote exact lines. Praise good code. If clean, say LGTM."""


def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(
            "⚠️ GOOGLE_API_KEY not available "
            "(fork PR from external contributor). Skipping AI review."
        )
        return
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
        "contents": [{"parts": [
            {"text": PROMPT},
            {"text": f"## PR: {title}\n\n```diff\n{diff}\n```"},
        ]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 8192},
    }
    try:
        resp = httpx.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            params={"key": api_key}, headers={"Content-Type": "application/json"},
            json=payload, timeout=120,
        )
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            print("⚠️ Gemini API rate limit exceeded. Skipping AI review this time.")
            return
        raise
    data = resp.json()
    parts = (data.get("candidates") or [{}])[0].get("content", {}).get("parts", [{}])
    text = parts[0].get("text", "") if parts else ""
    print(text or "⚠️ Empty response.")


if __name__ == "__main__":
    main()
