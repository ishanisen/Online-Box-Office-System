import uuid
from typing import List
from Data.movie import Movie
from src.theater import Theater
from src.auditorium import Auditorium
from src.showtime import Showtime
from src.seat import Seat


# find helpers


def find_movie(movieId: str, movies: List[Movie]):
    return next((m for m in movies if m.movieId == movieId), None)




def find_showtimes_for_movie(movieId: str, showtimes: List[Showtime]):
    return [s for s in showtimes if s.movieId == movieId]




def find_auditorium(auditoriumId: str, auditoriums: List[Auditorium]):
    return next((a for a in auditoriums if a.auditoriumId == auditoriumId), None)




def get_seats_for_auditorium(auditoriumId: str, seats: List[Seat]):
    return [s for s in seats if s.auditoriumId == auditoriumId]




def find_seat_by_label(auditoriumId: str, rowLabel: str, seatNumber: int, seats: List[Seat]):
    label = f"{rowLabel}{seatNumber}"
    return next((s for s in seats if s.auditoriumId==auditoriumId and s.label()==label), None)




def generate_id(prefix: str = "ID"):
    return prefix + uuid.uuid4().hex[:8]