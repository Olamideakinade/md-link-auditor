import argparse
import os
import re
import sys
import requests
from typing import List, Tuple

LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)')

def get_markdown_files(root_dir: str) -> List[str]:
    md_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def validate_link(base_path: str, link: str) -> Tuple[bool, str]:
    if link.startswith(('http://', 'https://')):
        try:
            resp = requests.head(link, timeout=5, allow_redirects=True)
            return resp.status_code < 400, f"Status: {resp.status_code}"
        except Exception as e:
            return False, str(e)
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(base_path), link))
        return os.path.exists(target), "File exists" if os.path.exists(target) else "File not found"

def main():
    parser = argparse.ArgumentParser(description='Audit markdown links.')
    parser.add_argument('path', help='Directory to scan')
    args = parser.parse_args()

    files = get_markdown_files(args.path)
    failed = 0
    passed = 0

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            links = LINK_REGEX.findall(content)
            for link in links:
                success, msg = validate_link(filepath, link)
                if success:
                    print(f"[PASS] {filepath} -> {link}")
                    passed += 1
                else:
                    print(f"[FAIL] {filepath} -> {link} ({msg})")
                    failed += 1

    print(f"\nAudit complete. {passed} passed, {failed} failed.")
    sys.exit(1 if failed > 0 else 0)

if __name__ == '__main__':
    main()