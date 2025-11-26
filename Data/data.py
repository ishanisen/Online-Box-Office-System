import sys
sys.path.insert(0,"src/")

from movie import Movie
from theater import Theater
from auditorium import Auditorium
from showtime import Showtime
from seat import Seat
from customer import Customer


# Theaters
theaters = [
Theater("T01", "ScotiaBank Theatre", "190 Chain Lake Dr, Halifax,NS B3S1C5"),
Theater("T02", "Cineplex Cinema Parklane Mall", "5657 Spring Garden Rd, Halifax,NS B3J3R4"),
Theater("T03", "Cinplex Cinemas Dartmouth Crossing", "145 Shubhie Drive, Dartmouth,NS B3B0C3"),
Theater("T04", "Cinplex Cinemas Lower Sackville", "760 Sackville Dr, Lower Sackville,NS B4E1R7")
]

# Auditoriums
auditoriums = [
    #Theater 1 auditoriums
Auditorium("A01", "Auditorium 1", "T01"),
Auditorium("A02", "Auditorium 2", "T01"),
    #Theater 2 auditoriums
Auditorium("A03", "Auditorium 1", "T02"),
Auditorium("A04", "Auditorium 2", "T02"),
    #Theater3 auditoriums
Auditorium("A05", "Auditorium 1", "T03"),
Auditorium("A06", "Auditorium 2", "T03"),
    #Theater4 auditoriums
Auditorium("A07", "Auditorium 1", "T04"),
Auditorium("A08", "Auditorium 2", "T04")
]

# Movies
movies = [
Movie("M01", "Dune 2", "PG-13", 166, "English"),
Movie("M02", "The Running Man", "14A", 170, "English"),
Movie("M03", "Inside Out 2", "G", 100, "English"),
Movie("M04", "Wicked:For Good", "PG", 138, "English")
]


# Showtimes
showtimes = [
Showtime("S01", "2025-11-20 18:30", "M01", "A01"),
Showtime("S02", "2025-11-20 21:00", "M01", "A02"),
Showtime("S03", "2025-11-20 19:00", "M02", "A03"),
Showtime("S04", "2025-11-20 17:00", "M03", "A04"),
Showtime("S05", "2025-11-20 17:30", "M04", "A05"),
Showtime("S06", "2025-11-20 16:00", "M04", "A06"),
Showtime("S07", "2025-11-20 17:00", "M01", "A01"),


]


# Seats (rows A-C, seats 1-6) for each auditorium
seats = []
for aud in auditoriums:
    for r_label in ["A","B","C"]:
        for num in range(1,7):
            seat_id = f"{aud.auditoriumId}-{r_label}{num}"
seats.append(Seat(seat_id, r_label, num, aud.auditoriumId))


# Preload example customers
customers = [
Customer("C001", "Alice", "Smith", "alice@example.com", "pass1"),
Customer("C002", "Bob", "Jones", "bob@example.com", "pass2")
]

# storage for runtime-created objects
orders = []
payments = []
tickets = []
