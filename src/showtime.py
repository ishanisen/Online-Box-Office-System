from datetime import datetime, time

class Showtime:
    def __init__(self, showtimeID: str, startAt: time, movieId: str, auditoriumId: str):
        self.showtimeID = showtimeID
        self.startAt = startAt
        self.movieId = movieId
        self.auditoriumId = auditoriumId

    def __str__(self):
        return f"Showtime ID: {self.showtimeID} at {self.startAt.strftime('%H:%M')} for Movie ID: {self.movieId} in Auditorium: {self.auditoriumId}"



