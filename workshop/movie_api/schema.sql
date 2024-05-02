-- This file contains all of the SQL commands to create the database, tables and relationships for the Movies Database

DROP TABLE IF EXISTS genre_assignment, genres, crew_assignment, roles, actors, movies, countries, languages;


CREATE TABLE languages (
    language_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    language VARCHAR UNIQUE NOT NULL
);

CREATE TABLE countries (
    country_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country CHAR(2) UNIQUE NOT NULL
);

CREATE TABLE movies (
    movie_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR UNIQUE NOT NULL,
    release_date DATE NOT NULL,
    score FLOAT NOT NULL,
    overview VARCHAR NOT NULL,
    orig_title VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    language_id INT NOT NULL,
    budget FLOAT NOT NULL,
    revenue FLOAT NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (language_id) REFERENCES languages ON DELETE SET NULL,
    FOREIGN KEY (country_id) REFERENCES countries ON DELETE SET NULL
);

CREATE TABLE actors (
    actor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    actor VARCHAR UNIQUE NOT NULL
);

CREATE TABLE roles (
    role_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role VARCHAR UNIQUE NOT NULL
);

CREATE TABLE crew_assignment (
    crew_assignment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors ON DELETE SET NULL,
    FOREIGN KEY (role_id) REFERENCES roles ON DELETE SET NULL
);

CREATE TABLE genres (
    genre_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    genre VARCHAR UNIQUE NOT NULL
);

CREATE TABLE genre_assignment (
    genre_assignment_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres ON DELETE SET NULL
);