from src.application import (
    create_movie,
    get_movie_details
)

# Create
def test_create_movie():
    movie_id = create_movie("2024-01-01", True, "pl", "Polski film", "Opis polskiego filmu")
    assert movie_id is not None, "Failed to create movie"

    movie_details = get_movie_details(movie_id, "pl")
    assert movie_details is not None, "Movie not found in database"

    assert str(movie_details[1]) == "2024-01-01", f"Expected release date '2024-01-01', got '{movie_details[1]}'"
    assert movie_details[2] == True, f"Expected is_premium_only True, got {movie_details[2]}"
    assert movie_details[3] == "Polski film", f"Expected title 'Polski film', got '{movie_details[3]}'"
    assert movie_details[4] == "Opis polskiego filmu", f"Expected description 'Opis polskiego filmu', got '{movie_details[4]}'"

# Update
def test_get_movie():
    