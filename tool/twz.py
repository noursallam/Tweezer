import re
import os
import sys
import json
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime
from tqdm import tqdm
from flag import FlagPrint

class SensitiveExtractor:
    """
    Sensitive information extraction utility 
    with improved error handling and progress tracking.
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
            format='%(asctime)s - %(levelname)s - %(message)s',
            stream=sys.stderr
        )
        return logging.getLogger(__name__)

    def extract(
        self, 
        content: str, 
        keys: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Extract sensitive patterns from content with progress tracking.
        
        Args:
            content (str): Text content to search
            keys (List[str], optional): Specific keys to extract
        
        Returns:
            Dict[str, List[str]]: Extracted sensitive information
        """
        self.results = {}
        
        # Determine which patterns to search
        search_keys = keys if keys else list(self.PATTERNS.keys())

        # Create a green progress bar
        progress_bar = tqdm(
            search_keys, 
            desc="Scanning", 
            bar_format="{l_bar}{bar}",
            colour='green'
        )

        for key in progress_bar:
            try:
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
                
                # Update progress bar description
                progress_bar.set_description(f"Scanning: {key}")

            except Exception as e:
                self.logger.error(f"Error processing key {key}: {e}")
                continue
            
        # Close the progress bar
        progress_bar.close()

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
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception as e:
            self.logger.error(f"Error creating output directory: {e}")
            return None

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

def fetch_url_content(url: str) -> Optional[str]:
    """
    Fetch content from a given URL.
    
    Args:
        url (str): URL to fetch content from
    
    Returns:
        Optional[str]: Content of the URL or None if fetch fails
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sensitive Information Extractor")
    
    # Create input source group
    parser.add_argument("filename", nargs='?', help="Path to the file to search")
    
    parser.add_argument(
        "-y", "--url", 
        help="URL to extract sensitive information from"
    )
    
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

    try:
        args = parser.parse_args()

        # Validate input
        if not args.filename and not args.url:
            print("Error: Please provide either a filename or a URL.")
            sys.exit(1)
        
        if args.filename and args.url:
            print("Error: Please provide either a filename or a URL, not both.")
            sys.exit(1)

        # Set up logging level
        log_level = logging.DEBUG if args.verbose else logging.INFO

        # Create extractor
        extractor = SensitiveExtractor(log_level)

        # Determine content source
        if args.filename:
            # Read file content
            try:
                with open(args.filename, 'r', encoding='utf-8') as f:
                    content = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.filename}' not found.")
                sys.exit(1)
            except PermissionError:
                print(f"Error: No permission to read file '{args.filename}'.")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected error reading file: {e}")
                sys.exit(1)
        
        elif args.url:
            # Fetch content from URL
            content = fetch_url_content(args.url)
            if not content:
                print("Failed to retrieve content from URL.")
                sys.exit(1)

        # Extract patterns
        results = extractor.extract(content, args.keys)

        # Display and save results
        if results:
            print("\n--- Sensitive Information Found ---")
            for key, matches in results.items():
                print(f"{key.upper()}: {len(matches)} matches")
            
            # Save results
            output_filename = args.filename or "url_content"
            output_file = extractor.save(
                filename=os.path.splitext(os.path.basename(output_filename))[0],
                output_dir=args.output
            )
            
            if output_file:
                print(f"Detailed results saved to {output_file}")
        else:
            print("No sensitive information found.")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    FlagPrint()
    main()

    













