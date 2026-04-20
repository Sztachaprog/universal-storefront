from src.application import (
    create_movie,
    register_user,
    process_watch_request,
    grant_ppv_access
)

# def test_user_access_to_movie():
#     # Create a test user with non-premium access
#     non_premium_user_id = register_user("user", "password123", "mail@mail.com")

#     # Create a test user with premium access
#     premium_user_id = register_user("user2", "password123", "mail2@mail.com", is_premium=True)

#     # Create a test movie that is premium only
#     premium_movie_id = create_movie("2023-01-01", True, "en", "Premium Movie", "A premium movie description")

#     # Create a test movie that is not premium only
#     non_premium_movie_id = create_movie("2023-01-01", False, "en", "Non-Premium Movie", "A non-premium movie description")

#     assert process_watch_request(non_premium_user_id, premium_movie_id) == False, "Non-premium user should not have access to premium movie"
#     assert process_watch_request(non_premium_user_id, non_premium_movie_id) == True, "Non-premium user should have access to non-premium movie"
#     assert process_watch_request(premium_user_id, premium_movie_id) == True, "Premium user should have access to premium movie"
#     assert process_watch_request(premium_user_id, non_premium_movie_id) == True, "Premium user should have access to non-premium movie"

def test_grant_ppv_access(cursor):
    # Create a test user with non-premium access
    register_user("user3", "password123", "mail3@mail.com", is_premium=True)
    cursor.execute("SELECT id, is_premium FROM users WHERE username = 'user3';")
    is_user_premium = cursor.fetchone()[1]
    # Create a test movie that is premium only
    create_movie("2023-01-01", True, "en", "Premium Movie", "A premium movie description")
    cursor.execute("SELECT id, is_premium_only FROM movies;")
    is_film_premium = cursor.fetchone()[1]

    # Grant PPV access to the user for the premium movie
    assert grant_ppv_access(is_user_premium, is_film_premium) == True, "PPV access should be granted to the user"