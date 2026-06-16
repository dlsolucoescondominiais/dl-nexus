## 2024-05-16 - KILLCRITIC Rule Validation Pattern
**Learning:** When validating negative constraints (e.g. "nunca diga visita técnica" which contains the forbidden term "visita técnica"), a naive substring check will yield false positives.
**Action:** Enhance the `validar_killcritic.py` script to accept exceptions. Replace exception strings with placeholders before performing the check for forbidden terms.
