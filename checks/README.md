# Checks

This folder contains tests that require specific environments or conditions that aren't suitable for the main test suite.

## test_playwright_not_installed.py

This test verifies that the `NotInstalled` proxy works correctly when optional dependencies (like Playwright) are not installed. It should only be run in environments without the optional dependencies installed, which is why it's separated from the main test suite.

The test is run in CI via the `.github/workflows/test-optional-deps.yml` workflow.