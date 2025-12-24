from src.order import Order
from src.payment import Payment
from src.ticket import Ticket
from src.customer import Customer
from io import StringIO
from utilities import hash_password, verify_password, ensure_hashed_password
from utilities import sanitize_string, is_valid_email, is_strong_password, name_ok, email_unique
import uuid
import csv
import os

# Read the CSV file containing all seat information
all_seats = []
with open("all_seats.csv", mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_seats.append({
            "seatID": row["seatID"],
            "auditoriumID": row["auditoriumID"],
            "rowLabel": row["row_label"],
            "seatNumber": int(row["seatNumber"]),
            "label": row["label"],
            "taken": row["taken"] == "True"
        })

# read the movies.csv file
movies = []
with open("movies.csv", mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        movies.append({
            "movieID": row["movieID"],
            "title": row["title"],
            "rating": row["rating"],
            "runtimeMin": row["runtimeMin"],
            "language": row["language"]
        })

# read theaters.csv file
theaters = []
with open("theaters.csv", mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        theaters.append({
            "theaterID": row["theaterID"],
            "theaterName": row["theaterName"],
            "location": row["location"],
        })




#read the auditoriums.csv file
auditoriums = []
with open("auditoriums.csv", mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        auditoriums.append({
            "auditoriumID": row["auditoriumID"],
            "auditoriumName": row["auditoriumName"],
            "theaterID": row["theaterID"],
        })   

#read the showtimes.csv file
showtimes = []
with open("showtimes.csv", mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        showtimes.append({
            "showtimeID": row["showtimeID"],
            "datetime": row["datetime"],
            "movieID": row["movieID"],
            "auditoriumID": row["auditoriumID"],
        })  


def load_seats_from_csv():
    """Reload all seats from CSV file"""
    global all_seats
    all_seats = []
    with open("all_seats.csv", mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_seats.append({
                "seatID": row["seatID"],
                "auditoriumID": row["auditoriumID"],
                "rowLabel": row["row_label"],
                "seatNumber": int(row["seatNumber"]),
                "label": row["label"],
                "taken": row["taken"] == "True"
            })


#Global customers list used by other function
customers= []

def save_customer_to_csv(customer):
    """Append customer to customers.csv file"""
    csv_file = "customers.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if file doesn't exist
            writer.writerow(["CustomerId", "FirstName", "LastName", "Email", "Password"])
        writer.writerow([customer.customerID, customer.firstName, customer.lastName, customer.email, customer.password])


def load_customers_from_csv():
    """Load customers from CSV file into customers list"""
    csv_file = "customers.csv"
    if not os.path.isfile(csv_file):
        return
    
    with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:

            # Skip rows missing CustomerId
            if not row.get("CustomerId"):
                continue

            # Avoid duplicates: check by customerID
            if any(c.customerID == row["CustomerId"] for c in customers):
                continue

            # Create Customer object and append
            c = Customer(
                row.get("CustomerId", ""),
                row.get("FirstName", ""),
                row.get("LastName", ""),
                row.get("Email", ""),
                row.get("Password", "")
            )
            customers.append(c)


def login_or_register():
    """
    Offer login/register/guest options.
    Returns: Customer object on successful login/register, or None for guest/failed login.
    """
    while True:
        print("\n1) Login\n2) Register\n3) Continue as Guest")
        choice = input("Choose option: ").strip()

        if choice == "1":
            email = sanitize_string(input("Email: "))
            pwd = input("Password: ").strip()  # do not sanitize password (preserve whitespace if user intended)
            if not is_valid_email(email):
                print("Invalid email format. Try again.\n")
                continue

            found = next((c for c in customers if c.email.strip().lower() == email.lower()), None)

            if not found:
                print("No account with that email. Try registering.\n")
                continue

            if verify_password(pwd, found.password):
                try:
                    ensure_hashed_password(found, save_customer_to_csv)
                except Exception as e:
                    print(f"Warning: failed to upgrade stored password hashing: {e}")
                print(f"Welcome back, {found.firstName}!")
                return found
            else:
                # Don't reveal whether email exists — but we already validated existence above.
                print("Login failed. Check credentials and try again.\n")

        elif choice == "2":
            # collect and validate registration info
            em = sanitize_string(input("Email: "))
            if not is_valid_email(em):
                print("Invalid email. Please use a valid email address.\n")
                continue
            if not email_unique(em, customers):
                print("An account with that email already exists. Try logging in or use a different email.\n")
                continue

            fn = sanitize_string(input("First Name: "))
            if not name_ok(fn):
                print("First name cannot be empty and must be reasonably short.\n")
                continue

            ln = sanitize_string(input("Last Name: "))
            if not name_ok(ln):
                print("Last name cannot be empty and must be reasonably short.\n")
                continue

            # ask for password twice with validation
            while True:
                print("Password: \n - must have atleast 8 characters\n - include one digit atleast\n - should include both upper and lower case letters\n - must include at least one special character (e.g. !@#$%) ")
                pw = input("Enter New Password: ")
                pw2 = input("Confirm Password: ")
                if pw != pw2:
                    print("Passwords do not match. Try again.")
                    continue
                ok, msg = is_strong_password(pw)
                if not ok:
                    print(f"Password not strong enough: {msg} Try again.")
                    continue
                break

            # hash the validated password before storing
            pw_hash = hash_password(pw)

            # generate a customer id
            cid = "C" + str(100 + len(customers) + 1)

            user = Customer(cid, fn, ln, em, pw_hash)
            customers.append(user)

            try:
                save_customer_to_csv(user)
            except Exception as e:
                print(f"Warning: failed to save new customer to CSV: {e}")

            print(f"Registered. Welcome, {fn}!\n")
            return user

        elif choice == "3":
            print("Continuing as guest.\n")
            return None

        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")



# displays movie in a table form
def display_movies():
    global movies
    print("\n=== Available Movies ===")
    # Header
    print("{:<6} {:<25} {:<8} {:<10}".format("ID", "Title", "Rating", "Runtime"))
    print("-" * 55)
    # Rows
    for m in movies:
        print("{:<6} {:<25} {:<8} {:<10}".format(
            m["movieID"], m["title"], m["rating"], str(m["runtimeMin"]) + " min"
        ))
    print()

#Helper Functions
def find_auditorium_by_id(aud_id):
    if aud_id is None:
        return None
    aud_id_s = str(aud_id).strip()
    return next((a for a in auditoriums if str(a.get("auditoriumID", "")).strip() == aud_id_s), None)


def find_theater_by_id(tid):
    if tid is None:
        return None
    tid_s = str(tid).strip()
    return next((t for t in theaters if str(t.get("theaterID", "")).strip() == tid_s), None)


def get_seats_for_auditorium(aud_id):
    return [s for s in all_seats if s["auditoriumID"] == aud_id]

def mark_seat_taken(seatID):
    for s in all_seats:
        if s.get("seatID") == seatID:
            s["taken"] = True
            break


def display_showtimes(movie_id):
    filtered = [s for s in showtimes if s.get("movieID") == movie_id]
    if not filtered:
        print(f"\nNo showtimes available for movie {movie_id}.\n")
        return

    header = "{:<12} {:<20} {:<25} {:<40}".format("ShowtimeID", "Date/Time", "Theater", "Location")
    print(f"\n=== Showtimes for {movie_id} ===")
    print(header)
    print("-" * len(header))

    for s in filtered:
        theater_name = "Unknown Theater"
        theater_location = "Unknown Location"

        aud_id = s.get("auditoriumID")
        aud = find_auditorium_by_id(aud_id)
        if aud:
            th_id = aud.get("theaterID")
            theater = find_theater_by_id(th_id)
            if theater:
                theater_name = theater.get("theaterName", theater_name)
                theater_location = theater.get("location", theater_location)
            else:
                theater_name = f"(aud {aud.get('auditoriumName','?')})"
                theater_location = f"(theater id {th_id} not found)"
        else:
            direct_th_id = s.get("theaterID") or s.get("theatreID")
            if direct_th_id is not None:
                theater = find_theater_by_id(direct_th_id)
                if theater:
                    theater_name = theater.get("theaterName", theater_name)
                    theater_location = theater.get("location", theater_location)
                else:
                    theater_name = f"(theater id {direct_th_id} not found)"
            else:
                if aud_id is not None:
                    theater_name = f"(aud {aud_id})"

        print("{:<12} {:<20} {:<25} {:<40}".format(
            s.get("showtimeID", ""),
            s.get("datetime", ""),
            theater_name,
            theater_location
        ))
    print()


def select_movie():
    """Displays movies, lets user pick one"""
    
    display_movies()
    movie_id = input("Enter Movie ID to view showtimes: ").strip()
        
        # Check if movie exists
    if any(m["movieID"] == movie_id for m in movies):
        return movie_id   # so you can use it later
    else:
        print("Invalid Movie ID. Please try again.\n")
        return None

def select_showtime(movie_id):
    """Displays showtimes for a given movie and lets user pick one."""
    display_showtimes(movie_id)
    showtime_id = input("Enter Showtime ID to view seats: ").strip()
    if any(s["showtimeID"] == showtime_id for s in showtimes):
        return showtime_id
    else:
        print("Invalid Showtime ID. Please try again.\n")
        return None
    
    
def display_seats_for_showtime(showtime_id):
    """
    Display a visual seat map like in a cinema booking system:
    - Rows labeled A, B, C...
    - Columns numbered
    - '.' for available, 'O' for reserved (taken)
    """
    selected_showtime = next((s for s in showtimes if s["showtimeID"] == showtime_id), None)

    if not selected_showtime:
        print("Showtime not found.")
        return
    
    aud_id = selected_showtime["auditoriumID"]
    seats = get_seats_for_auditorium(aud_id)
    
    if not seats:
        print(f"No seats found for auditorium {aud_id}")
        return

    # Group seats by row
    rows = {}
    for s in seats:
        rows.setdefault(s["rowLabel"], []).append(s)

    # Sort rows alphabetically, seats numerically
    sorted_row_labels = sorted(rows.keys())
    max_seats_in_row = max(len(r) for r in rows.values())

    # Print screen header
    screen_width = max_seats_in_row * 3 + 6
    print("\n" + " " * ((screen_width - 6) // 2) + "S C R E E N")
    print("-" * screen_width)
    print("Legend: '.' = Available, 'O' = Reserved\n")

    # Print each row
    for r in sorted_row_labels[::-1]:  # Reverse to have A at the bottom
        row_seats = sorted(rows[r], key=lambda x: x["seatNumber"])
        seat_line = "  ".join("O" if s["taken"] else "." for s in row_seats)
        print(f"{r}      {seat_line}")

    # Print seat numbers at bottom
    seat_numbers = "  ".join(str(s["seatNumber"]) for s in sorted(rows[sorted_row_labels[0]], key=lambda x: x["seatNumber"]))
    print(f"       {seat_numbers}\n")

def select_seat(showtime_id):
    display_seats_for_showtime(showtime_id)
    seat_label = input("Enter seat ID to reserve: ").strip().upper()
    
    # Get the showtime and its auditorium
    selected_showtime = next((s for s in showtimes if s["showtimeID"] == showtime_id), None)
    if not selected_showtime:
        print("Showtime not found.")
        return None
    
    aud_id = selected_showtime["auditoriumID"]
    
    # Find seat by label AND auditorium (not just label!)
    matching_seat = next((s for s in all_seats if s["label"] == seat_label and s["auditoriumID"] == aud_id), None)
    if not matching_seat:
        print("Invalid Seat ID. Please try again.")
        return None
    
    # Check if seat is already taken
    if matching_seat["taken"]:
        print(f"Seat {seat_label} is already taken. Please choose another seat.")
        return None
    
    return matching_seat["seatID"]


def checkout(customer, showtime_id, seat_id):
    """Process payment and create ticket"""
    # Get seat object
    seat = next((s for s in all_seats if s["seatID"] == seat_id), None)
    if not seat:
        print("Seat not found.")
        return None
    
    if seat["taken"]:
        print("Seat already taken.")
        return None
    
    # Get showtime and movie info
    showtime = next((st for st in showtimes if st["showtimeID"] == showtime_id), None)
    movie = next((m for m in movies if m["movieID"] == showtime["movieID"]), None) if showtime else None
    auditorium = next((a for a in auditoriums if a["auditoriumID"] == showtime["auditoriumID"]), None) if showtime else None
    theater = next((t for t in theaters if t["theaterID"] == auditorium["theaterID"]), None) if auditorium else None
    
    # Pricing
    price = 12.00
    fees = 1.50
    tax = round((price + fees) * 0.13, 2)
    
    # Create order
    orderNumber = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    order = Order(orderNumber, price, fees, tax)
    
    # Display order summary
    print("\n" + "="*50)
    print("ORDER SUMMARY")
    print("="*50)
    print(f"Movie: {movie['title'] if movie else 'Unknown'}")
    print(f"Theater: {theater['theaterName'] if theater else 'Unknown'}")
    print(f"Location: {theater['location'] if theater else 'Unknown'}")
    print(f"Auditorium: {auditorium['auditoriumName'] if auditorium else 'Unknown'}")
    print(f"Showtime: {showtime['datetime'] if showtime else 'Unknown'}")
    print(f"Seat: {seat['label']}")
    print(f"\nSubtotal: ${price:.2f}")
    print(f"Fees: ${fees:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"TOTAL: ${order.grandTotal:.2f}")
    print("="*50)
    
    confirm = input("\nProceed to payment? (y/n): ").strip().lower()
    if confirm != "y":
        print("Order cancelled.")
        return None
    
    # Process payment
    provider = input("Enter payment provider (Visa/MasterCard/Debit): ").strip()
    if not provider:
        provider = "Card"
    
    paymentId = f"PAY-{uuid.uuid4().hex[:8].upper()}"
    payment = Payment(paymentId, order.grandTotal, provider, "Completed")
    
    # Mark seat as taken
    seat["taken"] = True
    
    # Update CSV to mark seat as taken
    with open("all_seats.csv", mode='r', newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    
    for row in rows:
        if row["seatID"] == seat_id:
            row["taken"] = "True"
    
    with open("all_seats.csv", mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["seatID", "auditoriumID", "row_label", "seatNumber", "label", "taken"])
        writer.writeheader()
        writer.writerows(rows)
    
    # Reload seats to keep in-memory data in sync
    load_seats_from_csv()
    
    # Create ticket
    ticketId = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    qr = "QR-" + uuid.uuid4().hex[:10]
    
    # Save ticket to CSV
    csv_file = "tickets.csv"
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["TicketId", "QRCode", "ShowtimeId", "SeatId", "OrderNumber", "CustomerEmail", "CustomerName"])
        
        customer_email = customer.email if customer else "Guest"
        customer_name = f"{customer.firstName} {customer.lastName}" if customer else "Guest"
        writer.writerow([ticketId, qr, showtime_id, seat_id, orderNumber, customer_email, customer_name])
    
    print("\n" + "="*50)
    print("PAYMENT SUCCESSFUL!")
    print("="*50)
    print(f"Payment ID: {paymentId}")
    print(f"Amount Charged: ${payment.amount:.2f}")
    print(f"Payment Method: {payment.paymentProvider}")
    print(f"\nTicket ID: {ticketId}")
    print(f"QR Code: {qr}")
    print(f"Seat: {seat['label']}")
    print("="*50)
    print("\nYour ticket has been saved. Enjoy your movie!\n")
    
    return ticketId


def book_movie(customer):
    """Extracted repeated booking flow into single function"""
    movie_id = None
    while not movie_id:
        movie_id = select_movie()
    
    showtime_id = None
    while not showtime_id:
        showtime_id = select_showtime(movie_id)
    
    seat_id = None
    while not seat_id:
        seat_id = select_seat(showtime_id)
    
    # Process checkout
    checkout(customer, showtime_id, seat_id)


# Main Application Loop
def main():
    load_customers_from_csv() #preload saved customers
    current_user = None
    

    while True:
        #Top-level menu
        print("\nWelcome to Inox Cinemas!")
        print("\n=== Main Menu ===")
        print("1) Login/ Register / Continue as Guest")
        print("2) Browse Movies")
        print("3) Exit")
        choice = input("Choose option: ").strip()

        if choice == "1":
            current_user = login_or_register()
            book_movie(current_user)

        elif choice == "2":
            book_movie(current_user)
        
        elif choice == "3":
            print("Goodbye!")
            return
        
        else:
            print("Invalid option. Please try again")


if __name__ == "__main__":
    main()