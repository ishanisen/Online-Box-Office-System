class Payment:
    def __init__(self, paymentId: str, amount: float, paymentProvider: str, paymentStatus: str):
        self.paymentId = paymentId
        self.amount = amount
        self.paymentProvider = paymentProvider
        self.paymentStatus = paymentStatus


def __str__(self):
    return f"Payment {self.paymentId}: ${self.amount:.2f} via {self.paymentProvider} — {self.paymentStatus}"