"""
UNIT TESTS for Ticket class
Tests individual Ticket class functionality
"""
from src.ticket import Ticket


class TestTicketCreation:
    """Unit test: Ticket object creation"""
    
    def test_create_ticket_with_valid_data(self):
        ticket = Ticket("TICK-001", "QR12345", "ST-001", "SEAT-001", "ORD-001")
        assert ticket.ticketId == "TICK-001"
        assert ticket.qrCode == "QR12345"
        assert ticket.showtimeId == "ST-001"
        assert ticket.seatId == "SEAT-001"
        assert ticket.orderNumber == "ORD-001"


class TestTicketQRCode:
    """Unit test: QR code handling"""
    
    def test_qr_code_storage(self):
        ticket = Ticket("TICK-002", "QR98765", "ST-002", "SEAT-002", "ORD-002")
        assert ticket.qrCode == "QR98765"
    
    def test_different_qr_codes(self):
        ticket1 = Ticket("TICK-003", "QRABC123", "ST-003", "SEAT-003", "ORD-003")
        ticket2 = Ticket("TICK-004", "QRXYZ789", "ST-003", "SEAT-004", "ORD-003")
        assert ticket1.qrCode != ticket2.qrCode


class TestTicketShowtimeAssociation:
    """Unit test: Ticket-to-Showtime relationship"""
    
    def test_showtime_association(self):
        ticket = Ticket("TICK-005", "QR11111", "ST-100", "SEAT-005", "ORD-004")
        assert ticket.showtimeId == "ST-100"
    
    def test_multiple_tickets_same_showtime(self):
        ticket1 = Ticket("TICK-006", "QR22222", "ST-200", "SEAT-006", "ORD-005")
        ticket2 = Ticket("TICK-007", "QR33333", "ST-200", "SEAT-007", "ORD-005")
        assert ticket1.showtimeId == ticket2.showtimeId


class TestTicketSeatAssociation:
    """Unit test: Ticket-to-Seat relationship"""
    
    def test_seat_association(self):
        ticket = Ticket("TICK-008", "QR44444", "ST-300", "SEAT-A1", "ORD-006")
        assert ticket.seatId == "SEAT-A1"
    
    def test_unique_seat_per_ticket(self):
        ticket1 = Ticket("TICK-009", "QR55555", "ST-400", "SEAT-B5", "ORD-007")
        ticket2 = Ticket("TICK-010", "QR66666", "ST-400", "SEAT-B6", "ORD-007")
        assert ticket1.seatId != ticket2.seatId


class TestTicketOrderAssociation:
    """Unit test: Ticket-to-Order relationship"""
    
    def test_order_association(self):
        ticket = Ticket("TICK-011", "QR77777", "ST-500", "SEAT-C1", "ORD-100")
        assert ticket.orderNumber == "ORD-100"
    
    def test_multiple_tickets_same_order(self):
        ticket1 = Ticket("TICK-012", "QR88888", "ST-600", "SEAT-D1", "ORD-200")
        ticket2 = Ticket("TICK-013", "QR99999", "ST-600", "SEAT-D2", "ORD-200")
        assert ticket1.orderNumber == ticket2.orderNumber


class TestTicketString:
    """Unit test: Ticket string representation"""
    
    def test_str_includes_ticket_id(self):
        ticket = Ticket("TICK-014", "QRABCDE", "ST-700", "SEAT-E1", "ORD-300")
        result = str(ticket)
        assert "TICK-014" in result
    
    def test_str_includes_seat_id(self):
        ticket = Ticket("TICK-015", "QRFGHIJ", "ST-800", "SEAT-F1", "ORD-400")
        result = str(ticket)
        assert "SEAT-F1" in result
