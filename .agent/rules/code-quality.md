---
trigger: always_on
---

# Code Quality Standards

## 1. Python Style Guide
- Use `black` and `isort` for formatting.
- Type hints on all function signatures.
- Docstrings for all classes and public methods.
- Comprehensive exception handling (no silent failures).

## 2. Object-Oriented Programming (OOP)
- Single Responsibility Principle for classes in `core/lib/`.
- Clear encapsulation and interface separation.
- Decouple LLM provider API clients from the review logic.

## 3. Best Practices
- Every bug-fix conversationMUST end with a `best_practices.md` update.
- Ensure 100% test coverage for `review_engine` and `structure_validator`.
