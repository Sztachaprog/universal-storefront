

class MoviesPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("http://localhost:5000/movies")

    def choose_premium_movie(self):
        self.page.locator('[data-movie-id="2"]').click()

    def choose_non_premium_movie(self):
        self.page.locator('[data-movie-id="2"]').click()


    