from src.application import (
    register_user
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

