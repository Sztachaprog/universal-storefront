from playwright.sync_api import expect

from tests.e2e.pages.movies_page import MoviesPage
from tests.e2e.pages.login_page import LoginPage


def test_non_logged_user_cannot_enter_movie_watch(page, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/login")


def test_non_premium_user_can_watch_non_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{non_premium_movie}/watch")


def test_non_premium_user_cannot_watch_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    premium_movie = add_premium_and_non_premium_movies[0]

    page.goto(f"http://localhost:5000/movies/{premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{premium_movie}")
    
# def test_premium_user_watches_non_premium_movie(page, login_premium_user, add_premium_and_non_premium_movies):

#     movies_page = MoviesPage(page)

#     movies_page.navigate()
#     movies_page.choose_non_premium_movie()
#     movies_page.press_watch_button()

#     assert page.locator("#player-screen").is_visible() == True, "Player screen should be visible"

# def test_premium_user_watches_premium_movie(page, login_premium_user, add_premium_and_non_premium_movies):

#     movies_page = MoviesPage(page)

#     movies_page.navigate()
#     movies_page.choose_premium_movie()
#     movies_page.press_watch_button()

#     assert page.locator("#player-screen").is_visible() == True, "Player screen should be visible"