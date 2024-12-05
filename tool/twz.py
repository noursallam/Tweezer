import re
import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from tqdm import tqdm
from flag import FlagPrint

class SensitiveExtractor:
    """
    Simplified sensitive information extraction utility 
    with easy-to-use pattern matching.
    """

    PATTERNS = {
        # Personal Info
        "e": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",  # Email
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",  # Social Security Number
        "ph": r"\b(?:\+\d{1,2}\s?)?(\(?\d{3}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}\b",  # Phone
        "pp": r"\b[A-Z]{1,2}\d{6,9}\b",  # Passport
        "dl": r"\b[A-Z]{1,2}\d{4,9}\b",  # Driver's License

        # Credentials
        "pw": r"(?:password|pwd)\s*[:=]\s*([^\s]{8,})",  # Password
        "ak": r"(?:api_key|apikey)\s*[:=]\s*([A-Za-z0-9_\-]{32,})",  # API Key
        "ssh": r"-----BEGIN (RSA|DSA|ECDSA|ED25519) PRIVATE KEY-----[\s\S]*?-----END (RSA|DSA|ECDSA|ED25519) PRIVATE KEY-----",  # SSH Key
        "jwt": r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",  # JWT Token

        # Financial
        "cc": r"\b(?:4\d{3}|5[1-5]\d{2}|6011|3[47]\d{2})\s?\d{4}\s?\d{4}\s?\d{4}\b",  # Credit Card
        "ba": r"\b\d{9,18}\b",  # Bank Account
        "rn": r"\b(?:0[0-9]|1[0-2]|2[1-9]|3[0-2]|6[1-9]|7[0-2]|8[0-8])\d{7}\b",  # Routing Number

        # Network
        "ip": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",  # IP Address
        "mac": r"\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b",  # MAC Address
        "url": r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",  # URL
        "dom": r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\b",  # Domain

        # Corporate
        "eid": r"\b(?:EMP|STAFF)\d{4,6}\b",  # Employee ID
        "tax": r"\b\d{2}-\d{7}\b",  # Tax ID

        # Crypto
        "btc": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",  # Bitcoin Address
        "eth": r"\b0x[a-fA-F0-9]{40}\b",  # Ethereum Address
    }


    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize the Sensitive Extractor.
        
        Args:
            log_level (int): Logging level for the extractor
        """
        self.logger = self._setup_logging(log_level)
        self.results: Dict[str, List[str]] = {}

    def _setup_logging(self, log_level: int) -> logging.Logger:
        """Configure logging for the extractor."""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def extract(
        self, 
        content: str, 
        keys: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Extract sensitive patterns from content.
        
        Args:
            content (str): Text content to search
            keys (List[str], optional): Specific keys to extract
        
        Returns:
            Dict[str, List[str]]: Extracted sensitive information
        """
        self.results = {}
        
        # Determine which patterns to search
        search_keys = keys if keys else list(self.PATTERNS.keys())

        for key in search_keys:
            if key not in self.PATTERNS:
                self.logger.warning(f"Key '{key}' not found")
                continue

            pattern = self.PATTERNS[key]
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            
            # Flatten matches if they are tuples
            if matches and isinstance(matches[0], tuple):
                matches = [match[0] for match in matches]
            
            # Remove duplicates while preserving order
            matches = list(dict.fromkeys(matches))
            
            if matches:
                self.results[key] = matches

        return self.results


    

    def save(
        self, 
        filename: Optional[str] = None, 
        output_dir: str = '.'
    ) -> Optional[str]:
        """
        Save extraction results to a JSON file.
        
        Args:
            filename (str, optional): Base filename for output
            output_dir (str, optional): Directory to save results
        
        Returns:
            Optional[str]: Path to saved results file
        """
        if not self.results:
            self.logger.warning("No sensitive data to save")
            return None

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = filename or "sensitive_data"
        output_filename = os.path.join(
            output_dir, 
            f"{base_name}_sensitive_{timestamp}.json"
        )

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            
            self.logger.info(f"Results saved to {output_filename}")
            return output_filename
        
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
            return None

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Sensitive Information Extractor")
    parser.add_argument("filename", help="Path to the file to search")
    parser.add_argument(
        "-k", "--keys", 
        nargs='+', 
        help="Specific keys to extract (e.g., e ph cc ip)"
    )
    parser.add_argument(
        "-o", "--output", 
        default='.', 
        help="Output directory for results"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set up logging level
    log_level = logging.DEBUG if args.verbose else logging.INFO

    # Create extractor
    extractor = SensitiveExtractor(log_level)

    # Read file content
    try:
        with open(args.filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Extract patterns
    results = extractor.extract(content, args.keys)

    # Display and save results
    if results:
        print("\n--- Sensitive Information Found ---")

        
        # Save results
        extractor.save(
            filename=os.path.splitext(os.path.basename(args.filename))[0],
            output_dir=args.output
        )
    else:
        print("No sensitive information found.")

if __name__ == "__main__":
    FlagPrint()
    main()