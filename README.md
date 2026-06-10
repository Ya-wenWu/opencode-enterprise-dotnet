# Project Name

<!-- Describe your project in 2-3 sentences -->

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

## Quick Start

```bash
git clone <repo-url>
cd <repo-name>
dotnet build
dotnet test
```

## Enterprise Standards

| Practice | Tool | When |
|----------|------|------|
| SAST | Roslyn Analyzers + CodeQL | Every build |
| SCA | Dependabot | Weekly |
| Secret scan | Gitleaks | Every PR |
| Code review | Gemini AI | Every PR |
| SBOM | CycloneDX | Every release |
| Signed commits | GPG | Every commit |

## Project Structure

```
├── src/          # Source code
├── tests/        # Tests
├── specs/        # SDD specs
└── .github/      # CI/CD + policies
```

## License

MIT
