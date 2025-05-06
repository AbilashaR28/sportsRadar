-- 1. List all venues along with their associated complex name
SELECT v.venue_name, c.complex_name
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id;

-- 2. Count the number of venues in each complex
SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM complexes c
LEFT JOIN venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_id;

-- 3. Get details of venues in a specific country (e.g., Chile)
SELECT *
FROM venues
WHERE country = 'Chile';

-- 4. Identify all venues and their timezones
SELECT venue_name, timezone
FROM venues;

-- 5. Find complexes that have more than one venue
SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
FROM complexes c
JOIN venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_id
HAVING COUNT(v.venue_id) > 1;

-- 6. List venues grouped by country
SELECT country, GROUP_CONCAT(venue_name SEPARATOR ', ') AS venues
FROM venues
GROUP BY country;

-- 7. Find all venues for a specific complex (e.g., Nacional)
SELECT v.*
FROM venues v
JOIN complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name = 'Nacional';

-- 8. Analyze the distribution of competition types by category
SELECT c.category_id, cat.category_name, c.type, COUNT(*) AS count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY c.category_id, c.type;

-- 9. List all competitions with no parent (top-level competitions)
SELECT *
FROM competitions
WHERE parent_id IS NULL;
