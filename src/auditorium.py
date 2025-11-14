class auditorium:
    def __init__(self, auditoriumID: str, audName: str):
        self.auditoriumID = auditoriumID
        self.audName = audName

    def __str__(self):
        return f"Auditorium ID: {self.auditoriumID}\n Auditorium Name: {self.audName}"
    
    def read(cls):
        auditoriumID = input("Enter the Auditorium ID:")
        audName = input("Enter the Auditorium Name:")

        