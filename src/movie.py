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

    @classmethod
    def read(cls):
        movieId = input("Enter Movie ID: ")
        title = input("Enter movie title: ")
        rating = input("Enter movie rating: ")
        runtime = int(input("Enter runtime in minutes: "))
        language = input("Enter language: ")
        return cls(movieId=movieId, title=title, rating=rating, runtimeMin=runtime, language=language)


#movie1 = movie("Avataar", PG-13, 300, "English")
#print(movie1)
        
