import re
import os
import json
from datetime import datetime

# Patterns for sensitive information
PATTERNS = {
    "e": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",  # Email
    "ph": r"\b(?:\+\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}\b",  # Phone
    "cc": r"\b(?:4\d{3}|5[1-5]\d{2}|6011|3[47]\d{2})\s?\d{4}\s?\d{4}\s?\d{4}\b",  # Credit Card
    "ip": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"  # IP Address
}

def extract_patterns(content, keys=None):
    """
    Extract sensitive information based on patterns.
    Args:
        content (str): The text to search.
        keys (list): Specific keys to extract, or None for all.
    Returns:
        dict: Extracted information grouped by type.
    """
    results = {}
    search_keys = keys or PATTERNS.keys()

    for key in search_keys:
        if key in PATTERNS:
            matches = re.findall(PATTERNS[key], content)
            if matches:
                results[key] = list(set(matches))  # Remove duplicates

    return results

def save_results(results, filename="sensitive_data", output_dir="."):
    """
    Save results to a JSON file.
    Args:
        results (dict): Data to save.
        filename (str): Base name for the file.
        output_dir (str): Directory to save the file.
    Returns:
        str: Path to the saved file.
    """
    if not results:
        print("No sensitive data to save.")
        return None

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"{filename}_{timestamp}.json")

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    print(f"Results saved to {output_path}")
    return output_path

def main():
    """
    Main function to run the extraction process.
    """
    file_path = input("Enter the path to the file: ")
    keys = input("Enter keys to search (e.g., e ph cc ip) or press Enter for all: ").split()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    results = extract_patterns(content, keys if keys else None)

    if results:
        print("\n--- Sensitive Information Found ---")
        for key, matches in results.items():
            print(f"{key}: {matches}")

        save_results(results, filename=os.path.splitext(os.path.basename(file_path))[0])
    else:
        print("No sensitive information found.")

if __name__ == "__main__":
    main()
