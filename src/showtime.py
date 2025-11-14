from datetime import time
class showtime:
    def __init__(self, showtimeID: str, startAt: time):
        self.showtimeID = showtime
        self.startAt = startAt
    
    def __str__(self):
        return f"{self.showtimeID} at {self.startAt}"

    def read(cls):
        showtimeID = input("Eneter Show Time ID: ")
        startAt = input ("Enter the Start Time of the Movie:")
        return cls(showtimeId = showtimeID, startAt=startAt)
    
    