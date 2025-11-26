class Theater:
    def __init__(self, theaterID: str, theaterName: str, address: str):
        self.theaterID = theaterID
        self.theaterName = theaterName
        self.address = address
    
    def __str__(self):
        return f"Theater\n Theater ID: {self.theaterID}\n Name:{self.theaterName}\n Address:{self.address} "
    
