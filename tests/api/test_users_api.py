from src.application import (
    register_user,
    get_user_by_name
)
import requests
import allure
import jwt
from datetime import datetime, timezone, timedelta
from tests.api.conftest import BASE_URL

@allure.feature("API Users")
@allure.story("GET User")
def test_api_get_user(cursor, conn):

   user_id = register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
   conn.commit()
   login = requests.post(f"{BASE_URL}/login", json={
                        "username": "username1",
                        "password": "password1"
   })
   token = login.json()["token"]
   response = requests.get(
<<<<<<< HEAD
   f"{BASE_URL}/users/{user_id}",
=======
   f"http://localhost:5000/api/users/{user_id}",
>>>>>>> d557a03c8ed096459ff8659dae74cedbfb51ed02
   headers={"Authorization": f"Bearer {token}"}
   )
   data = response.json()

   assert response.status_code == 200, f"User should exist, got status code: {response.status_code}"
   assert data["username"] == "username1", f"Username should be 'username1', got {data["username"]}"


@allure.feature("API Users")
@allure.story("GET User")
def test_api_get_non_exist_user():

   token = jwt.encode(
      {"user_id": 1, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
      "dev-secret-key",
      algorithm="HS256")
   response = requests.get(f"{BASE_URL}/users/1",
                           headers={"Authorization": f"Bearer {token}"}
   )

   assert response.status_code == 404, f"User should not be found, got status code: {response.status_code}"

@allure.feature("API Users")
@allure.story("POST User")
def test_api_post_user(cursor, conn):

   response = requests.post(f"{BASE_URL}/users", json={
       "username": "username1",
       "password": "password1",
       "email": "bartek@example.com"
   })
   conn.commit()
   user = get_user_by_name("username1", cursor=cursor)

   assert user is not None, "User should be added to database"
   assert response.status_code == 201, f"User should be added to database, got status code: {response.status_code}"

@allure.feature("API Users")
@allure.story("POST User")
def test_api_post_duplicate_username(cursor, conn):

   register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
   conn.commit()

   duplicateResponse = requests.post(f"{BASE_URL}/users", json={
   "username": "username1",
   "password": "password123",
   "email": "test@example.com"
   })
   conn.commit()

   assert duplicateResponse.status_code == 409, f"Respone should be 409 'Conflict', got status code {duplicateResponse.status_code}"

@allure.feature("API Users")
@allure.story("POST User")
def test_api_post_without_email():

   response = requests.post(f"{BASE_URL}/users", json={
   "username": "username1",
   "password": "password123",
   "email": ""
   })

   data = response.json()

   assert response.status_code == 400, f"Respone should be 400 'Bad Request', got status code: {response.status_code}"

@allure.feature("API Users")
@allure.story("POST User")
def test_api_post_too_short_password():   
   
   response = requests.post(f"{BASE_URL}/users", json={
   "username": "username1",
   "password": "123",
   "email": "test@example.com"
   })

   assert response.status_code == 400, f"Response should be 400 'Bad Request', got status code: {response.status_code}"

@allure.feature("API Users")
@allure.story("Authentication")
def test_api_token_expired(conn, cursor):

      user_id = register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
      conn.commit()
      expired_token = jwt.encode(
      {"user_id": 1, "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
      "dev-secret-key",
      algorithm="HS256"
   )
<<<<<<< HEAD
      response = requests.get(f"{BASE_URL}/users/{user_id}",
=======
      response = requests.get(f"http://localhost:5000/api/users/{user_id}",
>>>>>>> d557a03c8ed096459ff8659dae74cedbfb51ed02
                              headers={"Authorization": f"Bearer {expired_token}"}
   )
      
      assert response.status_code == 401, f"Session should be expired, got status code: {response.status_code}"
      assert response.json()["error"] == "Token expired"

@allure.feature("API Users")
@allure.story("Authentication")
def test_api_token_invalid():

   invalid_token = jwt.encode(
      {"user_id": 1, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
      "wrong-key",
      algorithm="HS256"
   )

   response = requests.get(f"{BASE_URL}/users/1",
   headers={"Authorization": f"Bearer {invalid_token}"
   })


   assert response.status_code == 401, f"Token should be invalid '401', got status code: {response.status_code}"
   assert response.json()["error"] == "Invalid token"

@allure.feature("API Users")
@allure.story("Authentication")
def test_api_token_missing():

   response = requests.get(f"{BASE_URL}/users/1")

   assert response.status_code == 401, f"Token should be missing '401', got status code: {response.status_code} "
   assert response.json()["error"] == "Token is missing"
