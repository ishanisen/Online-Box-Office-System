"""
UNIT TESTS for Payment class
Tests individual Payment class functionality
"""
from src.payment import Payment


class TestPaymentCreation:
    """Unit test: Payment object creation"""
    
    def test_create_payment_with_valid_data(self):
        payment = Payment("PAY-001", 15.26, "Visa", "Completed")
        assert payment.paymentId == "PAY-001"
        assert payment.amount == 15.26
        assert payment.paymentProvider == "Visa"
        assert payment.paymentStatus == "Completed"


class TestPaymentProviders:
    """Unit test: Different payment providers"""
    
    def test_visa_payment(self):
        payment = Payment("PAY-002", 10.00, "Visa", "Completed")
        assert payment.paymentProvider == "Visa"
    
    def test_mastercard_payment(self):
        payment = Payment("PAY-003", 10.00, "MasterCard", "Completed")
        assert payment.paymentProvider == "MasterCard"
    
    def test_debit_payment(self):
        payment = Payment("PAY-004", 10.00, "Debit", "Completed")
        assert payment.paymentProvider == "Debit"


class TestPaymentStatus:
    """Unit test: Different payment statuses"""
    
    def test_completed_status(self):
        payment = Payment("PAY-005", 10.00, "Visa", "Completed")
        assert payment.paymentStatus == "Completed"
    
    def test_pending_status(self):
        payment = Payment("PAY-006", 10.00, "Visa", "Pending")
        assert payment.paymentStatus == "Pending"
    
    def test_failed_status(self):
        payment = Payment("PAY-007", 10.00, "Visa", "Failed")
        assert payment.paymentStatus == "Failed"


class TestPaymentAmounts:
    """Unit test: Payment amount handling"""
    
    def test_typical_movie_ticket_amount(self):
        payment = Payment("PAY-008", 15.26, "Visa", "Completed")
        assert payment.amount == 15.26
    
    def test_large_amount(self):
        payment = Payment("PAY-009", 1234.56, "Visa", "Completed")
        assert payment.amount == 1234.56


class TestPaymentString:
    """Unit test: Payment string representation"""
    
    def test_str_includes_payment_id(self):
        payment = Payment("PAY-010", 15.00, "Visa", "Completed")
        result = str(payment)
        assert "PAY-010" in result
    
    def test_str_includes_amount(self):
        payment = Payment("PAY-011", 25.50, "Visa", "Completed")
        result = str(payment)
        assert "25.50" in result
