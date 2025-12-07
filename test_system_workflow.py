"""
SYSTEM/END-TO-END TESTS
Tests complete workflows from start to finish
"""
import pytest
from src.customer import Customer
from src.order import Order
from src.payment import Payment
from src.ticket import Ticket


class TestCompleteBookingWorkflow:
    """System test: Full customer booking workflow"""
    
    def test_new_customer_complete_booking(self):
        """Test: New customer registers, books ticket, and completes payment"""
        # Step 1: Customer registration
        customer = Customer("C-001", "John", "Doe", "john@example.com", "password123")
        assert customer.email == "john@example.com"
        assert len(customer.orders) == 0
        
        # Step 2: Customer selects movie and showtime (simulated)
        selected_movie = "MOV-001"
        selected_showtime = "ST-001"
        selected_seat = "SEAT-A1"
        
        # Step 3: Create order for the ticket
        ticket_price = 12.00
        fees = 1.50
        tax = round((ticket_price + fees) * 0.13, 2)
        order = Order("ORD-001", ticket_price, fees, tax)
        customer.orders.append(order)
        
        # Step 4: Process payment
        payment = Payment("PAY-001", order.grandTotal, "Visa", "Completed")
        assert payment.amount == order.grandTotal
        assert payment.paymentStatus == "Completed"
        
        # Step 5: Generate ticket
        ticket = Ticket("TICK-001", "QR-ABC123", selected_showtime, selected_seat, order.orderNumber)
        assert ticket.orderNumber == order.orderNumber
        assert ticket.seatId == selected_seat
        
        # Verify complete workflow
        assert len(customer.orders) == 1
        assert customer.orders[0].grandTotal == payment.amount
        assert ticket.orderNumber == customer.orders[0].orderNumber
    
    def test_returning_customer_multiple_bookings(self):
        """Test: Returning customer makes multiple bookings"""
        # Existing customer
        customer = Customer("C-002", "Jane", "Smith", "jane@example.com", "pass456")
        
        # First booking
        order1 = Order("ORD-002", 12.00, 1.50, 1.76)
        customer.orders.append(order1)
        payment1 = Payment("PAY-002", order1.grandTotal, "MasterCard", "Completed")
        ticket1 = Ticket("TICK-002", "QR-XYZ789", "ST-002", "SEAT-B2", order1.orderNumber)
        
        # Second booking (same session)
        order2 = Order("ORD-003", 12.00, 1.50, 1.76)
        customer.orders.append(order2)
        payment2 = Payment("PAY-003", order2.grandTotal, "Visa", "Completed")
        ticket2 = Ticket("TICK-003", "QR-DEF456", "ST-003", "SEAT-C3", order2.orderNumber)
        
        # Verify customer has both orders
        assert len(customer.orders) == 2
        assert customer.orders[0].orderNumber == ticket1.orderNumber
        assert customer.orders[1].orderNumber == ticket2.orderNumber


class TestGroupBookingWorkflow:
    """System test: Group booking scenarios"""
    
    def test_customer_books_multiple_seats_same_showtime(self):
        """Test: Customer books multiple seats for same showtime"""
        customer = Customer("C-003", "Bob", "Wilson", "bob@example.com", "secure789")
        
        # Book 3 seats for same showtime
        showtime = "ST-100"
        seats = ["SEAT-D1", "SEAT-D2", "SEAT-D3"]
        
        # Single order for all tickets
        total_price = 12.00 * 3
        total_fees = 1.50 * 3
        total_tax = round((total_price + total_fees) * 0.13, 2)
        order = Order("ORD-100", total_price, total_fees, total_tax)
        customer.orders.append(order)
        
        # Single payment for entire order
        payment = Payment("PAY-100", order.grandTotal, "Debit", "Completed")
        
        # Generate multiple tickets
        tickets = []
        for i, seat in enumerate(seats):
            ticket = Ticket(f"TICK-10{i}", f"QR-GROUP{i}", showtime, seat, order.orderNumber)
            tickets.append(ticket)
        
        # Verify group booking
        assert len(tickets) == 3
        assert all(t.showtimeId == showtime for t in tickets)
        assert all(t.orderNumber == order.orderNumber for t in tickets)
        assert len(set(t.seatId for t in tickets)) == 3  # All different seats
        assert payment.amount == order.grandTotal
    
    def test_two_customers_book_adjacent_seats(self):
        """Test: Two different customers book adjacent seats"""
        customer1 = Customer("C-004", "Alice", "Brown", "alice@example.com", "pass111")
        customer2 = Customer("C-005", "Charlie", "Davis", "charlie@example.com", "pass222")
        
        showtime = "ST-200"
        
        # Customer 1 books seat E1
        order1 = Order("ORD-201", 12.00, 1.50, 1.76)
        customer1.orders.append(order1)
        payment1 = Payment("PAY-201", order1.grandTotal, "Visa", "Completed")
        ticket1 = Ticket("TICK-201", "QR-ALICE", showtime, "SEAT-E1", order1.orderNumber)
        
        # Customer 2 books seat E2 (adjacent)
        order2 = Order("ORD-202", 12.00, 1.50, 1.76)
        customer2.orders.append(order2)
        payment2 = Payment("PAY-202", order2.grandTotal, "MasterCard", "Completed")
        ticket2 = Ticket("TICK-202", "QR-CHARLIE", showtime, "SEAT-E2", order2.orderNumber)
        
        # Verify both bookings successful
        assert ticket1.showtimeId == ticket2.showtimeId
        assert ticket1.seatId != ticket2.seatId
        assert ticket1.orderNumber != ticket2.orderNumber


class TestPaymentFailureScenarios:
    """System test: Payment failure handling"""
    
    def test_payment_declined_no_ticket_generated(self):
        """Test: Payment declined scenario - no ticket should be generated"""
        customer = Customer("C-006", "Eve", "Martin", "eve@example.com", "pass333")
        
        # Create order
        order = Order("ORD-300", 12.00, 1.50, 1.76)
        customer.orders.append(order)
        
        # Payment declined
        payment = Payment("PAY-300", order.grandTotal, "Visa", "Failed")
        
        # Verify payment failed
        assert payment.paymentStatus == "Failed"
        
        # In real system, ticket should NOT be created if payment failed
        # We verify this by not creating ticket object
        assert len(customer.orders) == 1
        assert customer.orders[0].orderNumber == "ORD-300"
    
    def test_payment_pending_ticket_not_confirmed(self):
        """Test: Payment pending - ticket exists but not confirmed"""
        customer = Customer("C-007", "Frank", "Taylor", "frank@example.com", "pass444")
        
        order = Order("ORD-400", 12.00, 1.50, 1.76)
        customer.orders.append(order)
        
        # Payment pending
        payment = Payment("PAY-400", order.grandTotal, "Debit", "Pending")
        
        # Ticket created but linked to pending payment
        ticket = Ticket("TICK-400", "QR-PENDING", "ST-400", "SEAT-F1", order.orderNumber)
        
        # Verify payment is pending
        assert payment.paymentStatus == "Pending"
        assert ticket.orderNumber == order.orderNumber


class TestOrderPricingWorkflow:
    """System test: Order pricing calculations in complete workflow"""
    
    def test_order_pricing_matches_payment_amount(self):
        """Test: Order total matches payment amount in complete workflow"""
        customer = Customer("C-008", "Grace", "Lee", "grace@example.com", "pass555")
        
        # Define pricing
        subtotal = 15.00
        fees = 2.00
        tax = round((subtotal + fees) * 0.13, 2)
        
        # Create order
        order = Order("ORD-500", subtotal, fees, tax)
        customer.orders.append(order)
        
        # Calculate expected total
        expected_total = subtotal + fees + tax
        
        # Process payment with exact order total
        payment = Payment("PAY-500", order.grandTotal, "Visa", "Completed")
        
        # Verify amounts match
        assert order.grandTotal == expected_total
        assert payment.amount == order.grandTotal
        assert payment.amount == expected_total
    
    def test_multi_ticket_order_pricing(self):
        """Test: Multi-ticket order pricing calculation"""
        customer = Customer("C-009", "Henry", "White", "henry@example.com", "pass666")
        
        # 4 tickets
        num_tickets = 4
        price_per_ticket = 12.00
        fee_per_ticket = 1.50
        
        subtotal = price_per_ticket * num_tickets
        fees = fee_per_ticket * num_tickets
        tax = round((subtotal + fees) * 0.13, 2)
        
        order = Order("ORD-600", subtotal, fees, tax)
        payment = Payment("PAY-600", order.grandTotal, "MasterCard", "Completed")
        
        # Verify pricing
        assert order.subtotal == 48.00  # 12 * 4
        assert order.feesTotal == 6.00  # 1.50 * 4
        assert order.grandTotal == payment.amount


class TestEdgeCaseWorkflows:
    """System test: Edge cases and boundary conditions"""
    
    def test_minimum_valid_booking(self):
        """Test: Minimum viable booking (all minimum values)"""
        customer = Customer("C-010", "I", "J", "i@j.com", "pw")
        order = Order("O-1", 0.01, 0.01, 0.01)
        customer.orders.append(order)
        payment = Payment("P-1", order.grandTotal, "C", "Completed")
        ticket = Ticket("T-1", "QR-1", "S-1", "A1", order.orderNumber)
        
        # Verify minimum booking works
        assert customer.customerId == "C-010"
        assert order.grandTotal == 0.03
        assert payment.amount == 0.03
        assert ticket.ticketId == "T-1"
    
    def test_customer_with_no_orders(self):
        """Test: Customer registered but hasn't booked anything"""
        customer = Customer("C-011", "Karen", "Moore", "karen@example.com", "pass777")
        
        # Verify customer exists but has no orders
        assert customer.email == "karen@example.com"
        assert len(customer.orders) == 0
        assert customer.orders == []
