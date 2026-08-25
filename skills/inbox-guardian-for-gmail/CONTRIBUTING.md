# Contributing to Gmail Guardian

Thank you for your interest in contributing! We welcome bug fixes, documentation improvements, and test coverage additions.

---

## 🛠️ Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/gmail-guardian.git
   cd gmail-guardian
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

---

## 🧪 Running Tests

We maintain strict unit test coverage for classification precedence, sanitizer functions, and API error resilience:

```bash
# Run all unit tests
pytest tests/ -v

# Run tests with coverage report
pytest --cov=guardian --cov=guardian_sanitizer tests/
```

---

## 📐 Pull Request Guidelines

1. **Safety First**: Never implement automatic destructive deletion as a default behavior. Quarantine and review must remain the standard flow.
2. **Strict Sanitization**: Never pass unsanitized strings directly into Gmail query parameters.
3. **Test Coverage**: All new features or rule additions must be accompanied by unit tests in `tests/`.
4. **Semantic Versioning**: Releases follow SemVer format (`MAJOR.MINOR.PATCH`).
