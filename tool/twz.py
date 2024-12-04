import re
import argparse
import os
from datetime import datetime
from tqdm import tqdm
import time
from flag import FlagPrint


# Config file containing regex patterns
REGEX_PATTERNS = {
    "-e": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",  # Email addresses
    "-p": r"password\s*[:=]\s*([^\s]+)",  # Passwords
    "-ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",  # IP addresses
    "-cfg": r"config\s*[:=]\s*([^\s]+)",  # Server configurations
    "-log": r"\b(?:log|error|server)\b[\w\s]+",  # Server logs
    "-ssh": r"ssh-(rsa|dss|ecdsa|ed25519) [A-Za-z0-9+/=]+",  # SSH keys
    "-dbcfg": r"db\s*config\s*[:=]\s*([^\s]+)",  # Database configuration
    "-sysinfo": r"\b(?:OS|system|kernel)\b[\w\s]+",  # System information
    "-svc": r"\b(?:username|password|credential)\b[\w\s]+",  # Service credentials
    "-dbcred": r"db\s*credential\s*[:=]\s*([^\s]+)",  # Database credentials
    "-dblog": r"\b(?:select|insert|update|delete)\b[\w\s]+",  # Database logs
    "-dbapi": r"api_key\s*[:=]\s*([A-Za-z0-9]{32})",  # API keys in databases
    "-web": r"\b(?:session|cookie|token|portal)\b[\w\s]+",  # Web app data
}


# Function to display loader
def green_loader(task_description="Processing..."):
    print(f"\033[92m{task_description}\033[0m")  # Green text
    for _ in tqdm(range(50), desc="Loading", bar_format="\033[92m{l_bar}{bar}\033[0m"):
        time.sleep(0.05)

# Function to extract data based on pattern
def extract_data(pattern, content):
    matches = re.findall(pattern, content)
    return [match[0] if isinstance(match, tuple) else match for match in matches]

# Function to read file content
def read_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            print("\033[91mError: File contains unsupported characters for UTF-8 encoding.\033[0m")
            return None
    else:
        print(f"\033[91mError: File '{filename}' not found.\033[0m")
        return None

# Function to save results to file
def save_results(filename, results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{os.path.splitext(filename)[0]}_results_{timestamp}.txt"
    try:
        with open(output_file, 'w') as file:
            for option, matches in results.items():
                file.write(f"Option: {option}\n")
                file.write("\n".join(matches) + "\n\n")
        print(f"\033[92mResults saved to {output_file}\033[0m")
    except Exception as e:
        print(f"\033[91mError saving results: {e}\033[0m")

# Main CLI logic
def main():
    parser = argparse.ArgumentParser(description="Extract sensitive data from files based on patterns.")
    parser.add_argument(
        "option",
        type=str,
        help="The search option (e.g., -e, -p, etc.). Use 'all' for all options."
    )
    parser.add_argument("filename", type=str, help="The file to search in.")
    args = parser.parse_args()

    green_loader("Initializing...")

    content = read_file(args.filename)
    if not content:
        return

    results = {}
    if args.option == "all":
        for option, pattern in REGEX_PATTERNS.items():
            matches = extract_data(pattern, content)
            if matches:
                results[option] = matches
    elif args.option in REGEX_PATTERNS:
        pattern = REGEX_PATTERNS[args.option]
        # Using 'grep' command to filter the pattern in the file content
        command = f"cat {args.filename} | grep -oP '{pattern}'"
        matches = os.popen(command).readlines()  # Execute the grep command
        matches = [match.strip() for match in matches]  # Clean the matches
        if matches:
            results[args.option] = matches
    else:
        print(f"\033[91mInvalid option: {args.option}\033[0m")
        return

    if results:
        save_results(args.filename, results)
    else:
        print("\033[91mNo matches found.\033[0m")

if __name__ == "__main__":
    FlagPrint()
    main()
