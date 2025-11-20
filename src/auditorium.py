class auditorium:
    def __init__(self, auditoriumID: str, audName: str):
        self.auditoriumID = auditoriumID
        self.audName = audName

    def __str__(self):
        return f"Auditorium ID: {self.auditoriumID}\n Auditorium Name: {self.audName}"
    
    def get_seats(self, all_seats):
        return [s for s in all_seats if s.auditoriumId == self.auditoriumId]

    def find_seat(self, all_seats, rowLabel, seatNumber):
        return next(
            (s for s in all_seats 
             if s.auditoriumId == self.auditoriumId 
             and s.label() == f"{rowLabel}{seatNumber}"),
            None
        )

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
            

        