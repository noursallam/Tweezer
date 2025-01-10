# 🔍 Tweezer - Sensitive Information Extractor

![Tweezer Logo](tweezer.png)

## Overview

Tweezer is a powerful Python utility designed to scan and identify potentially sensitive information across various document types and URLs. This tool provides a robust, flexible solution for detecting personal, financial, network, and credential-related data patterns in both local files and web content.

---

## 🌟 Key Features

- **Comprehensive Pattern Matching**: Detects over 20 different types of sensitive information.
- **Configurable Scanning**: Ability to target specific information types.
- **Multiple Input Sources**: Scan both local files and web URLs.
- **Secure Logging**: Detailed logging with configurable verbosity.
- **JSON Output**: Save extraction results in a clean, structured format.
- **Progress Tracking**: Real-time scanning feedback with green progress bar.
- **Color-coded Output**: Enhanced readability of scan results.

---

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Required Python libraries (installed via `setup.sh`)

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/noursallam/Tweezer.git
cd Tweezer/tool

sudo chmod +x setup.sh
./setup.sh

source ~/.bashrc  # or source ~/.zshrc
```

---

## Usage

### File Scanning

Scan a local file:
```bash
tweezer [filename] -k [options]
```

### URL Scanning

Scan a website or web page:
```bash
tweezer -y https://example.com -k [options]
```

### Global Access

The setup script sets up an alias for `tweezer`, enabling global usage.

### Command Line Options
```bash
usage: twz.py [-h] [-y URL] [-k KEYS [KEYS ...]] [-o OUTPUT] [-v] [filename]

options:
  -h, --help            show this help message and exit
  filename              Path to the file to search
  -y, --url URL        URL to extract sensitive information from
  -k, --keys KEYS      Specific keys to extract (e.g., e ph cc ip)
  -o, --output OUTPUT  Output directory for results (default: current directory)
  -v, --verbose        Enable verbose logging
```

---

### Examples

Scan a local file for all patterns:
```bash
tweezer sensitive_data.txt
```

Scan a website for specific patterns:
```bash
tweezer -y https://example.com -k e ph ip
```

Scan a file for credentials with verbose logging:
```bash
tweezer config.txt -k pw ak ssh jwt -v
```

Scan a URL and save results to a specific directory:
```bash
tweezer -y https://example.com -o /path/to/results
```

---

## 📖 Pattern Reference

Tweezer uses sophisticated regular expressions to detect various types of sensitive information:

| Category           | Key   | Description                    | Example                        |
|--------------------|-------|--------------------------------|--------------------------------|
| **Personal Information** |       |                                |                                |
|                    | `e`   | Email Address                  | user@example.com              |
|                    | `ssn` | Social Security Number         | 123-45-6789                   |
|                    | `ph`  | Phone Number                  | +1 (555) 123-4567             |
|                    | `pp`  | Passport Number               | A12345678                     |
|                    | `dl`  | Driver's License Number       | A1234567                      |
| **Credentials**    |       |                                |                                |
|                    | `pw`  | Password                      | password: mypassword123       |
|                    | `ak`  | API Key                       | apikey=12345678abcdefgh       |
|                    | `ssh` | SSH Key                       | -----BEGIN RSA PRIVATE KEY----|
|                    | `jwt` | JWT Token                     | eyJhbGciOiJIUzI1NiI...         |
| **Financial**      |       |                                |                                |
|                    | `cc`  | Credit Card Number            | 4111 1111 1111 1111           |
|                    | `ba`  | Bank Account Number           | 1234567890123456              |
|                    | `rn`  | Routing Number                | 011000015                     |
| **Network**        |       |                                |                                |
|                    | `ip`  | IP Address                    | 192.168.1.1                   |
|                    | `mac` | MAC Address                   | 00:14:22:01:23:45             |
|                    | `url` | URL                           | https://example.com           |
|                    | `dom` | Domain Name                   | example.com                   |
| **Corporate**      |       |                                |                                |
|                    | `eid` | Employee ID                   | EMP12345                      |
|                    | `tax` | Tax ID                        | 12-3456789                    |
| **Cryptocurrency** |       |                                |                                |
|                    | `btc` | Bitcoin Address               | 1A1zP1eP5QGefi2DMPTfTL...     |
|                    | `eth` | Ethereum Address              | 0x32Be343B94f860124dC4...     |

---

## ⚠️ URL Scanning Notes

- The URL scanner respects `robots.txt` and implements rate limiting.
- Only publicly accessible pages can be scanned.
- Network timeouts are handled gracefully.
- URLs must include the protocol (`http://` or `https://`).
- Redirects are followed automatically (up to a maximum of 5 redirects).
- JavaScript-rendered content cannot be scanned.
- Some websites may block automated scanning.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

---

## 📝 License

Copyright (c) 2024, Nour Sallam. All rights reserved.

---

## 📧 Contact

For questions or support:

- Email: noursallam@nspspace.com

---

## ❤️ Support

Don't buy me coffee - Pray for Palestine! 🇵🇸

---

**Note**: This tool is designed for legitimate security assessment purposes only. Use responsibly and in compliance with applicable laws and regulations.
