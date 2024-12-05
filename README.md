![Alt Text](tweezer.png)
<br>
Copyright (c) 2024, Nour Sallam. All rights reserved.

# 🔍 Sensitive Information Extractor

## Overview
The **Sensitive Information Extractor** is a powerful Python utility designed to scan and identify potentially sensitive information across various document types. This tool provides a robust, flexible solution for detecting personal, financial, network, and credential-related data patterns.

---

## 🌟 Key Features
- **Comprehensive Pattern Matching**: Detects over 20 different types of sensitive information.
- **Configurable Scanning**: Ability to target specific information types.
- **Secure Logging**: Detailed logging with configurable verbosity.
- **JSON Output**: Save extraction results in a clean, structured format.
- **Progress Tracking**: Green progress bar for real-time scanning feedback.



## 📦 Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- Required Python libraries (see `requirements.txt`)

---

## 🚀 Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/noursallam/Tweezer.git
   cd Tweezer/tool
   

2. **get prim**:
   ```bash
   sudo chmod +x setup/sh
   ./setup.sh
   

- no you can run the tool:
  ```bash
  python twz.py  [filename] -k  [option]


- to make it easy and accecable:
  ```bash
  alaice twz='path to /Tweezer/tool/twz.py'


The **Sensitive Information Extractor** uses regular expressions to detect sensitive information across various document types. Below is a table explaining each pattern used for detection:

| **Pattern** | **Description** | **Example** |
|-------------|-----------------|-------------|
| `e` | Email Address | `user@example.com` |
| `ssn` | Social Security Number | `123-45-6789` |
| `ph` | Phone Number | `+1 (555) 123-4567` |
| `pp` | Passport Number | `A12345678` |
| `dl` | Driver's License Number | `A1234567` |
| `pw` | Password | `password: mypassword123` |
| `ak` | API Key | `apikey=12345678abcdefgh12345678` |
| `ssh` | SSH Key | `-----BEGIN RSA PRIVATE KEY-----\n...` |
| `jwt` | JWT Token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.MSg2KgtuOdTt5qxYZ0Wy8_G9ZTThh7lYqFpt05InHYQ` |
| `cc` | Credit Card Number | `4111 1111 1111 1111` |
| `ba` | Bank Account Number | `1234567890123456` |
| `rn` | Routing Number | `011000015` |
| `ip` | IP Address | `192.168.1.1` |
| `mac` | MAC Address | `00:14:22:01:23:45` |
| `url` | URL | `https://www.example.com` |
| `dom` | Domain Name | `example.com` |
| `eid` | Employee ID | `EMP12345` |
| `tax` | Tax ID | `12-3456789` |
| `btc` | Bitcoin Address | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` |
| `eth` | Ethereum Address | `0x32Be343B94f860124dC4fEe278FDCBD38C102D88` |

---

