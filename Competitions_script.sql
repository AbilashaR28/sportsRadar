SHOW databases;
CREATE DATABASE sportsradar;
SELECT * FROM sportsradar;
-- List all competitions along with their category name
SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id;
-- Count the number of competitions in each category
SELECT
    cat.category_name,
    COUNT(c.competition_id) AS competition_count
FROM categories cat
LEFT JOIN competitions c ON cat.category_id = c.category_id
GROUP BY cat.category_id, cat.category_name;
-- Find all competitions of type 'doubles'
SELECT
    competition_id,
    competition_name,
    type,
    gender
FROM competitions
WHERE type = 'doubles';
-- Get competitions that belong to a specific category (e.g., ITF Men)
SELECT
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';
-- Identify parent competitions and their sub-competitions
SELECT
    parent.competition_name AS parent_name,
    child.competition_name AS sub_competition_name
FROM competitions child
JOIN competitions parent ON child.parent_id = parent.competition_id;
-- Analyze the distribution of competition types by category
SELECT
    cat.category_name,
    c.type,
    COUNT(*) AS type_count
FROM competitions c
JOIN categories cat ON c.category_id = cat.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, type_count DESC;
-- List all competitions with no parent (top-level competitions)
SELECT
    competition_id,
    competition_name,
    type,
    gender
FROM competitions
WHERE parent_id IS NULL;

