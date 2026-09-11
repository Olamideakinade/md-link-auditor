# Markdown Link Auditor

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Olamideakinade/md-link-auditor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

![Project Snapshot](preview.svg)

A command-line utility to verify the validity of links within Markdown files. It checks for broken relative paths and performs HTTP requests on absolute URLs to confirm reachability.

## Capabilities
- Recursive directory scanning for `.md` files
- Multithreaded concurrent verification
- Export reports in JSON and JUnit XML formats
- Configurable timeout and ignore patterns via CLI flags

## Installation & Usage

```bash
pip install requests
python main.py /path/to/docs --workers 20 --json-output report.json
```
