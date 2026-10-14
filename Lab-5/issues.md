# Lab 5 — Static Code Analysis: Identified Issues

**Program:** Library Fine and Book Renewal System

**Objective:** Identify and fix code quality, security, and formatting issues using Pylint, Bandit, and Flake8.

## Issue Documentation

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe `eval()` (B307) | Security — Medium | 45 | Executes potentially unsafe Python expressions. | Replaced `eval()` with an explicitly supported fine formula. |
| Try-except-pass (B110) | Security — Low | 21–22 | Errors were silently ignored. | Checked whether the student and book exist before removing them. |
| Mutable default argument (W0102) | Bug | 9 | The default `dates=[]` list was shared between function calls. | Changed the default to `None` and created a fresh list. |
| Global fine modification (W0603) | Logic / Code quality | 27–31 | Renewing a book changed the fine rate for all students. | Removed the global fine modification. |
| Negative fine calculation | Logic bug | 24–25 | Negative overdue days produced negative fines. | Used `max(0, days_overdue)` to prevent negative charges. |
| Unsafe file handling (R1732, W1514) | Reliability | 34, 40 | Files were opened without explicit encoding or context managers. | Used `with open()` and UTF-8 encoding. |
| Unused import (F401) | Code style | 2 | The `os` module was imported but never used. | Removed the unused import. |
| Missing blank lines (E302, E305) | Formatting | Multiple lines | Functions did not have the required separation. | Added two blank lines between top-level definitions. |
| Long lines (E501) | Formatting | 14, 31 | Some lines exceeded the 79-character limit. | Split long statements across multiple lines. |

*Line numbers refer to the original Python file before fixes.*

## Final Results

| Tool | Before | After |
|---|---|---|
| Pylint | 6.07/10 | 10.00/10 |
| Bandit | 2 findings | 0 findings |
| Flake8 | 14 violations | 0 violations |

## Conclusion

Static analysis helped identify security risks, coding mistakes, and formatting problems. After correcting the issues, all three tools passed. The program is now easier to read, safer, and more maintainable.