---
trigger: model_decision
description: For writing or updating tests
---

# Running tests
1. Use venv for running tests: `cmd /c "call venv\Scripts\activate.bat && pytest -s test-src"`
2. Always run tests you just wrote. Fix code until tests pass.

# Writing tests
1. Don't write SQL inside tests. All queries should be written inside project repositories, and methods are called in tests.