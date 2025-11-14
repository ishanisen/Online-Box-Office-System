class movie:
    def __init__(self, title:str, rating:str, runtimeMin:int, language:str):
        self.title = title
        self.rating = rating
        self.runtimeMin = runtimeMin
        self.language = language

    def __str__(self):
        return f"Title: {self.title}\nRating: {self.rating}\nRun Time: {self.runtimeMin} mins\nLanguage: {self.language}"

    def read(cls):
        "Movie"
        title = input("Enter movie title: ")
        rating = input("Enter movie rating : ")
        runtime = int(input("Enter runtime in minutes: "))
        language = input("Enter language: ")
        return cls(title=title, rating=rating, runtime_min=runtime, language=language)


#movie1 = movie("Jab Tak Hai Jaan", 4, 270, "Hindi")
#print(movie1)
        
