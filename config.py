import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Application settings
APP_NAME = "ClassTracker"
APP_VERSION = "1.0.0 (Demo)"

# Dummy data settings
DEMO_COURSES = [
    {"id": 1, "code": "CS101", "title": "Introduction to Computer Science", "max_absences": 3},
    {"id": 2, "code": "MATH201", "title": "Calculus II", "max_absences": 4},
    {"id": 3, "code": "ENG105", "title": "Technical Writing", "max_absences": 3},
]

DEMO_STUDENTS = [
    {"id": 1, "name": "Alex Johnson", "student_id": "S1001", "courses": [1, 2, 3]},
    {"id": 2, "name": "Maria Garcia", "student_id": "S1002", "courses": [1, 3]},
    {"id": 3, "name": "James Wilson", "student_id": "S1003", "courses": [1, 2]},
    {"id": 4, "name": "Emma Davis", "student_id": "S1004", "courses": [2, 3]},
    {"id": 5, "name": "Liam Chen", "student_id": "S1005", "courses": [1, 2, 3]},
]

DEMO_PROFESSORS = [
    {"id": 1, "name": "Dr. Sarah Miller", "department": "Computer Science", "courses": [1]},
    {"id": 2, "name": "Dr. Robert Johnson", "department": "Mathematics", "courses": [2]},
    {"id": 3, "name": "Prof. Jennifer Lee", "department": "English", "courses": [3]},
]

# AI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Path settings
POLICIES_DIR = BASE_DIR / "docs" / "university_policies"