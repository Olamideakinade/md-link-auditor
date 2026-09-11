# Markdown Link Auditor

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github)](https://github.com/Olamideakinade/md-link-auditor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

![Project Snapshot](preview.svg)

A command-line utility to verify the validity of links within Markdown files. It checks for broken relative paths and performs HTTP HEAD requests on absolute URLs to confirm reachability.

## Capabilities
- Recursive directory scanning for `.md` files.
- Validates relative file links (checks local filesystem existence).
- Validates absolute URLs (HTTP HEAD requests with timeout).
- Configurable concurrency for network I/O.
- Non-zero exit status on broken links for CI/CD integration.

## Quickstart
```bash
pip install requests
python main.py ./docs
```

## CLI Example
```text
$ python main.py ./content
[PASS] ./content/index.md -> ./about.md
[FAIL] ./content/posts/test.md -> https://example.com/404 (Status: 404)
[PASS] ./content/posts/test.md -> https://google.com (Status: 200)

Audit complete. 2 passed, 1 failed.
```

## License
MIT