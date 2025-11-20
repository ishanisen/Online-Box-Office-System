class Ticket:
    def __init__(self, ticketId: str, qrCode: str, showtimeId: str, seatId: str, orderNumber: str):
        self.ticketId = ticketId
        self.qrCode = qrCode
        self.showtimeId = showtimeId
        self.seatId = seatId
        self.orderNumber = orderNumber


def __str__(self):
    return f"Ticket {self.ticketId}: Seat {self.seatId}, Showtime {self.showtimeId}, Order {self.orderNumber}"