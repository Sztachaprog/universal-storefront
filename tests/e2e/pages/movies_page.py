

class MoviesPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("http://localhost:5000/movies")

    def choose_premium_movie(self):
        self.page.locator('.movie-card').filter(has=self.page.locator(".tag.premium")).click()

    def choose_non_premium_movie(self):
        self.page.locator('.movie-card').filter(has=self.page.locator(".tag.free")).click()

    def press_watch_button(self):
        self.page.click("#watch-btn")

    def get_movie_cards_count(self):
        return self.page.locator(".movie-card").count()

    def get_movie_titles(self):
        return self.page.locator(".movie-title").all_inner_texts()