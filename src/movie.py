class Movie:
    def __init__(self, movieId: str, title: str, rating: str, runtimeMin: int, language: str):
        self.movieId = movieId
        self.title = title
        self.rating = rating
        self.runtimeMin = runtimeMin
        self.language = language

    def __str__(self):
        return (
            f"Movie ID: {self.movieId}\n"
            f"Title: {self.title}\n"
            f"Rating: {self.rating}\n"
            f"Run Time: {self.runtimeMin} mins\n"
            f"Language: {self.language}"
        )
    def get_showtimes(self, all_showtimes):
        return [s for s in all_showtimes if s.movieId == self.movieId]
    