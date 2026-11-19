-- Practice queries. Run each one on its own and read the result.

-- 1. All students with the courses they joined
SELECT s.full_name AS student, c.title AS course, e.status
FROM enrollments e
JOIN students s ON s.id = e.student_id
JOIN courses  c ON c.id = e.course_id
ORDER BY s.full_name;

-- 2. Which trainer teaches which course
SELECT c.title AS course, emp.full_name AS trainer
FROM courses c
LEFT JOIN employees emp ON emp.id = c.trainer_id
ORDER BY c.title;

-- 3. How many students are in each course
SELECT c.title AS course, COUNT(e.id) AS total_students
FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.id
GROUP BY c.title
ORDER BY total_students DESC;
