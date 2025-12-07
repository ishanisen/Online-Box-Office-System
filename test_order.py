"""
UNIT TESTS for Order class
Tests individual Order class functionality
"""
from src.order import Order


class TestOrderCreation:
    """Unit test: Order object creation"""
    
    def test_create_order_with_valid_data(self):
        order = Order("ORD-001", 10.00, 1.50, 1.50)
        assert order.orderNumber == "ORD-001"
        assert order.subtotal == 10.00
        assert order.feesTotal == 1.50
        assert order.taxTotal == 1.50
    
    def test_order_grand_total_calculation(self):
        order = Order("ORD-002", 12.00, 1.50, 1.76)
        expected_total = 12.00 + 1.50 + 1.76
        assert order.grandTotal == round(expected_total, 2)
    
    def test_grand_total_is_rounded_to_two_decimals(self):
        order = Order("ORD-003", 10.123, 1.456, 1.789)
        assert order.grandTotal == round(order.grandTotal, 2)


class TestOrderCalculations:
    """Unit test: Order calculation logic"""
    
    def test_zero_fees_and_tax(self):
        order = Order("ORD-004", 15.00, 0.00, 0.00)
        assert order.grandTotal == 15.00
    
    def test_typical_movie_ticket_order(self):
        # Typical: $12 ticket + $1.50 fees + $1.76 tax
        order = Order("ORD-005", 12.00, 1.50, 1.76)
        assert order.grandTotal == 15.26
    
    def test_large_order_calculation(self):
        order = Order("ORD-006", 999.99, 50.00, 136.50)
        expected = round(999.99 + 50.00 + 136.50, 2)
        assert order.grandTotal == expected


class TestOrderString:
    """Unit test: Order string representation"""
    
    def test_str_method_includes_order_number(self):
        order = Order("ORD-007", 10.00, 1.00, 1.00)
        result = str(order)
        assert "ORD-007" in result
    
    def test_str_method_includes_grand_total(self):
        order = Order("ORD-008", 10.00, 1.00, 1.00)
        result = str(order)
        assert "12.00" in result
