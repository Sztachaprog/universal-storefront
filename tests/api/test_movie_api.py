from src.application import (
    create_movie,
    register_user,
    grant_ppv_access
)

import requests
import allure
from datetime import datetime, timezone, timedelta
from tests.api.conftest import BASE_URL

@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_premium_user_watches_premium_movie(cursor, conn, create_token):

    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=True, cursor=cursor)
    movie_id = create_movie("2000-01-01", True, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()

    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200, f"Premium user should be able to watch movie, got status code:{response.status_code}"

@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_non_premium_user_watches_premium_movie(cursor, conn, create_token):

    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
    movie_id = create_movie("2000-01-01", True, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()

    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 403, f"Non premium user should not be able to watch movie, got status code:{response.status_code}"

@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_non_premium_user_watches_non_premium_movie(cursor, conn, create_token):

    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
    movie_id = create_movie("2000-01-01", False, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()

    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200, f"Non premium user should be able to watch non premium movie, got status code:{response.status_code}"

@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_user_with_ppv_access_watches_premium_movie(cursor, conn, create_token):
    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
    movie_id = create_movie("2000-01-01", True, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()
    result = grant_ppv_access(user_id, movie_id, cursor = cursor)
    conn.commit()

    assert result[0] is True, "PPV grant failed in setup"

    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200, f"User with ppv access should be able to watch premium movie, got status code:{response.status_code}"

@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_non_existing_movie(cursor, conn, create_token):
    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=True, cursor=cursor)
    conn.commit()


    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/99999999/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 404, f"Movie should not exists, got status code:{response.status_code}"
    
@allure.feature("API Movies")
@allure.story("Access Control")
def test_api_user_without_token_watches_movie(cursor, conn):
    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=True, cursor=cursor)
    movie_id = create_movie("2000-01-01", True, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()


    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch")
    
    assert response.status_code == 401, f"User should not be able to watch movie without authorization, got status code:{response.status_code}"

    