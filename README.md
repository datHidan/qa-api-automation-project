# 🚀 QA API Automation Project

A portfolio-ready API test automation project built with modern Python tools.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-PyTest-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

This project demonstrates a complete, production-grade API test automation setup:

* **Local Mock API:** Built with **FastAPI** to simulate real-world endpoints.
* **Automatic Orchestration:** Server startup and teardown via PyTest fixtures.
* **Authentication:** Full Bearer token flow implementation.
* **Data Driven:** Test data management using JSON files.
* **Contract Testing:** Schema validation using `jsonschema`.
* **CI/CD:** Automated pipeline with **GitHub Actions**.
* **Reporting:** Detailed HTML test reports generated after execution.

---

## 🏗 Architecture & Flow

```mermaid
graph TD
    subgraph Local_or_CI_Environment
        A[PyTest Runner] --> B[Fixture: Start FastAPI Server]
        B --> C[Fixture: Auth & Token Acquisition]
        C --> D{Execute Test Suite}
        D --> E[test_login.py]
        D --> F[test_users.py]
        E --> G[PyTest Teardown]
        F --> G
        G --> H[Fixture: Stop FastAPI Server]
        H --> I[Generate HTML Report]
    end
📁 Project Structure
Plaintext
qa-api-automation-project/
├── .github/workflows/
│   └── ci.yml             # GitHub Actions CI configuration
├── app/                   # FastAPI mock backend
│   ├── main.py
│   ├── schemas.py
│   └── store.py
├── data/
│   └── credentials.json   # Test data & environment variables
├── src/
│   └── api_client.py      # API client abstraction (Requests wrapper)
├── tests/
│   ├── conftest.py        # Shared fixtures & server lifecycle
│   ├── test_login.py      # Auth-specific scenarios
│   └── test_users.py      # CRUD & User management scenarios
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
🚀 How to Run Locally
1️⃣ Setup Virtual Environment
Windows:

Bash
python -m venv .venv
.venv\Scripts\Activate.ps1
Linux/Mac:

Bash
python -m venv .venv
source .venv/bin/activate
2️⃣ Install Dependencies
Bash
pip install -r requirements.txt
3️⃣ Run Tests
The FastAPI server is automatically started and stopped by the PyTest lifecycle.

Bash
python -m pytest -v
🧪 Reporting & Auth
Generate HTML Test Report
To generate a standalone, styled report, run:

Bash
python -m pytest --html=report.html --self-contained-html
Pak otevři soubor report.html v prohlížeči.

🔐 Authentication Flow
/api/login vrací dočasný Bearer token.

Chráněné endpointy vyžadují hlavičku: Authorization: Bearer <token>.

Token je automaticky spravován a injektován do testů přes fixture auth_api.

🧱 Test Strategy
Positive/Negative Scenarios: Validace očekávaného chování i chybových stavů.

Security: Ověření neautorizovaného přístupu (401).

Edge Cases: Validace nenalezených zdrojů (404) a nevalidních dat.

Schema Validation: Kontrola, zda odpovědi odpovídají JSON schématu.

Isolation: Nezávislá testovací data a čistý teardown pro každý běh.

🔄 CI Pipeline
GitHub Actions workflow běží při každém pushi:

Setup: Příprava Python prostředí.

Dependencies: Instalace knihoven.

Execution: Spuštění PyTest suite (včetně automatického startu API).

Artifacts: Nahrání HTML reportu pro audit.

🎯 Key Skills Demonstrated
Frameworks: PyTest, FastAPI, Requests.

Architecture: Page Object Model (POM) koncept aplikovaný na API.

DevOps: GitHub Actions, automatizace serverových procesů.

Quality: JSON Schema validation, CI/CD integrace.

👤 Author
Jiří Kodejš QA Engineer