import argparse
import os
import re
import sys
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Dict, Any
import requests

LINK_REGEX = re.compile(r'\[.*?\]\((.*?)\)')

class LinkAuditor:
    def __init__(self, root_dir: str, timeout: int = 5, ignore_patterns: List[str] = None):
        self.root_dir = os.path.abspath(root_dir)
        self.timeout = timeout
        self.ignore_patterns = ignore_patterns or []

    def get_markdown_files(self) -> List[str]:
        md_files = []
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        return md_files

    def is_ignored(self, link: str) -> bool:
        for pattern in self.ignore_patterns:
            if pattern in link:
                return True
        return False

    def validate_link(self, base_path: str, link: str) -> Tuple[bool, str]:
        if not link or link.startswith('#'):
            return True, "Ignored anchor or empty link"

        if self.is_ignored(link):
            return True, "Ignored by pattern"

        if link.startswith(('http://', 'https://')):
            try:
                resp = requests.head(link, timeout=self.timeout, allow_redirects=True)
                if resp.status_code >= 400:
                    resp = requests.get(link, timeout=self.timeout, allow_redirects=True)
                if resp.status_code < 400:
                    return True, f"HTTP {resp.status_code}"
                else:
                    return False, f"HTTP {resp.status_code}"
            except requests.RequestException as e:
                return False, f"Request Error: {str(e)}"
        else:
            clean_link = link.split('#')[0]
            if not clean_link:
                return True, "Same-file anchor"
            target_path = os.path.normpath(os.path.join(os.path.dirname(base_path), clean_link))
            if os.path.exists(target_path):
                return True, "Local file exists"
            else:
                return False, f"Local file not found: {target_path}"

    def audit_file(self, file_path: str) -> List[Dict[str, Any]]:
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [{'file': file_path, 'link': '', 'valid': False, 'message': f'Read error: {e}'}]

        matches = LINK_REGEX.findall(content)
        for link in matches:
            valid, message = self.validate_link(file_path, link)
            results.append({
                'file': file_path,
                'link': link,
                'valid': valid,
                'message': message
            })
        return results

    def run(self, max_workers: int = 10) -> List[Dict[str, Any]]:
        files = self.get_markdown_files()
        all_results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.audit_file, f): f for f in files}
            for future in as_completed(futures):
                try:
                    res = future.result()
                    all_results.extend(res)
                except Exception as e:
                    print(f"Error processing file: {e}", file=sys.stderr)
                    
        return all_results

def export_json(results: List[Dict[str, Any]], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

def export_junit(results: List[Dict[str, Any]], output_path: str):
    testsuite = ET.Element('testsuite', name='Markdown Link Auditor', tests=str(len(results)))
    failures = sum(1 for r in results if not r['valid'])
    testsuite.set('failures', str(failures))

    for r in results:
        testcase = ET.SubElement(testsuite, 'testcase', classname=r['file'], name=r['link'])
        if not r['valid']:
            failure = ET.SubElement(testcase, 'failure', message=r['message'])
            failure.text = f"Link '{r['link']}' in {r['file']} failed: {r['message']}"

    tree = ET.ElementTree(testsuite)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

def main():
    parser = argparse.ArgumentParser(description='Audit markdown links for validity.')
    parser.add_argument('directory', nargs='?', default='.', help='Root directory to scan')
    parser.add_argument('--timeout', type=int, default=5, help='HTTP request timeout in seconds')
    parser.add_argument('--workers', type=int, default=10, help='Concurrent worker threads')
    parser.add_argument('--ignore', action='append', default=[], help='Ignore link containing pattern')
    parser.add_argument('--json-output', type=str, help='Export results to JSON file')
    parser.add_argument('--junit-output', type=str, help='Export results to JUnit XML file')

    args = parser.parse_args()

    auditor = LinkAuditor(args.directory, timeout=args.timeout, ignore_patterns=args.ignore)
    results = auditor.run(max_workers=args.workers)

    if args.json_output:
        export_json(results, args.json_output)
        print(f"JSON report saved to {args.json_output}")

    if args.junit_output:
        export_junit(results, args.junit_output)
        print(f"JUnit XML report saved to {args.junit_output}")

    broken_count = sum(1 for r in results if not r['valid'])
    print(f"Audited {len(results)} links. Broken links found: {broken_count}")

    for r in results:
        status = "PASS" if r['valid'] else "FAIL"
        print(f"[{status}] {r['file']} -> {r['link']} ({r['message']})")

    if broken_count > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
