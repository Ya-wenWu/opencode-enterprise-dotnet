# Version Update Records

| Date | Name | Summary | Author | Notes |
|------|------|---------|--------|-------|
| 2026-06-10 | Initial | Enterprise repo template created | opencode | Base template for all .NET projects |
| 2026-06-10 | Sample Project | Added sample console app (MyApp) + xUnit tests | opencode | Includes GreetingService, Program.cs, Directory.Build.targets for test NoWarn |
| 2026-06-12 | AI Review Groq Fallback | Added Groq as third fallback provider (Gemini → NVIDIA → Groq) | opencode | Rewrote from opencode action to Python script; GROQ_API_KEY; ruleset narrowed to main only |
| 2026-06-12 | Security Fixes | Add .gitleaks.toml; upgrade gitleaks v2→v3; fix SECURITY.md | opencode | Custom secret patterns; latest gitleaks rules; private vulnerability reporting |
