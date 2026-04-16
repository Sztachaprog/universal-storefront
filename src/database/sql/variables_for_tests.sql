WITH movie_id AS(
INSERT INTO movies (release_date, is_premium_only) VALUES
('2000-01-01', True) RETURNING id)
INSERT INTO movie_translations (movie_id, language_code, title, description)
SELECT id, 'pl', 'film', 'to jest polski film' FROM movie_id;

WITH movie_id AS(
INSERT INTO movies (release_date, is_premium_only) VALUES
('2000-01-01', False) RETURNING id)
INSERT INTO movie_translations (movie_id, language_code, title, description)
SELECT id, 'eg', 'film', 'This is english film' FROM movie_id;



