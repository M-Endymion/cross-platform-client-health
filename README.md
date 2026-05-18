<div align="center">
  <img src="https://raw.githubusercontent.com/M-Endymion/cross-platform-client-health/main/thumbnail.png" alt="Cross-Platform Client Health" width="100%" />
</div>

<br>

# Cross-Platform Client Health Checker

A Python tool to gather system health information across **Windows, macOS, and Linux**.

Built as a companion to my PowerShell MECM/SCCM tools, this project demonstrates cross-platform automation capabilities.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

---

## Features

- Works on Windows, macOS, and Linux
- Checks disk space, memory, CPU, and basic system info
- Generates **JSON** + **HTML** reports
- Easy to extend with more checks (MECM client status, Intune compliance, etc.)

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/M-Endymion/cross-platform-client-health.git
cd cross-platform-client-health

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run it
python client_health.py
```

---

## Example Output

```reports/health_HOSTNAME_20250518_XXXX.json```

```reports/health_HOSTNAME_20250518_XXXX.html``` (nice formatted report)

---

### Roadmap

- Windows-specific MECM/SCCM client checks
- macOS Jamf/Intune status
- CPU temperature & service status
- Optional web dashboard (Streamlit)

---

**Jason Ray** (M-Endymion)
MECM/SCCM Automation & Cross-Platform Scripting

LinkedIn: Jason Ray
Main Portfolio: m-endymion.github.io

Last Updated: May 18, 2026
