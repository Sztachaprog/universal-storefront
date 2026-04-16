    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        is_premium BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        release_date DATE,
        is_premium_only BOOLEAN DEFAULT FALSE
    );
    CREATE TABLE IF NOT EXISTS movie_translations ( -- Creating two tables for a movies to translations relationship
        id SERIAL PRIMARY KEY,
        movie_id INTEGER NOT NULL,
        language_code VARCHAR(2) NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        UNIQUE (movie_id, language_code)
    );
    CREATE TABLE IF NOT EXISTS user_access (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
        expires_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW() + INTERVAL '30 days',
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
        UNIQUE (user_id, movie_id)
    );  


