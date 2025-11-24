class Order:
    def __init__(self, orderNumber: str, subtotal: float, feesTotal: float, taxTotal: float):
        self.orderNumber = orderNumber
        self.subtotal = subtotal
        self.feesTotal = feesTotal
        self.taxTotal = taxTotal
        self.grandTotal = round(subtotal + feesTotal + taxTotal, 2)

    def __str__(self):
        return f"Order {self.orderNumber} — Total: ${self.grandTotal:.2f}"
