# student.py

class Student:
    """
    Tracks a student's name, ID, and quiz history.
    OOP: Encapsulates student data.
    """
    # Class-level attribute to assign unique IDs
    next_id = 1001 
    
    def __init__(self, name, student_id=None):
        if student_id is None:
            self.student_id = Student.next_id
            Student.next_id += 1
        else:
            self.student_id = student_id
            
        self.name = name
        # Data Structures: dict {quiz_title: (score, total_questions)}
        self.scores = {} 

    def record_score(self, quiz_title, score, total_questions):
        """Records the result of a completed quiz."""
        self.scores[quiz_title] = (score, total_questions)

    def get_summary(self):
        """Reports: Generates a summary of the student's performance."""
        report = {
            "ID": self.student_id,
            "Name": self.name,
            "Total_Quizzes_Attempted": len(self.scores),
            "Quiz_Details": self.scores
        }
        return report

    def to_dict(self):
        """Persistence: Returns a dictionary for JSON serialization."""
        # Convert the scores tuple (score, total) into a list for JSON serialization
        serializable_scores = {title: list(data) for title, data in self.scores.items()}
        return {
            "id": self.student_id,
            "name": self.name,
            "scores": serializable_scores
        }

    @classmethod
    def from_dict(cls, data):
        """Persistence: Creates a Student object from saved data (Deserialization)."""
        student = cls(data['name'], student_id=data['id'])
        # Convert list back to tuple for score tracking
        student.scores = {title: tuple(data) for title, data in data['scores'].items()}
        return student
