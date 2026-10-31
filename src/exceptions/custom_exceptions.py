class BaseAppExceptions(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidMarksError(BaseAppExceptions):
    def __init__(self, score):
        super().__init__(score)
        self.score = score
    def __str__(self):    
        return f"Invalid input for marks." if self.score>100 or self.score<0 else f"{self.message}"

class RecordNotFound(BaseAppExceptions):
    def __init__(self, roll=None):
        super().__init__(roll)
        self.roll = roll
    def __str__(self):
        return f"Roll number does not exist." if not self.roll else f"{self.message}"
