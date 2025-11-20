class seat:
    def __init__(self, seatID: str, rowLabel:str, seatNumber: int, auditoriumId: str):
        self.seatId= seatID
        self.rowLabel = rowLabel
        self.seatNUmber = seatNumber
        self.aiditoriumId = auditoriumId
        self.taken = False

    def label(self):
        return f"{self.rowLabel}{self.seatNumber}"
    
    def __str__(self):
        return f"{self.label()} [{'X' if self.taken else 'O'}]"
    

