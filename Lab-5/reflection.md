# Lab 5 — Static Code Analysis Reflection

### 1. What did you learn from static code analysis?

I learned that static code analysis helps find errors in Python code without executing the program. It helps improve code quality, security, and readability.

### 2. How did Pylint, Bandit, and Flake8 help?

Pylint identified code-quality issues, Bandit detected security risks such as unsafe `eval()`, and Flake8 highlighted formatting problems.

### 3. What were the important issues you fixed?

I fixed unsafe `eval()`, silent exception handling, shared default lists, global variable modification, and negative fine calculations. I also improved file handling and formatting.

### 4. How did the code improve after fixing the issues?

The Pylint score increased from 6.07 to 10.00. Bandit findings decreased from 2 to 0, and Flake8 violations decreased from 14 to 0. The corrected program is safer and easier to maintain.