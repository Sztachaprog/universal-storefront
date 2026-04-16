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


INSERT INTO users (username, password_hash, email, is_premium)
VALUES 
('Bartek' , 'password_hash', 'bartek@mail.com', TRUE),
('Kacper' , 'password_hash', 'kacper@mail.com', TRUE),
('Michal' , 'password_hash', 'michal@mail.com', False);


SELECT 
    u.username,
    m.id AS movie_id,
    u.is_premium,
    m.is_premium_only,
    ua.expires_at
FROM users u
CROSS JOIN movies m
LEFT JOIN user_access ua 
    ON ua.user_id = u.id 
    AND ua.movie_id = m.id 
    AND ua.expires_at > NOW()
WHERE 
    u.is_premium = TRUE
    OR m.is_premium_only = FALSE
    OR ua.id IS NOT NULL
ORDER BY u.username;


