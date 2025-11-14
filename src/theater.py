class theater:
    def __init__(self, theaterID: str, theaterName: str, address: str):
        self.theaterID = theaterID
        self.theaterName = theaterName
        self.adress = address
    
    def __str__(self):
        return f"Theater\n Theater ID: {self.theaterID}\n Name:{self.theaterName}\n Address:{self.address} "
    
    def read(cls):
        theaterID = input("Enter the Theater ID:")
        theaterNAme = input("Eter the Theater Name: ")
        address = input ("Enter the Theater Address:")
        return cls(theaterID=theaterID, theaterNAme= theaterNAme, address=address)
    