from datetime import datetime, time

class Showtime:
    def __init__(self, showtimeID: str, startAt: time, movieID: str, auditoriumID: str):
        self.showtimeID = showtimeID
        self.startAt = startAt
        self.movieID = movieID
        self.auditoriumID = auditoriumID

    def __str__(self):
        return f"Showtime ID: {self.showtimeID} at {self.startAt.strftime('%H:%M')} for Movie ID: {self.movieID} in Auditorium: {self.auditoriumID}"



