from playwright.sync_api import expect

from tests.e2e.pages.movies_page import MoviesPage
from tests.e2e.pages.login_page import LoginPage

from src.application import get_movie_details

import allure 

allure.feature("E2E movies")
@allure.story("access control")
def test_non_logged_user_cannot_enter_movie_watch(page, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/login")

allure.feature("E2E movies")
@allure.story("access control")
def test_non_premium_user_can_watch_non_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{non_premium_movie}/watch")

allure.feature("E2E movies")
@allure.story("access control")
def test_non_premium_user_cannot_watch_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    premium_movie = add_premium_and_non_premium_movies[0]

    page.goto(f"http://localhost:5000/movies/{premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{premium_movie}")
    
allure.feature("E2E movies")
@allure.story("access control")    
def test_premium_user_cann_watch_premium_movie_via_direct_url(page, login_premium_user, add_premium_and_non_premium_movies):

    premium_movie = add_premium_and_non_premium_movies[0]

    page.goto(f"http://localhost:5000/movies/{premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{premium_movie}/watch")

def test_movie_cards_count_and_titles(page, login_non_premium_user, add_premium_and_non_premium_movies, cursor):

    premium_movie = add_premium_and_non_premium_movies[0]
    non_premium_movie = add_premium_and_non_premium_movies[1]

    premium_movie_title = get_movie_details(premium_movie, "en", cursor = cursor)[3]
    non_premium_movie_title = get_movie_details(non_premium_movie, "en", cursor = cursor)[3]

    movies_page = MoviesPage(page)

    movies_page.navigate()

    assert movies_page.get_movie_cards_count() == 2, "Should be 2 movie cards"
    assert set(movies_page.get_movie_titles()) == {premium_movie_title, non_premium_movie_title, "nice"}, "invalid movie titles"