# Auditorium class 
class Auditorium:
    def __init__(self, auditoriumID: str, audName: str, theaterID: str):
        self.auditoriumID = auditoriumID
        self.audName = audName
        self.theaterID = theaterID
# string method
    def __str__(self):
        return f"Auditorium ID: {self.auditoriumID}\n Auditorium Name: {self.audName}"
    
# Method to filter and return only seats that belong to this auditorium from a list all_seats
    def get_seats(self, all_seats):
        return [s for s in all_seats if s.auditoriumID == self.auditoriumID]
    
#  finds a specific seat in the auditorium    MIGHT NOT NEED THIS!!!!!!!!!!!!!!!!!!!
#     def find_seat(self, all_seats, rowLabel, seatNumber):
#         return next(
#             (s for s in all_seats 
#              if s.auditoriumID== self.auditoriumID
#              and s.label() == f"{rowLabel}{seatNumber}"),
#             None
#         )


    def display_seating_chart(self, all_seats):
        seats = self.get_seats(all_seats)
        rows = {}
        for seat in seats:
            rows.setdefault(seat.rowLabel, []).append(seat)

        print(f"\nSeating chart for {self.name}:")
        for row, seats_in_row in sorted(rows.items()):
            row_display = " ".join(
                f"{s.label()}{'X' if s.taken else ''}" for s in seats_in_row
            )
            print(f"Row {row}: {row_display}")
            

        
