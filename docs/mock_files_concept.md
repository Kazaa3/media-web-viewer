# Mock Files Concept

## Purpose
To enable safe, copyright-compliant development and testing, all real media files are excluded from the repository. Instead, a dedicated directory (`media/mock_files/`) is used for mock/test files that are free of copyright restrictions.

## Structure
- `media/cache/` is gitignored and must not contain any files under copyright.
- `media/mock_files/` contains only self-created, open, or generated test files for development and CI.

## Guidelines
- Never add real or copyrighted media to the repository.
- Use only mock/test files in `media/mock_files/` for automated tests and demos.
- Document the origin and license of any file in `media/mock_files/` if not self-generated.

## Rationale
This separation ensures legal compliance, reproducibility, and safe collaboration for all contributors.
