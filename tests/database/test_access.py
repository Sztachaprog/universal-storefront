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
    non_premium_user_id = register_user("user", "password123", "mail@mail.com", is_premium=False, cursor=cursor)

    # Create a test user with premium access
    premium_user_id = register_user("user2", "password123", "mail2@mail.com", is_premium=True, cursor=cursor)
    

    # Create a test movie that is premium only
    movie_id = create_movie("2023-01-01", True, "en", "Premium Movie", "A premium movie description", cursor=cursor)

    # Grant PPV access to the user for the premium movie
    user_granted = grant_ppv_access(non_premium_user_id, movie_id, cursor=cursor)
    user_premium_granted = grant_ppv_access(premium_user_id, movie_id, cursor=cursor)

    # Grant PPV access to the user for the premium movie
    assert user_granted[0] == True, "PPV access should be granted to the user"
    assert user_premium_granted[0] == False, "PPV access should not be granted to the premium user who already has access"
def test_process_watch_request(cursor):
    # Create a test user with non-premium access
    non_premium_user_id = register_user("user", "password123", "mail@mail.com", is_premium=False, cursor=cursor)

    
    # Create a test user with premium access
    premium_user_id = register_user("user2", "password123", "mail2@mail.com", is_premium=True, cursor=cursor)

    # Create a test movie that is premium only
    movie_id = create_movie("2023-01-01", True, "en", "Premium Movie", "A premium movie description", cursor=cursor)

    assert process_watch_request(non_premium_user_id, movie_id, cursor = cursor) == False, "Non premium user should not have access to premium movies"

    # Grant PPV access to the non-premium user for the premium movie
    user_granted_ppv_access = grant_ppv_access(non_premium_user_id, movie_id, cursor=cursor)
    

    assert process_watch_request(premium_user_id, movie_id, cursor = cursor) == True, "Premium user should have access to premium movie"
    assert process_watch_request(non_premium_user_id, movie_id, cursor = cursor) == True, "User with ppv access should have access to premium movie"

    
