# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-08

### Added

- Initial release of the RRC Field Rules Parser module
- **Core Features**
  - `FieldRulesParser` class for database connectivity and data extraction
  - `ParserConfig` for Pydantic-based configuration with environment variable support
  - Connection pooling via `oracledb`
  - Health check functionality
- **Data Models** (Pydantic v2)
  - `OgField` - Oil & Gas Field master records
  - `OgFieldInfo` - Field information with discovery dates
  - `OgFieldRule` - Field-specific spacing rules
  - `OgStdFieldRule` - Statewide standard rules
- **CLI** (Typer + Rich)
  - `rrc-field-rules check` - Database health check with table counts
  - `rrc-field-rules export` - Export tables to JSON
  - `rrc-field-rules list-tables` - Display available tables
- **Export Capabilities**
  - Export single table or all tables to JSON
  - Optional record limit
  - ISO 8601 date serialization
- **Documentation**
  - Comprehensive README with usage examples
  - Full schema documentation
  - Python API reference
- **Modern Python Packaging**
  - `pyproject.toml` with PEP 621 metadata
  - `hatchling` build backend
  - Development dependencies: pytest, ruff, mypy

### Infrastructure

- Docker Compose setup for Oracle Free container
- Automated data import from Oracle `.dmp` files
- `OracleContainer` helper class for container management

[Unreleased]: https://github.com/username/rrc-field-rules/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/username/rrc-field-rules/releases/tag/v0.1.0
