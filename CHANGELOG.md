# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.0] - 2025-02-15

### Added
- Concurrent link auditing using `ThreadPoolExecutor` for high-performance scanning.
- Export capabilities for JSON and JUnit XML reports to support CI/CD pipelines.
- Command-line flag `--ignore` to skip specific URLs or link patterns.
- Comprehensive unit test suite in `test_auditor.py`.

### Changed
- Enhanced HTTP request verification fallback mechanism from HEAD to GET requests on error codes >= 400.

## [v1.0.0] - 2025-01-01

### Added
- Initial release with recursive directory scanning for Markdown files.
- Basic validation of relative paths and HTTP HEAD checks for absolute URLs.
