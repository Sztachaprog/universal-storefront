from src.application import (
    register_user,
    get_user_by_id
)
import requests

def test_api_get_user(cursor, conn):

   register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
   conn.commit()
   response = requests.get("http://localhost:5000/api/users/1")
   data = response.json()

   assert response.status_code == 200, "User should exist"
   assert data["username"] == "username1", f"Username should be 'username1', got {data["username"]}"


def test_api_get_non_exist_user():

   response = requests.get("http://localhost:5000/api/users/1")

   assert response.status_code == 404, "User should not be found"


def test_api_post_user(cursor, conn):

   response = requests.post("http://localhost:5000/api/users", json={
       "username": "username1",
       "password": "password1",
       "email": "bartek@example.com",
       "is_premium": False
   })
   conn.commit()
   user = get_user_by_id(1, cursor=cursor)

   assert user is not None, "User should be added to database"
   assert response.status_code == 201, "User should be added to database"

def test_api_post_duplicate_username(cursor, conn):

   register_user("username1", "password1", "bartek@example.com", is_premium=False, cursor=cursor)
   conn.commit()

   duplicateResponse = requests.post("http://localhost:5000/api/users", json={
   "username": "username1",
   "password": "password123",
   "email": "test@example.com",
   "is_premium": False
   })
   conn.commit()

   assert duplicateResponse.status_code == 409, f"Respone should be 409 'Conflict', got {duplicateResponse.status_code}"

def test_api_post_without_email():

   response = requests.post("http://localhost:5000/api/users", json={
   "username": "username1",
   "password": "password123",
   "email": "",
   "is_premium": False
   })

   data = response.json()

   assert response.status_code == 400, f"Respone should be 400 'Bad Request', got {response.status_code}"

def test_api_post_too_short_password():   
   
   response = requests.post("http://localhost:5000/api/users", json={
   "username": "username1",
   "password": "123",
   "email": "test@example.com",
   "is_premium": False
   })

   assert response.status_code == 400, f"Response should be 400 'Bad Request', got {response.status_code}"