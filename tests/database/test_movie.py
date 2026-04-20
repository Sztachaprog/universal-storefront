from src.application import (
    create_movie,
    get_movie_details,
    update_movie,
    delete_movie
)

# Create
def test_create_movie(cursor):
    movie_id = create_movie("2024-01-01", True, "pl", "Polski film", "Opis polskiego filmu", cursor = cursor)
    assert movie_id is not None, "Failed to create movie"

    movie_details = get_movie_details(movie_id, "pl", cursor = cursor)
    assert movie_details is not None, "Movie not found in database"

    assert str(movie_details[1]) == "2024-01-01", f"Expected release date '2024-01-01', got '{movie_details[1]}'"
    assert movie_details[2] == True, f"Expected is_premium_only True, got {movie_details[2]}"
    assert movie_details[3] == "Polski film", f"Expected title 'Polski film', got '{movie_details[3]}'"
    assert movie_details[4] == "Opis polskiego filmu", f"Expected description 'Opis polskiego filmu', got '{movie_details[4]}'"

# Read
def test_get_movie(cursor):
    movie_id = create_movie("2024-01-01", True, "pl", "Polski film", "Opis polskiego filmu", cursor = cursor)
    movie_details = get_movie_details(movie_id, "pl", cursor = cursor)

    assert movie_details is not None, "Movie not found in database"
    assert str(movie_details[1]) == "2024-01-01", f"Expected release date '2024-01-01', got '{movie_details[1]}'"
    assert movie_details[2] == True, f"Expected is_premium_only True, got {movie_details[2]}"
    assert movie_details[3] == "Polski film", f"Expected title 'Polski film', got '{movie_details[3]}'"
    assert movie_details[4] == "Opis polskiego filmu", f"Expected description 'Opis polskiego filmu', got '{movie_details[4]}'"
# Update
def test_update_movie(cursor):
    movie_id = create_movie("2024-01-01", True, "pl", "Polski film", "Opis polskiego filmu", cursor = cursor)
    updated_movies = update_movie("2025-01-01", False, "en", "English Movie", "Description of English movie", movie_id, cursor = cursor)
    get_updated_movies = get_movie_details(updated_movies, "en", cursor = cursor)

    assert get_updated_movies is not None, "Movie not found in database"
    assert str(get_updated_movies[1]) == "2025-01-01", f"Expected release date '2025-01-01', got '{get_updated_movies[1]}'"
    assert get_updated_movies[2] == False, f"Expected is_premium_only False, got {get_updated_movies[2]}"
    assert get_updated_movies[3] == "English Movie", f"Expected title 'English Movie', got '{get_updated_movies[3]}'"
    assert get_updated_movies[4] == "Description of English movie", f"Expected description 'Description of English movie', got '{get_updated_movies[4]}'"
# Delete
def test_delete_movie(cursor):
    movie_id = create_movie("2024-01-01", True, "pl", "Polski film", "Opis polskiego filmu", cursor = cursor)
    delete_movie(movie_id, cursor = cursor)
    movie_details = get_movie_details(movie_id, "pl", cursor = cursor)

    assert movie_details is None, "Movie was not deleted from database"