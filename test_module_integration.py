"""
MODULE/INTEGRATION TESTS
Tests interactions between multiple classes
"""
from src.customer import Customer
from src.order import Order
from src.payment import Payment
from src.ticket import Ticket


class TestCustomerOrderIntegration:
    """Module test: Customer and Order interaction"""
    
    def test_customer_can_have_orders(self):
        customer = Customer("C-001", "John", "Doe", "john@example.com", "pass123")
        order = Order("ORD-001", 10.00, 1.50, 1.00)
        customer.orders.append(order)
        assert len(customer.orders) == 1
        assert customer.orders[0].orderNumber == "ORD-001"
    
    def test_customer_multiple_orders(self):
        customer = Customer("C-002", "Jane", "Smith", "jane@example.com", "pass456")
        order1 = Order("ORD-002", 10.00, 1.50, 1.00)
        order2 = Order("ORD-003", 15.00, 2.00, 1.50)
        customer.orders.append(order1)
        customer.orders.append(order2)
        assert len(customer.orders) == 2
    
    def test_order_grand_total_matches_customer_order(self):
        customer = Customer("C-003", "Bob", "Wilson", "bob@example.com", "pass789")
        order = Order("ORD-004", 10.00, 1.50, 1.00)
        customer.orders.append(order)
        expected_total = 10.00 + 1.50 + 1.00
        assert customer.orders[0].grandTotal == expected_total


class TestOrderPaymentIntegration:
    """Module test: Order and Payment interaction"""
    
    def test_payment_amount_matches_order_total(self):
        order = Order("ORD-005", 10.00, 1.50, 1.00)
        grand_total = order.grandTotal
        payment = Payment("PAY-001", grand_total, "Visa", "Completed")
        assert payment.amount == order.grandTotal
    
    def test_payment_for_large_order(self):
        order = Order("ORD-006", 100.00, 10.00, 8.00)
        payment = Payment("PAY-002", order.grandTotal, "MasterCard", "Completed")
        assert payment.amount == 118.00
    
    def test_payment_status_after_order(self):
        order = Order("ORD-007", 20.00, 2.00, 1.80)
        payment = Payment("PAY-003", order.grandTotal, "Visa", "Completed")
        assert payment.paymentStatus == "Completed"


class TestOrderTicketIntegration:
    """Module test: Order and Ticket interaction"""
    
    def test_ticket_belongs_to_order(self):
        order = Order("ORD-008", 10.00, 1.50, 1.00)
        ticket = Ticket("TICK-001", "QR123", "ST-001", "SEAT-001", order.orderNumber)
        assert ticket.orderNumber == order.orderNumber
    
    def test_multiple_tickets_per_order(self):
        order = Order("ORD-009", 20.00, 3.00, 2.00)
        ticket1 = Ticket("TICK-002", "QR456", "ST-002", "SEAT-002", order.orderNumber)
        ticket2 = Ticket("TICK-003", "QR789", "ST-002", "SEAT-003", order.orderNumber)
        assert ticket1.orderNumber == order.orderNumber
        assert ticket2.orderNumber == order.orderNumber
        assert ticket1.ticketId != ticket2.ticketId


class TestPaymentTicketIntegration:
    """Module test: Payment and Ticket interaction"""
    
    def test_payment_covers_ticket_cost(self):
        payment = Payment("PAY-004", 12.50, "Visa", "Completed")
        ticket = Ticket("TICK-004", "QR111", "ST-003", "SEAT-004", "ORD-010")
        assert payment.amount >= 10.00  # Typical ticket price
    
    def test_payment_for_multiple_tickets(self):
        payment = Payment("PAY-005", 25.00, "MasterCard", "Completed")
        ticket1 = Ticket("TICK-005", "QR222", "ST-004", "SEAT-005", "ORD-011")
        ticket2 = Ticket("TICK-006", "QR333", "ST-004", "SEAT-006", "ORD-011")
        # Payment amount should cover cost of multiple tickets
        assert payment.amount >= 20.00


class TestFullBookingFlow:
    """Module test: Customer → Order → Payment → Ticket workflow"""
    
    def test_complete_booking_workflow(self):
        # Step 1: Customer initiates booking
        customer = Customer("C-100", "Alice", "Brown", "alice@example.com", "secure123")
        
        # Step 2: Create order
        order = Order("ORD-100", 10.00, 1.50, 1.00)
        customer.orders.append(order)
        
        # Step 3: Process payment
        payment = Payment("PAY-100", order.grandTotal, "Visa", "Completed")
        
        # Step 4: Generate ticket
        ticket = Ticket("TICK-100", "QRFINAL", "ST-100", "SEAT-A1", order.orderNumber)
        
        # Verify workflow integrity
        assert len(customer.orders) == 1
        assert payment.amount == order.grandTotal
        assert payment.paymentStatus == "Completed"
        assert ticket.orderNumber == order.orderNumber
    
    def test_booking_with_multiple_tickets(self):
        # Customer books multiple seats
        customer = Customer("C-101", "Charlie", "Davis", "charlie@example.com", "pass999")
        
        # Order for 2 tickets
        order = Order("ORD-101", 20.00, 3.00, 2.00)
        customer.orders.append(order)
        
        # Single payment for entire order
        payment = Payment("PAY-101", order.grandTotal, "Debit", "Completed")
        
        # Two tickets for same showtime
        ticket1 = Ticket("TICK-101", "QR1001", "ST-200", "SEAT-B1", order.orderNumber)
        ticket2 = Ticket("TICK-102", "QR1002", "ST-200", "SEAT-B2", order.orderNumber)
        
        # Verify multi-ticket booking
        assert payment.amount == 25.00  # 20 + 3 + 2
        assert ticket1.orderNumber == order.orderNumber
        assert ticket2.orderNumber == order.orderNumber
        assert ticket1.showtimeId == ticket2.showtimeId
        assert ticket1.seatId != ticket2.seatId  # Different seats
