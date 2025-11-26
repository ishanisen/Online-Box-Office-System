class Movie:
    def __init__(self, movieID: str, title: str, rating: str, runtimeMin: int, language: str):
        self.movieID = movieID
        self.title = title
        self.rating = rating
        self.runtimeMin = runtimeMin
        self.language = language

    def __str__(self):
        return (
            f"Movie ID: {self.movieID}\n"
            f"Title: {self.title}\n"
            f"Rating: {self.rating}\n"
            f"Run Time: {self.runtimeMin} mins\n"
            f"Language: {self.language}"
        )
    def get_showtimes(self, all_showtimes):
        return [s for s in all_showtimes if s.movieID == self.movieID]
    