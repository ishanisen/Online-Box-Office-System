# src/datastore.py

class DataStore:
    def __init__(self):
        self.theaters = []
        self.auditoriums = []
        self.movies = []
        self.showtimes = []
        self.seats = []
        self.customers = []
        
        # Runtime-created data
        self.orders = []
        self.payments = []
        self.tickets = []

    def load_hardcoded_data(self):
        from Data.data import (
            theaters, auditoriums, movies, showtimes,
            seats, customers
        )

        self.theaters = theaters
        self.auditoriums = auditoriums
        self.movies = movies
        self.showtimes = showtimes
        self.seats = seats
        self.customers = customers
