-- All of the queries requested by The Movies DB

SELECT title, ARRAY_AGG(genre)
FROM movies
JOIN genre_assignment USING(movie_id)
JOIN genres USING(genre_id)
GROUP BY title
LIMIT 10;

SELECT country, COUNT(title)
FROM countries
JOIN movies USING(country_id)
GROUP BY country
LIMIT 10;

SELECT title, language
FROM movies
JOIN languages USING(language_id)
LIMIT 10;

SELECT title, budget
FROM movies
WHERE budget > 50000000
LIMIT 10;

SELECT status, AVG(score)
FROM movies
GROUP BY status
LIMIT 10;

SELECT title, actor, role
FROM crew_assignment
JOIN actors USING(actor_id)
JOIN roles USING(role_id)
JOIN movies USING (movie_id)
WHERE movie_id = 100
LIMIT 10;

SELECT country, MAX(budget)
FROM movies
JOIN countries USING(country_id)
GROUP BY country
LIMIT 10;

SELECT genre, AVG(score)
FROM movies
JOIN genre_assignment USING(movie_id)
JOIN genres USING(genre_id)
GROUP BY genre
HAVING COUNT(title) > 5
LIMIT 10;

SELECT actor
FROM crew_assignment
JOIN actors USING(actor_id)
GROUP BY actor
HAVING COUNT(movie_id) > 3
LIMIT 10;

SELECT title
FROM movies
WHERE release_date >= CURRENT_DATE - INTERVAL '3' YEAR AND score > 8
LIMIT 10;

SELECT language, COUNT(title), SUM(revenue)
FROM movies
JOIN languages USING(language_id)
GROUP BY language
LIMIT 10;

SELECT g.genre, c.country, COUNT (*) AS movie_count
FROM genres g
JOIN genre_assignment ga USING(genre_id)
JOIN movies m USING(movie_id)
JOIN countries c USING(country_id)
WHERE (c.country, g.genre) IN (
    SELECT c2.country, g2.genre
    FROM genres g2
    JOIN genre_assignment ga2 USING(genre_id)
    JOIN movies m2 USING(movie_id)
    JOIN countries c2 USING(country_id)
    GROUP BY g2.genre, c2.country
    ORDER BY COUNT(*) DESC
    FETCH FIRST 10 ROW WITH TIES
)
GROUP BY g.genre, c.country
ORDER BY g.genre, COUNT(*) DESC;
