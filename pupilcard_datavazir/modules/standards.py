# standards.py - Centralized standards definitions for the application

"""
This module provides centralized standards definitions for EGRA and EGMA assessments.
All applications should import standards from this module rather than defining them locally.
"""

# Standard evaluation thresholds for each category
STANDARDS = {
    # EGRA standards
    "clpm": {"Mastery": 44, "Developing": (31, 43), "Emerging": (0, 30)},
    "phoneme": {"Mastery": 41, "Developing": (24, 40), "Emerging": (0, 23)},
    "sound_word": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "cwpm": {"Mastery": 29, "Developing": (17, 28), "Emerging": (0, 16)},
    "listening": {"Mastery": 75, "Developing": (50, 74), "Emerging": (0, 49)},
    "orf": {"Mastery": 50, "Developing": (30, 49), "Emerging": (0, 29)},
    "comprehension": {"Mastery": 75, "Developing": (50, 74), "Emerging": (0, 49)},
    
    # EGMA standards
    "number_id": {"Mastery": 56, "Developing": (49, 55), "Emerging": (0, 48)},
    "discrimin": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "missing_number": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "addition": {"Mastery": 10, "Developing": (6, 9), "Emerging": (0, 5)},
    "subtraction": {"Mastery": 10, "Developing": (6, 9), "Emerging": (0, 5)},
    "problems": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)}
}

# Group indicators by assessment type for easier access
EGRA_INDICATORS = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
EGMA_INDICATORS = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]
