class Seat:
    def __init__(self, seatID: str, rowLabel:str, seatNumber: int, auditoriumID: str):
        self.seatID = seatID
        self.rowLabel = rowLabel
        self.seatNumber = seatNumber
        self.auditoriumID  = auditoriumID
        self.taken = False

    def label(self):
        return f"{self.rowLabel}{self.seatNumber}"
    
    def __str__(self):
        return f"{self.label()} [{'X' if self.taken else 'O'}]"
    
    
