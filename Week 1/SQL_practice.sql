SELECT * FROM netflix_titles;
-- LEVEL 1 - SELECT & WHERE
SELECT title, release_year FROM netflix_titles;
SELECT * FROM netflix_titles WHERE type = "Movie";
SELECT * FROM netflix_titles WHERE release_year > 2018;
SELECT * FROM netflix_titles WHERE rating = "PG-13";
SELECT * FROM netflix_titles
WHERE type = "Movie" AND release_year < 2000;
SELECT * FROM netflix_titles
WHERE country LIKE "%Japan%";
SELECT * FROM netflix_titles
WHERE title LIKE "%Love%";
SELECT * FROM netflix_titles
WHERE director IS NULL;
-- LEVEL 2 - ORDER BY & LIMIT
SELECT * FROM netflix_titles
ORDER BY release_year DESC
LIMIT 10;
SELECT * FROM netflix_titles
ORDER BY release_year LIMIT 20;
SELECT * FROM netflix_titles
ORDER BY date_added DESC LIMIT 5;
-- LEVEL 3 - AGGREGATE FUNCTIONS
SELECT COUNT(*) FROM netflix_titles;
SELECT COUNT(*) FROM netflix_titles
WHERE type = "Movie";
SELECT MIN(release_year) FROM netflix_titles;
SELECT COUNT(DISTINCT rating) FROM netflix_titles;
-- LEVEL 4 - GROUP BY
SELECT rating, COUNT(*) FROM netflix_titles
GROUP BY rating ORDER BY COUNT(*) DESC;
WITH RECURSIVE split_country AS (
    -- Anchor
    SELECT
        title,
        TRIM(SUBSTRING_INDEX(country, ',', 1)) AS current_country,
        TRIM(
            SUBSTRING(
                country,
                LENGTH(SUBSTRING_INDEX(country, ',', 1)) + 2
            )
        ) AS remaining
    FROM netflix_titles
    WHERE country IS NOT NULL

    UNION ALL

    -- Recursive
    SELECT
        title,
        TRIM(SUBSTRING_INDEX(remaining, ',', 1)),
        TRIM(
            SUBSTRING(
                remaining,
                LENGTH(SUBSTRING_INDEX(remaining, ',', 1)) + 2
            )
        )
    FROM split_country
    WHERE remaining <> ''
)
SELECT
    current_country,
    COUNT(*) AS total_titles
FROM split_country
GROUP BY current_country
ORDER BY total_titles DESC;
SELECT director, COUNT(director) FROM netflix_titles 
GROUP BY director ORDER BY COUNT(director) DESC
LIMIT 5;
SELECT release_year, COUNT(release_year) FROM netflix_titles
GROUP BY release_year ORDER BY release_year;
-- LEVEL 5 - HAVING
SELECT rating, COUNT(rating)
FROM netflix_titles GROUP BY rating
HAVING COUNT(rating) > 100;
SELECT director, COUNT(director)
FROM netflix_titles GROUP BY director
HAVING COUNT(director) > 3;
SELECT release_year, COUNT(release_year)
FROM netflix_titles GROUP BY release_year
HAVING COUNT(release_year) > 50;
-- LEVEL 6 - STRING FUNCTIONS
SELECT * FROM netflix_titles
WHERE title LIKE "The %";
SELECT * FROM netflix_titles
WHERE LENGTH(title) > 20;
SELECT * FROM netflix_titles
WHERE BINARY title = BINARY UPPER(title);
SELECT * FROM netflix_titles
WHERE director LIKE "%Lee";
-- LEVEL 7 - WORKING WITH DATES
SELECT * FROM netflix_titles
WHERE date_added BETWEEN "2021-01-01" AND "2021-12-31";
SELECT
	MONTHNAME(date_added) AS month_name,
	COUNT(*) AS total_tiles
FROM netflix_titles
WHERE date_added IS NOT NULL
GROUP BY month_name
ORDER BY COUNT(*) DESC
LIMIT 1;
-- LEVEL 8 - INTERMEDIATE CHALLENGES
SELECT release_year, COUNT(*)
FROM netflix_titles
GROUP BY release_year
ORDER BY COUNT(*) DESC
LIMIT 1;
SELECT rating, AVG(rating)
FROM netflix_titles
GROUP BY rating
ORDER BY AVG(rating) DESC
LIMIT 1;
SELECT * FROM netflix_titles
WHERE type = "Movie"
ORDER BY release_year
LIMIT 1;
SELECT * FROM netflix_titles
WHERE type = "TV Show"
ORDER BY release_year DESC
LIMIT 1;