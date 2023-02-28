/* Задача на SQL №1. */

SELECT date_part('year', birthday) AS year,
COUNT(id) as total
FROM users
WHERE birthday is not null
GROUP BY year
ORDER BY year;

/* Задача на SQL №2.*/

SELECT topics.id, users.first_name AS first_name
FROM topics
INNER JOIN users ON users.id = topics.user_id
WHERE users.email LIKE '%@lannister.com'
ORDER BY topics.created_at