
from Data.data import movies, showtimes, auditoriums, seats, customers, orders, payments, tickets, theaters


from utils.utils import find_movie, find_showtimes_for_movie, find_auditorium, \
    get_seats_for_auditorium, find_seat_by_label, generate_id

from src.order import Order
from src.payment import Payment
from src.ticket import Ticket
from src.customer import Customer  # ensure class path matches your project

import uuid
import csv
import os


def save_ticket_to_csv(ticket, customer=None):
    """Append ticket to tickets.csv file"""
    csv_file = "tickets.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if file doesn't exist
            writer.writerow(["TicketId", "QRCode", "ShowtimeId", "SeatId", "OrderNumber", "CustomerEmail", "CustomerName"])
        
        customer_email = customer.email if customer else "Guest"
        customer_name = f"{customer.firstName} {customer.lastName}" if customer else "Guest"
        writer.writerow([ticket.ticketId, ticket.qrCode, ticket.showtimeId, ticket.seatId, ticket.orderNumber, customer_email, customer_name])


def save_customer_to_csv(customer):
    """Append customer to customers.csv file"""
    csv_file = "customers.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if file doesn't exist
            writer.writerow(["CustomerId", "FirstName", "LastName", "Email", "Password"])
        writer.writerow([customer.customerId, customer.firstName, customer.lastName, customer.email, customer.password])


def load_customers_from_csv():
    """Load customers from CSV file into customers list"""
    csv_file = "customers.csv"
    if not os.path.isfile(csv_file):
        return
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check if customer already exists (avoid duplicates)
            if not any(c.customerId == row["CustomerId"] for c in customers):
                customer = Customer(
                    row["CustomerId"],
                    row["FirstName"],
                    row["LastName"],
                    row["Email"],
                    row["Password"]
                )
                customers.append(customer)


def login_or_register():
    print("\n1) Login\n2) Register\n3) Continue as Guest")
    choice = input("Choose option: ").strip()
    if choice == "1":
        email = input("Email: ").strip()
        pwd = input("Password: ").strip()
        user = next((u for u in customers if u.email == email and u.password == pwd), None)
        if user:
            print(f"Welcome back, {user.firstName}!\n")
            return user
        else:
            print("Invalid login.")
            return None

    elif choice == "2":
        cid = "C" + str(100 + len(customers) + 1)
        fn = input("First name: ").strip()
        ln = input("Last name: ").strip()
        em = input("Email: ").strip()
        pw = input("Password: ").strip()
        user = Customer(cid, fn, ln, em, pw)
        customers.append(user)
        save_customer_to_csv(user)
        print(f"Registered. Welcome, {fn}!\n")
        return user

    else:
        print("Continuing as guest.\n")
        return None


def display_movies():
    print("\n=== Available Movies ===")
    for m in movies:
        print(f"{m.movieId}: {m.title} — {m.rating} — {m.runtimeMin} min")
    print()


def select_movie():
    display_movies()
    mid = input("Enter movie ID to view showtimes (or 'q' to quit): ").strip()
    if mid.lower() == "q":
        return None
    movie = find_movie(mid, movies)
    if not movie:
        print("Movie not found.")
        return None
    sts = find_showtimes_for_movie(mid, showtimes)
    if not sts:
        print("No showtimes.")
        return None
    print(f"\nShowtimes for {movie.title}:")
    for s in sts:
        aud = find_auditorium(s.auditoriumId, auditoriums)
        aud_name = aud.name if aud else s.auditoriumId
        print(f"{s.showtimeId}: {s.startAt} — {aud_name} (Aud {s.auditoriumId})")
    sid = input("Enter showtime ID to select (or 'b' to go back): ").strip()
    if sid.lower() == "b":
        return None
    st = next((x for x in sts if x.showtimeId == sid), None)
    if not st:
        print("Showtime not found.")
        return None
    return st


def display_seats_for_showtime(showtime):
    aud = find_auditorium(showtime.auditoriumId, auditoriums)
    aud_name = aud.name if aud else showtime.auditoriumId
    print(f"\nSeats for {aud_name} (Aud {showtime.auditoriumId}) — showtime {showtime.showtimeId} at {showtime.startAt}")
    aud_seats = get_seats_for_auditorium(showtime.auditoriumId, seats)
    rows = {}
    for s in aud_seats:
        rows.setdefault(s.rowLabel, []).append(s)
    for r in sorted(rows.keys()):
        line = " ".join(f"{s.label()}{'X' if s.taken else ''}" for s in rows[r])
        print(f"Row {r}: {line}")
    print("Legend: X = taken (occupied).")


def choose_seat(showtime):
    display_seats_for_showtime(showtime)
    row = input("Enter row (e.g., A): ").strip().upper()
    num = input("Enter seat number (e.g., 3): ").strip()
    if not num.isdigit():
        print("Invalid seat number.")
        return None
    num = int(num)
    seat = find_seat_by_label(showtime.auditoriumId, row, num, seats)
    if not seat:
        print("Seat not found.")
        return None
    if seat.taken:
        print("Seat already taken. Choose another.")
        return None
    return seat


def checkout(customer, showtime, seat):
    # pricing (simple)
    price = 12.00
    fees = 1.50
    tax = round((price + fees) * 0.13, 2)  # example tax
    orderNumber = generate_id("ORD-")
    order = Order(orderNumber, price, fees, tax)
    print("\n--- Order Summary ---")
    movie = find_movie(showtime.movieId, movies)
    aud = find_auditorium(showtime.auditoriumId, auditoriums)
    print(f"Movie: {movie.title if movie else showtime.movieId}")
    print(f"Showtime: {showtime.startAt} in {aud.name if aud else showtime.auditoriumId}")
    print(f"Seat: {seat.label()}")
    print(order)
    confirm = input("Proceed to payment? (y/n): ").strip().lower()
    if confirm != "y":
        print("Order cancelled.")
        return None

    provider = input("Enter payment provider (e.g., Visa, Stripe): ").strip()
    paymentId = generate_id("PAY-")
    payment = Payment(paymentId, order.grandTotal, provider, "Completed")
    payments.append(payment)
    orders.append(order)

    # finalize seat and ticket
    seat.taken = True
    ticketId = generate_id("TKT-")
    qr = "QR-" + uuid.uuid4().hex[:10]
    ticket = Ticket(ticketId, qr, showtime.showtimeId, seat.seatId, order.orderNumber)
    tickets.append(ticket)
    if customer:
        customer.orders.append(order)

    # Save ticket to CSV
    save_ticket_to_csv(ticket, customer)

    print("\nPayment successful!")
    print(payment)
    print("Your ticket:")
    print(ticket)
    return ticket


def main_menu():
    # Load existing customers from CSV on startup
    load_customers_from_csv()
    
    print("Welcome to the CLI Movie Booking")
    user = None
    while True:
        print("\n--- Main Menu ---")
        print("1) Login/Register/Guest")
        print("2) Browse Movies")
        print("3) Exit")
        choice = input("Select: ").strip()
        if choice == "1":
            user = login_or_register()
        elif choice == "2":
            st = select_movie()
            if not st:
                continue
            seat = None
            while seat is None:
                seat = choose_seat(st)
                if seat is None:
                    again = input("Try again? (y/n): ").strip().lower()
                    if again != "y":
                        break
            if seat:
                _ = checkout(user, st, seat)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main_menu()
