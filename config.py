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
    {"id": 4, "code": "PHYS101", "title": "Introduction to Physics", "max_absences": 3},
    {"id": 5, "code": "CHEM110", "title": "General Chemistry", "max_absences": 4},
    {"id": 6, "code": "BIO120", "title": "Introduction to Biology", "max_absences": 3},
    {"id": 7, "code": "CS201", "title": "Data Structures", "max_absences": 3},
    {"id": 8, "code": "HIST101", "title": "World History", "max_absences": 4},
]

DEMO_STUDENTS = [
    {"id": 1, "name": "Alex Johnson", "student_id": "S1001", "courses": [1, 2, 3]},
    {"id": 2, "name": "Maria Garcia", "student_id": "S1002", "courses": [1, 3, 5]},
    {"id": 3, "name": "James Wilson", "student_id": "S1003", "courses": [1, 2, 4]},
    {"id": 4, "name": "Emma Davis", "student_id": "S1004", "courses": [2, 3, 6]},
    {"id": 5, "name": "Liam Chen", "student_id": "S1005", "courses": [1, 2, 3]},
    {"id": 6, "name": "Sophia Kim", "student_id": "S1006", "courses": [4, 5, 6]},
    {"id": 7, "name": "Noah Martinez", "student_id": "S1007", "courses": [7, 8]},
    {"id": 8, "name": "Olivia Thompson", "student_id": "S1008", "courses": [3, 5, 8]},
    {"id": 9, "name": "Ethan Brown", "student_id": "S1009", "courses": [1, 4, 7]},
    {"id": 10, "name": "Ava Robinson", "student_id": "S1010", "courses": [2, 6, 8]},
]

DEMO_PROFESSORS = [
    {"id": 1, "name": "Dr. Sarah Miller", "department": "Computer Science", "courses": [1, 7]},
    {"id": 2, "name": "Dr. Robert Johnson", "department": "Mathematics", "courses": [2]},
    {"id": 3, "name": "Prof. Jennifer Lee", "department": "English", "courses": [3]},
    {"id": 4, "name": "Dr. Michael Clark", "department": "Physics", "courses": [4]},
    {"id": 5, "name": "Dr. Emily Chen", "department": "Chemistry", "courses": [5]},
    {"id": 6, "name": "Prof. David Rodriguez", "department": "Biology", "courses": [6]},
    {"id": 7, "name": "Dr. Amanda Williams", "department": "History", "courses": [8]},
]

# AI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Path settings
POLICIES_DIR = BASE_DIR / "docs" / "university_policies"