"""
Website to Brochure Generator
"""
import os
from brochure import stream_brochure, create_brochure

DEFAULT_URL = os.getenv("DEFAULT_URL", "https://reanblock.com")

def main():
    """Main entry point for testing."""
    url = input(f"Enter a URL to use as content generate the brochure [{DEFAULT_URL}]: ").strip() or DEFAULT_URL
    print("\nFetching and generating...\n")
    # create_brochure("Example Company", url)
    stream_brochure("Example Company", url)

if __name__ == "__main__":
    main()