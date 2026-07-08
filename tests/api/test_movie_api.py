from src.application import (
    create_movie,
    register_user
)

import requests
import jwt
import allure
from datetime import datetime, timezone, timedelta
from tests.api.conftest import BASE_URL


def test_api_premium_user_watches_premium_movie(cursor, conn, create_token):

    user_id = register_user("username1", "password1", "bartek@example.com", is_premium=True, cursor=cursor)
    movie_id = create_movie("2000-01-01", True, "pl", "Movie", "movie description", cursor = cursor)
    conn.commit()

    token = create_token(user_id)

    response = requests.get(f"{BASE_URL}/movies/{movie_id}/watch",
                            headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200, f"User Should be able to watch movie, got status code:{response.status_code}"
    