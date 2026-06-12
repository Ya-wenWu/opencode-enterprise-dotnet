# opencode-enterprise-dotnet

Enterprise-grade .NET project template with CI/CD, security scanning,
dependabot, and AI-powered code review.

## Enterprise Standards

| Practice | Tool | When |
|----------|------|------|
| SAST | Roslyn Analyzers + CodeQL | Every build |
| SCA | Dependabot | Weekly |
| Secret scan | Gitleaks | Every PR |
| Code review | Gemini AI | Every PR |
| SBOM | CycloneDX | Every release |
| Signed commits | GPG | Every commit |

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

## Quick Start

```bash
git clone https://github.com/Ya-wenWu/opencode-enterprise-dotnet.git
cd opencode-enterprise-dotnet
dotnet build
dotnet test
```

## Project Structure

```
├── src/
│   └── MyApp/
│       ├── MyApp.csproj
│       ├── Program.cs
│       └── Services/
│           └── GreetingService.cs
├── tests/
│   └── MyApp.Tests/
│       ├── MyApp.Tests.csproj
│       └── GreetingServiceTests.cs
├── specs/                         # SDD specs
├── MyApp.sln
├── .github/
│   └── workflows/
│       ├── ai-code-review.yml     # Gemini AI review on every PR
│       ├── ci.yml                 # Gitleaks + dotnet build + test
│       ├── dependency-review.yml  # Dependency graph check
│       └── release.yml            # SBOM + NuGet publish
├── .gitleaks.toml                 # Secret scanning rules
├── CONTRIBUTING.md                # Contribution guide
├── CODE_OF_CONDUCT.md             # Community guidelines
├── SECURITY.md                    # Security policies
└── LICENSE                        # MIT
```

## Security

This project uses multiple layers of security:

- **Gitleaks** scans every PR for hardcoded secrets
- **Dependabot** automatically opens PRs for outdated dependencies
- **Gemini AI** reviews every PR for security issues
- **Secret scanning + push protection** enabled at GitHub level
- **Branch ruleset** requires PR for all branches
- **GPG-signed commits** verify contributor identity

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## License

MIT
