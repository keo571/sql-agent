# Changelog

All notable changes to the SQL Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- (Future improvements will be listed here)

### Changed
- (Future changes will be listed here)

## [0.2.0] - 2024-12-17

### Added
- Enhanced relevancy analyzer for intelligent table selection
- Robust case-insensitive query handling
- Context-aware prompt generation system

### Improved
- Query accuracy through better schema relevance detection
- User experience with flexible case input handling
- Performance optimization by reducing unnecessary token usage
- JOIN detection capabilities for complex queries

### Technical Details
- Implemented advanced query analysis to determine table relevance
- Added case-insensitive matching for database values and user input
- Optimized prompt generation to include only necessary schema information
- Enhanced error handling and validation

## [0.1.0] - 2024-12-01 (Initial Release)

### Added
- Basic natural language to SQL query conversion
- Dynamic prompt generation based on query context
- Schema-aware query generation
- Interactive web interface
- Support for SQL queries with JOINs
- Schema information retrieval
- Error handling and validation

---

## How to Use This Changelog

### When making changes:
1. Add new items under the **[Unreleased]** section
2. Use appropriate categories (Added, Changed, Fixed, etc.)
3. When ready to release, move items from [Unreleased] to a new dated version

### Categories:
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities
- **Improved** for enhancements to existing features

### Date Format:
- Use YYYY-MM-DD format for consistency
- Add dates when you tag/release a version
- Keep [Unreleased] for ongoing work 