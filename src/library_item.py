class LibraryItem:
    
    def __init__(self, name, artist, rating = 0, path = None):
        self.name = name
        self.artist = artist
        self.rating = rating
        self.path = path
        self.play_count = 0

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"
    
    def stars(self):
        stars = ""

        for i in range(self.rating):
            stars += "*"
        
        return stars