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

---

## 🛠 Supported Sensitive Information Types
### Personal Information
- Email Addresses  
- Social Security Numbers  
- Phone Numbers  
- Passport Numbers  
- Driver's Licenses  

### Credentials
- Passwords  
- API Keys  
- SSH Keys  
- JWT Tokens  

### Financial Data
- Credit Card Numbers  
- Bank Account Numbers  
- Routing Numbers  

### Network Information
- IP Addresses  
- MAC Addresses  
- URLs  
- Domain Names  

### Corporate Identifiers
- Employee IDs  
- Tax IDs  

### Cryptocurrency
- Bitcoin Addresses  
- Ethereum Addresses  

---

## 📦 Prerequisites
- **Python 3.8+**
- **pip** (Python package manager)
- Required Python libraries (see `requirements.txt`)

---

## 🚀 Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sensitive-info-extractor.git
   cd sensitive-info-extractor
