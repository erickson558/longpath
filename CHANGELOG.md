# Changelog

All notable changes to this project will be documented in this file.

## V1.0.3 - 2026-03-11

- Updated `app.py` to generate recursive folder trees with long names and long file names.
- Added recursive generation counters in popup summary (files, folders, failures).
- Kept output rooted at `generated_long_paths/` next to `app.py` for ticket validation.

## V1.0.2 - 2026-03-11

- Updated `app.py` to create long-path files physically under `generated_long_paths/` in the project folder.
- Popup now displays generated paths from disk and reports generated/failed counts.
- Updated `.gitignore` to exclude generated stress-test files.

## V1.0.1 - 2026-03-11

- Added configurable massive path generation (default `39090`) in `app.py` to stress popup wrapping.
- Added validation for path count input and warning for very large values.
- Kept wrapping behavior (`wrap=tk.WORD`) for long paths to avoid horizontal scrolling.
- Aligned docs to use `VERSION` as single source of truth.

## V1.0.0 - 2026-03-11

- Initial project setup.
- Added Tkinter app to reproduce and validate long filepath wrapping behavior.
- Added semantic versioning with single source of truth in `VERSION`.
- Added PowerShell build script to generate `.exe` in project root using local `app.ico`.
- Added GitHub Actions workflow to create release on each push to `main`.
- Added Apache License 2.0.
