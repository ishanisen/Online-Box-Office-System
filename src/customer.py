class Customer:
    def __init__(self, customerID: str, firstName: str, lastName: str, email: str, password: str):
        self.customerID = customerID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.orders = []

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.email})"
    
