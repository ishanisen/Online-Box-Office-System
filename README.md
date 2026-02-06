# Online Box Office System

A **command-line movie ticket booking system** developed in **Python** that simulates the core functionality of an online cinema box office.  
The system allows users to securely authenticate, browse movies and showtimes, select seats from a seating plan, and complete a ticket booking workflow with simulated payment processing.

---

## Features

### User Authentication
- Register, login, or continue as a guest  
- Passwords securely hashed using **bcrypt**  
- Email and password input validation  

### Movie & Showtime Browsing
- Browse available movies  
- View showtimes by location and date  
- Display movie details (runtime, rating, synopsis)  

### Seat Selection
- Interactive seat map rendering  
- Real-time seat availability (Available / Held / Sold)  
- Prevents double-booking of seats  

### Checkout & Ticketing
- Simulated payment processing  
- Order creation and ticket generation  
- Seat inventory updated after successful booking  

### Testing & Performance
- Unit and integration testing  
- cProfile used to analyze runtime performance  
- Deterministic non-interactive profiling mode  

### Accessibility & Usability
- Clear step-by-step instructions  
- User-friendly error messages  
- Keyboard-navigable interface  
- Designed with POUR accessibility principles 

---

## 📂 Project Structure

```text
.
├── src/
│   ├── __init__.py
│   ├── customer.py        # Customer model & authentication logic
│   ├── order.py           # Order creation and pricing logic
│   ├── payment.py         # Payment processing (simulated)
│   ├── ticket.py          # Ticket generation and validation
│   └── utilities.py       # Helper and utility functions
│
├── main.py                # Application entry point
│
├── customers.csv          # Customer data (hashed passwords)
├── movies.csv             # Movie information
├── showtimes.csv          # Showtime schedules
├── theaters.csv           # Theater data
├── auditoriums.csv        # Auditorium layouts
├── all_seats.csv          # Seat definitions
├── tickets.csv            # Issued tickets
│
├── test_customer.py
├── test_order.py
├── test_payment.py
├── test_ticket.py
├── test_module_integration.py
├── test_system_workflow.py
│
└── README.md

