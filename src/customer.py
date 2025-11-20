class Customer:
    def __init__(self, customerId: str, firstName: str, lastName: str, email: str, password: str):
        self.customerId = customerId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.orders = []


    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.email})"
    