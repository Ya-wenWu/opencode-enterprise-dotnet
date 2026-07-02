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
# 🛡️ 如何在 GitHub 上保護環境變數與機密（Secrets）

在 GitHub 上保護環境變數，最核心的原則就是：**絕對不要將秘密（如密碼、API 金鑰）直接寫在程式碼中並推送到儲存庫（Repository）**。

請透過以下 4 個步驟與功能，來徹底保護您的敏感資料：

---

### 1. 🔑 使用 GitHub Secrets 儲存機密
如果您使用 GitHub Actions 進行自動化部署（CI/CD），請將敏感資料存放在專門的加密欄位中：
*   **操作路徑：** 進入 Repository -> 點選 **Settings** -> 左側 **Secrets and variables** -> 選擇 **Actions**。
*   **儲存方法：** 點選 **New repository secret**，填入金鑰名稱與內容（例如 `AWS_ACCESS_KEY_ID`）。
*   **程式碼調用：** 在 `.github/workflows/` 的 YAML 檔中，使用 `${{ secrets.YOUR_SECRET_NAME }}` 來讀取。GitHub 會自動在 Log 紀錄中將其遮蔽（顯示為 `***`）。

---

### 2. 🙈 使用 `.gitignore` 排除本地環境檔案
在本地開發時，通常會將變數寫在 `.env` 檔案中。請務必確保這個檔案不會被推送到 GitHub：
*   在專案根目錄建立一個名為 `.gitignore` 的文字檔。
*   在裡面加入以下內容：
    ```text
    .env
    .env.local
    .env.*.local
    ```
*   💡 **實用小技巧：** 可以建立一個 `.env.example` 檔案推上 GitHub，裡面只留欄位名稱（例如 `API_KEY=your_key_here`），方便其他開發者複製參考，但不要寫入真實資料。

---

### 3. 🔍 開啟 GitHub Secret Scanning（機密掃描）
GitHub 內建了自動偵測功能，可以在您不小心推上金鑰時發出警告，甚至直接阻斷推送：
*   **操作路徑：** 進入 Repository -> **Settings** -> **Code security and analysis**。
*   **啟用功能：** 找到 **Secret scanning** 並點選 **Enable**。
*   **進階保護：** 勾選 **Push protection**。只要您的程式碼裡包含常見的金鑰格式（如 AWS、Google Cloud 金鑰），GitHub 就會直接拒絕該次 `git push`。

---

### 4. 🚨 萬一不小心外洩了，該怎麼辦？
如果您發現含有秘密的 `.env` 檔已經被推上 GitHub（即使後來刪除，Git 歷史紀錄裡也還看得到）：
1.  **立刻撤銷（Revoke）該金鑰：** 馬上到該服務的後台（如 AWS、OpenAI）把舊金鑰作廢並產生新的。**（最重要的一步！）**
2.  **清理 Git 歷史紀錄：** 使用工具如 `git-filter-repo` 或 `BFG Repo-Cleaner` 來徹底從專案歷史中抹除該檔案。


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## License

MIT
