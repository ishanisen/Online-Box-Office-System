
# from Data.data import movie, showtime, auditorium, seats, customers, orders, payments, tickets, theaters


# from utils.utils import find_movie, find_showtimes_for_movie, find_auditorium, \
 #   get_seats_for_auditorium, find_seat_by_label, generate_id


from src.movie import Movie
from src.theater import Theater
from src.auditorium import Auditorium
from src.order import Order
from src.payment import Payment
from src.ticket import Ticket
from src.customer import Customer  # ensure class path matches your project

import uuid
import csv
import os

# def save_ticket_to_csv(ticket, customer=None):
#     """Append ticket to tickets.csv file"""
#     csv_file = "tickets.csv"
#     file_exists = os.path.isfile(csv_file)
    
#     with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             # Write header if file doesn't exist
#             writer.writerow(["TicketId", "QRCode", "ShowtimeId", "SeatId", "OrderNumber", "CustomerEmail", "CustomerName"])
        
#         customer_email = customer.email if customer else "Guest"
#         customer_name = f"{customer.firstName} {customer.lastName}" if customer else "Guest"
#         writer.writerow([ticket.ticketId, ticket.qrCode, ticket.showtimeId, ticket.seatId, ticket.orderNumber, customer_email, customer_name])


# def save_customer_to_csv(customer):
#     """Append customer to customers.csv file"""
#     csv_file = "customers.csv"
#     file_exists = os.path.isfile(csv_file)
    
#     with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
#         writer = csv.writer(f)
#         if not file_exists:
#             # Write header if file doesn't exist
#             writer.writerow(["CustomerID", "FirstName", "LastName", "Email", "Password"])
#         writer.writerow([customer.customerId, customer.firstName, customer.lastName, customer.email, customer.password])


# def load_customers_from_csv():
    
#     """Load customers from CSV file into customers list"""
#     csv_file = "customers.csv"
#     if not os.path.isfile(csv_file):
#         return
    
#     with open(csv_file, mode='r', newline='', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             # Check if customer already exists (avoid duplicates)
#             if not any(c.customerID == row["CustomerID"] for c in customer):
#                 customer = Customer(
#                     row["CustomerID"],
#                     row["FirstName"],
#                     row["LastName"],
#                     row["Email"],
#                     row["Password"]
#                 )
#                 customer.append(customer)

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
            "theaterId": row["theaterID"],
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

#test function to print from the csv files
# print("Loaded seats:", len(all_seats))
# print(all_seats[:5])   # show first 5 rows

# print("Loaded movies:", len(movies))
# print(movies[:5])

# print("Loaded theaters:", len(theaters))
# print(theaters[:5])

# print("Loaded auditoriums:", len(auditoriums))
# print(auditoriums[:5])

# print("Loaded showtimes:", len(showtimes))
# print(showtimes[:5])


# def login_or_register():
#     """
#     Offer login / register / guest options.
#     Returns: Customer object on successful login/register, or None for guest / failed login.
#     """
#     print("\n1) Login\n2) Register\n3) Continue as Guest")
#     choice = input("Choose option: ").strip()

#     if choice == "1":
#         email = input("Email: ").strip()
#         pwd = input("Password: ").strip()

#     elif choice == "2":
#         # Collect registration info
#         em = input("Email: ").strip()
#         fn = input("First name: ").strip()
#         ln = input("Last name: ").strip()

#         # ask for password twice
#         while True:
#             pw = input("Password: ").strip()
#             pw2 = input("Confirm password: ").strip()
#             if pw != pw2:
#                 print("Passwords do not match. Try again.")
#             elif pw == "":
#                 print("Password cannot be empty. Try again.")
#             else:
#                 break

        # # generate a customer id (simple deterministic scheme or use uuid)
        # cid = "C" + str(100 + len(customers) + 1)

        # user = Customer(cid, fn, ln, em, pw)
        # customers.append(user)

        # # call your save function if present; catch exceptions so registration doesn't crash
        # try:
        #     save_customer_to_csv(user)
        # except NameError:
        #     # save function not defined — ignore, but inform developer
        #     pass
        # except Exception as e:
        #     print(f"Warning: failed to save new customer to CSV: {e}")

        # print(f"Registered. Welcome, {fn}!\n")
        # return user

    # else:
    #     print("Continuing as guest.\n")
    #     return None


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


def find_auditorium_by_id(aud_id):
    return next((a for a in auditoriums if a.get("auditoriumID") == aud_id), None)

def find_theater_by_id(t_id):
    return next((t for t in theaters if t.get("theaterID") == t_id), None)

def display_showtimes(movie_id):
    """
    Show showtimes for movie_id with theater name + location (no auditorium shown).
    Uses:
      - showtimes: list of dicts with keys 'showtimeID','datetime','movieID','auditoriumID'
      - auditoriums: list of dicts with keys 'auditoriumID','auditoriumName','theaterID'
      - theaters: list of dicts with keys 'theaterID','theaterName','location'
    """
    filtered = [s for s in showtimes if s.get("movieID") == movie_id]
    if not filtered:
        print(f"\nNo showtimes available for movie {movie_id}.\n")
        return

    header = "{:<12} {:<20} {:<25} {:<40}".format("ShowtimeID", "Date/Time", "Theater", "Location")
    print(f"\n=== Showtimes for {movie_id} ===")
    print(header)
    print("-" * len(header))

    for s in filtered:
        aud_id = s.get("auditoriumID")
        aud = find_auditorium_by_id(aud_id)
        theater_name = "Unknown Theater"
        theater_location = "Unknown Location"

        if aud:
            # auditorium stores the theater id in'theaterID'
            th_id =  aud.get("theaterID")
            theater = find_theater_by_id(th_id)
            if theater:
                theater_name = theater.get("theaterName", theater_name)
                theater_location = theater.get("location", theater_location)
        else:
            # fallback: maybe show the raw auditorium id so dev can debug
            theater_name = f"(aud {aud_id})"

        print("{:<12} {:<20} {:<25} {:<40}".format(
            s.get("showtimeID", ""),
            s.get("datetime", ""),
            theater_name,
            theater_location
        ))
    print()

def select_movie():
    """Displays movies, lets user pick one, then shows its showtimes."""
    
    while True:
        display_movies()
        movie_id = input("Enter Movie ID to view showtimes: ").strip()
        
        # Check if movie exists
        if any(m["movieID"] == movie_id for m in movies):
            display_showtimes(movie_id)
            #return movie_id   # so you can use it later
        else:
            print("Invalid Movie ID. Please try again.\n")

def select_showtime():

    
# selected_movie = select_movie()
# print("User selected:", selected_movie)     


# def display_seats_for_showtime(showtime):
#     aud = find_auditorium(showtime.auditoriumId, auditoriums)
#     aud_name = aud.name if aud else showtime.auditoriumId
#     print(f"\nSeats for {aud_name} (Aud {showtime.auditoriumId}) — showtime {showtime.showtimeId} at {showtime.startAt}")
#     aud_seats = get_seats_for_auditorium(showtime.auditoriumId, seats)
#     rows = {}
#     for s in aud_seats:
#         rows.setdefault(s.rowLabel, []).append(s)
#     for r in sorted(rows.keys()):
#         line = " ".join(f"{s.label()}{'X' if s.taken else ''}" for s in rows[r])
#         print(f"Row {r}: {line}")
#     print("Legend: X = taken (occupied).")


# def choose_seat(showtime):
#     display_seats_for_showtime(showtime)
#     row = input("Enter row (e.g., A): ").strip().upper()
#     num = input("Enter seat number (e.g., 3): ").strip()
#     if not num.isdigit():
#         print("Invalid seat number.")
#         return None
#     num = int(num)
#     seat = find_seat_by_label(showtime.auditoriumId, row, num, seats)
#     if not seat:
#         print("Seat not found.")
#         return None
#     if seat.taken:
#         print("Seat already taken. Choose another.")
#         return None
#     return seat


# def checkout(customer, showtime, seat):
#     # pricing (simple)
#     price = 12.00
#     fees = 1.50
#     tax = round((price + fees) * 0.13, 2)  # example tax
#     orderNumber = generate_id("ORD-")
#     order = Order(orderNumber, price, fees, tax)
#     print("\n--- Order Summary ---")
#     movie = find_movie(showtime.movieId, movies)
#     aud = find_auditorium(showtime.auditoriumId, auditoriums)
#     print(f"Movie: {movie.title if movie else showtime.movieId}")
#     print(f"Showtime: {showtime.startAt} in {aud.name if aud else showtime.auditoriumId}")
#     print(f"Seat: {seat.label()}")
#     print(order)
#     confirm = input("Proceed to payment? (y/n): ").strip().lower()
#     if confirm != "y":
#         print("Order cancelled.")
#         return None

#     provider = input("Enter payment provider (e.g., Visa, Stripe): ").strip()
#     paymentId = generate_id("PAY-")
#     payment = Payment(paymentId, order.grandTotal, provider, "Completed")
#     payments.append(payment)
#     orders.append(order)

#     # finalize seat and ticket
#     seat.taken = True
#     ticketId = generate_id("TKT-")
#     qr = "QR-" + uuid.uuid4().hex[:10]
#     ticket = Ticket(ticketId, qr, showtime.showtimeId, seat.seatId, order.orderNumber)
#     tickets.append(ticket)
#     if customer:
#         customer.orders.append(order)

#     # Save ticket to CSV
#     save_ticket_to_csv(ticket, customer)

#     print("\nPayment successful!")
#     print(payment)
#     print("Your ticket:")
#     print(ticket)
#     return ticket


# def main_menu():
#     # Load existing customers from CSV on startup
#     load_customers_from_csv()
    
#     print("Welcome to the CLI Movie Booking")
#     user = None
#     while True:
#         print("\n--- Main Menu ---")
#         print("1) Login/Register/Guest")
#         print("2) Browse Movies")
#         print("3) Exit")
#         choice = input("Select: ").strip()
#         if choice == "1":
#             user = login_or_register()
#         elif choice == "2":
#             st = select_movie()
#             if not st:
#                 continue
#             seat = None
#             while seat is None:
#                 seat = choose_seat(st)
#                 if seat is None:
#                     again = input("Try again? (y/n): ").strip().lower()
#                     if again != "y":
#                         break
#             if seat:
#                 _ = checkout(user, st, seat)
#         elif choice == "3":
#             print("Goodbye.")
#             break
#         else:
#             print("Invalid choice.")


# if __name__ == "__main__":
#     main_menu()
