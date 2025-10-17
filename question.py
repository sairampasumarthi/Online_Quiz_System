# question.py

class Question:
    """
    Represents a single multiple-choice question.
    OOP: Defines a base object.
    """
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options  # Data Structures: list of strings
        # The correct_answer must be the 0-based index of the correct option
        if not isinstance(correct_answer, int) or correct_answer < 0 or correct_answer >= len(options):
            # Exception Handling
            raise ValueError("Correct answer index is invalid.")
        self.correct_answer = correct_answer

    def display(self):
        """Prints the question and its options."""
        print(f"\nQ: {self.text}")
        for i, option in enumerate(self.options):
            print(f"   {i+1}. {option}")

    def is_correct(self, answer_index):
        """Functions: Checks if the given 1-based answer index is correct."""
        # Convert user's 1-based index back to 0-based
        return (answer_index - 1) == self.correct_answer

    def to_dict(self):
        """Persistence: Returns a dictionary for JSON serialization."""
        return {
            "text": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer
        }
