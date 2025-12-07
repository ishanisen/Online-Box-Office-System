"""
UNIT TESTS for Customer class
Tests individual Customer class functionality
"""
from src.customer import Customer


class TestCustomerCreation:
    """Unit test: Customer object creation"""
    
    def test_create_customer_with_valid_data(self):
        customer = Customer("C101", "John", "Doe", "john@example.com", "password123")
        
        assert customer.customerId == "C101"
        assert customer.firstName == "John"
        assert customer.lastName == "Doe"
        assert customer.email == "john@example.com"
        assert customer.password == "password123"
        assert customer.orders == []
    
    def test_customer_has_empty_orders_initially(self):
        customer = Customer("C102", "Jane", "Smith", "jane@example.com", "pass456")
        assert len(customer.orders) == 0
    
    def test_customer_with_special_characters_in_email(self):
        customer = Customer("C103", "Test", "User", "test+special@example.co.uk", "pass")
        assert customer.email == "test+special@example.co.uk"


class TestCustomerOrders:
    """Unit test: Customer order management"""
    
    def test_can_add_order_to_customer(self):
        customer = Customer("C104", "Carol", "Davis", "carol@example.com", "pass")
        customer.orders.append("ORDER-001")
        assert len(customer.orders) == 1
    
    def test_multiple_orders_can_be_added(self):
        customer = Customer("C105", "David", "Miller", "david@example.com", "pass")
        customer.orders.append("ORDER-001")
        customer.orders.append("ORDER-002")
        assert len(customer.orders) == 2


class TestCustomerString:
    """Unit test: Customer string representation"""
    
    def test_str_method_includes_full_name(self):
        customer = Customer("C106", "Bob", "Wilson", "bob@example.com", "pass")
        result = str(customer)
        assert "Bob Wilson" in result
