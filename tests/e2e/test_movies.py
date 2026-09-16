from playwright.sync_api import expect

from tests.e2e.pages.movies_page import MoviesPage
from tests.e2e.pages.login_page import LoginPage

from src.application import get_movie_details

import allure 

@allure.feature("E2E movies")
@allure.story("access control")
def test_non_logged_user_cannot_enter_movie_watch(page, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/login")

@allure.feature("E2E movies")
@allure.story("access control")
def test_non_premium_user_can_watch_non_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    non_premium_movie = add_premium_and_non_premium_movies[1]

    page.goto(f"http://localhost:5000/movies/{non_premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{non_premium_movie}/watch")

@allure.feature("E2E movies")
@allure.story("access control")
def test_non_premium_user_cannot_watch_premium_movie_via_direct_url(page, login_non_premium_user, add_premium_and_non_premium_movies):

    premium_movie = add_premium_and_non_premium_movies[0]

    page.goto(f"http://localhost:5000/movies/{premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{premium_movie}")
    
@allure.feature("E2E movies")
@allure.story("access control")    
def test_premium_user_cann_watch_premium_movie_via_direct_url(page, login_premium_user, add_premium_and_non_premium_movies):

    premium_movie = add_premium_and_non_premium_movies[0]

    page.goto(f"http://localhost:5000/movies/{premium_movie}/watch")
    expect(page).to_have_url(f"http://localhost:5000/movies/{premium_movie}/watch")

@allure.feature("E2E movies")
@allure.story("UI tests") 
def test_movie_cards_count_and_titles(page, login_non_premium_user, add_premium_and_non_premium_movies, cursor):

    premium_movie = add_premium_and_non_premium_movies[0]
    non_premium_movie = add_premium_and_non_premium_movies[1]

    premium_movie_title = get_movie_details(premium_movie, "en", cursor = cursor)[3]
    non_premium_movie_title = get_movie_details(non_premium_movie, "en", cursor = cursor)[3]

    movies_page = MoviesPage(page)

    movies_page.navigate()

    expect(movies_page.get_movie_cards()).to_have_count(2)
    assert set(movies_page.get_movie_titles()) == {premium_movie_title, non_premium_movie_title}, "invalid movie titles"

@allure.feature("E2E movies")
@allure.story("UI tests") 
def test_non_premium_user_cannot_watch_premium_movie(page, login_non_premium_user, add_premium_and_non_premium_movies, cursor):


    movies_page = MoviesPage(page)

    movies_page.navigate()
    movies_page.choose_premium_movie()

    expect(movies_page.watch_button()).to_have_count(0)
    expect(movies_page.get_upgrade_to_premium_button()).to_be_visible()

    (movies_page.get_upgrade_to_premium_button()).click()

    expect(page).to_have_url("http://localhost:5000/dashboard")

@allure.feature("E2E movies")
@allure.story("UI tests") 
def test_premium_user_can_watch_premium_movie(page, login_premium_user, add_premium_and_non_premium_movies, cursor):

    movies_page = MoviesPage(page)

    movies_page.navigate()
    movies_page.choose_premium_movie()
    movies_page.press_watch_button()

    expect(movies_page.get_player_screen()).to_be_visible()

@allure.feature("E2E movies")
@allure.story("UI tests") 
def test_non_premium_user_can_watch_non_premium_movie(page, login_non_premium_user, add_premium_and_non_premium_movies, cursor):

    movies_page = MoviesPage(page)

    movies_page.navigate()
    movies_page.choose_non_premium_movie()
    movies_page.press_watch_button()

    expect(movies_page.get_player_screen()).to_be_visible()