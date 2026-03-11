# Changelog

All notable changes to this project will be documented in this file.

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
