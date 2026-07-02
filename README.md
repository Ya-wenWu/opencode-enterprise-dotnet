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

# 駭客與環境變數（Environment Variables）的資安攻防

駭客通常會利用系統的**環境變數**（如 `PATH`）來劫持應用程式執行順序（DLL 挾持或二進位劫持），或是竊取存放在環境變數中未加密的敏感 **API 金鑰**與**密碼**來發動攻擊。保護環境變數是防範資訊外洩的關鍵。

---

## 🛑 常見的攻擊手段

*   **PATH 劫持與執行檔替換：** 當使用者或應用程式呼叫指令時，系統會依照 `PATH` 環境變數中的目錄順序來尋找執行檔。如果駭客能竄改此變數或在順位較高的目錄中放置惡意同名檔案，就能誘騙系統執行惡意程式。
*   **敏感機密（Secrets）外洩：** 將資料庫密碼、雲端權限憑證等敏感資訊直接寫入環境變數（如 CI/CD 流水線或 Vercel 等平台），若未設定為加密（Sensitive），駭客可藉由讀取環境變數的漏洞一併將機密竊出。
*   **記憶體傾印與注入：** 惡意軟體常會掃描進程的記憶體或透過環境變數注入攻擊腳本，以繞過防毒軟體的靜態掃描。

---

## 🛡️ 建議的防禦策略

1.  **限制 PATH 權限：** 嚴格控管能修改系統層級或全域環境變數的管理權限，避免一般使用者目錄被置於執行路徑的首位。
2.  **機密集中管理：** 不要在環境變數中明碼儲存機密，應改用專門的機密管理工具，例如 HashiCorp Vault 或雲端供應商內建的金鑰管理服務（KMS）。
3.  **加密敏感變數：** 在部署應用程式（如 PaaS 平臺）時，務必將包含 API Key 等機密的環境變數設定為「加密（Sensitive）」，防止面板權限被盜導致資料外洩。


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## License

MIT
