-- Get all competitors with their rank and points.
SELECT c.competitor_id, c.name, r.rank, r.points
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id;
-- Find competitors ranked in the top 5
SELECT c.competitor_id, c.name, r.rank, r.points
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
WHERE r.rank <= 5
ORDER BY r.rank ASC;
-- List competitors with no rank movement (stable rank)
SELECT c.competitor_id, c.name, r.rank
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
WHERE r.movement = 0;
-- Get the total points of competitors from a specific country (e.g., Croatia)
SELECT c.country, SUM(r.points) AS total_points
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;
-- Count the number of competitors per country
SELECT country, COUNT(*) AS competitor_count
FROM Competitors
GROUP BY country
ORDER BY competitor_count DESC;
-- Find competitors with the highest points in the current week
SELECT c.competitor_id, c.name, r.points
FROM Competitors c
JOIN Rankings r ON c.competitor_id = r.competitor_id
WHERE r.points = (SELECT MAX(points) FROM Rankings);

