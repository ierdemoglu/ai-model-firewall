# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-06-11

### Added
- Initial release of AI Model Firewall
- Core pipeline with 5 security modules:
  - Hugging Face Hash Verification
  - VirusTotal Malware Scanning
  - Model Integrity & Safety Checks
  - Pickle Injection Scanner (RCE protection)
  - Disk Space Guard
- Real-time file monitoring with Watchdog
- Automatic directory discovery (LM Studio, Ollama, HF Cache)
- Modern Tkinter GUI + CLI support
- Quarantine system for blocked files
- Desktop notifications

### Security
- Business Source License 1.1 with clear commercial restrictions
- Transparent AI usage disclosure in README
- Responsible disclosure policy via SECURITY.md

---

## [0.9.0] - 2025-06-01 (Pre-release)

### Added
- Initial modular architecture design
- BaseSecurityModule interface
- Hugging Face hash checking module prototype
- Basic file monitoring

### Fixed
- AI-generated race condition bug in file handler (manually reviewed and corrected)

---

*Note: All AI-assisted code sections have been manually audited for security.*