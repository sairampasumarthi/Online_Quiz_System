# quiz_system.py
import json
import os
from quiz import Quiz
from student import Student

# Define file paths
QUIZ_FILE = 'data/quizzes.json'
STUDENT_FILE = 'data/students.json'

class QuizSystem:
    """
    Manages all quizzes and students in the system.
    OOP: Central manager/Facade class.
    """
    def __init__(self):
        # Data Structures: Dictionaries for O(1) lookup
        self.quizzes = {} 
        self.students = {} 
        self.load_data() # Persistence: Load data upon initialization

    # --- Persistence Methods ---

    def load_data(self):
        """Loads all student and quiz data from JSON files."""
        # Load Students
        try:
            if os.path.exists(STUDENT_FILE):
                with open(STUDENT_FILE, 'r') as f:
                    students_data = json.load(f)
                    
                max_id = Student.next_id 
                for s_data in students_data:
                    student = Student.from_dict(s_data)
                    self.students[student.student_id] = student
                    if student.student_id >= max_id:
                        max_id = student.student_id + 1
                
                # Functions: Update the class variable to prevent ID collision
                Student.next_id = max_id
            
            print(f"Loaded {len(self.students)} students.")
            
        except json.JSONDecodeError:
            # Exception Handling
            print(f"Warning: {STUDENT_FILE} is corrupted or empty. Starting student data fresh.")
        except FileNotFoundError:
            print(f"Note: {STUDENT_FILE} not found. Starting student data fresh.")

        # Load Quizzes
        try:
            if os.path.exists(QUIZ_FILE):
                with open(QUIZ_FILE, 'r') as f:
                    quizzes_data = json.load(f)
                    
                for q_data in quizzes_data:
                    quiz = Quiz.from_dict(q_data)
                    self.quizzes[quiz.title] = quiz
                    
            print(f"Loaded {len(self.quizzes)} quizzes.")
            
        except json.JSONDecodeError:
            print(f"Warning: {QUIZ_FILE} is corrupted or empty. Starting quiz data fresh.")
        except FileNotFoundError:
            print(f"Note: {QUIZ_FILE} not found. Starting quiz data fresh.")


    def save_data(self):
        """Saves all current student and quiz data to JSON files."""
        os.makedirs(os.path.dirname(STUDENT_FILE), exist_ok=True) # Ensure data dir exists
        
        students_to_save = [s.to_dict() for s in self.students.values()]
        with open(STUDENT_FILE, 'w') as f:
            json.dump(students_to_save, f, indent=4)
        
        quizzes_to_save = [q.to_dict() for q in self.quizzes.values()]
        with open(QUIZ_FILE, 'w') as f:
            json.dump(quizzes_to_save, f, indent=4)

    # --- Core Functionality ---

    def create_student(self, name):
        """Creates a new student, saves, and prints ID."""
        new_student = Student(name)
        self.students[new_student.student_id] = new_student
        self.save_data() 
        print(f"Student created: {name} with ID: {new_student.student_id}")
        return new_student

    def add_quiz(self, quiz):
        """Adds a pre-made Quiz object to the system."""
        self.quizzes[quiz.title] = quiz
        self.save_data() 
        print(f"Quiz '{quiz.title}' added to the system.")

    def get_student(self, student_id):
        """Fetches a student by ID, using exception handling."""
        try:
            return self.students[student_id]
        except KeyError:
            # Exception Handling: specific error for non-existent student
            raise ValueError(f"No student found with ID: {student_id}")

    def attempt_quiz(self, student_id, quiz_title):
        """Handles the main workflow for a student attempting a quiz."""
        try:
            student = self.get_student(student_id)
            
            # Exception Handling: check if quiz exists
            if quiz_title not in self.quizzes:
                raise ValueError(f"Quiz titled '{quiz_title}' does not exist.")
            
            quiz = self.quizzes[quiz_title]
            
            score, total_questions = quiz.attempt_quiz()
            
            student.record_score(quiz_title, score, total_questions)
            self.save_data() # Save score immediately
            
            print(f"\n*** {student.name}'s Result for {quiz_title} ***")
            print(f"Score: {score} out of {total_questions}")
            print(f"Percentage: {score/total_questions * 100:.2f}%")
            
        except ValueError as e:
            print(f"Quiz Attempt Failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during quiz attempt: {e}")
