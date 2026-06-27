-- ============================================================
-- Digital Nurture 5.0 | Database Integration | Hands-On 2
-- Writing SQL Queries — DML, Joins & Aggregations
-- Author: Madhumitha R
-- Prerequisite: hands_on_1.sql must have been run first
-- ============================================================

USE college_db;

-- ============================================================
-- TASK 1: INSERT, UPDATE, DELETE (Steps 15–19)
--
-- WHY: Every API endpoint that writes data — POST, PUT, DELETE —
-- translates directly to one of these three SQL operations.
-- Knowing raw DML means you understand what your ORM is doing
-- and can debug it when it goes wrong.
-- ============================================================

-- Step 15: Sample data already inserted in hands_on_1.sql
-- Verify current counts before we begin
SELECT 'students before' AS label, COUNT(*) AS count FROM students
UNION ALL
SELECT 'enrollments before', COUNT(*) FROM enrollments;


-- Step 16: Insert two additional students
-- WHY: Real apps continuously add rows — this tests FK integrity
-- (department_id 1 = Computer Science must already exist)
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES
    ('Ananya',   'Krishnan', 'ananya.krishnan@college.edu', '2004-06-15', 1, 2023),
    ('Siddharth','Nair',     'siddharth.nair@college.edu',  '2003-12-20', 2, 2022);

-- Verify: should now show 10 students
SELECT COUNT(*) AS total_students FROM students;


-- Step 17: Update grade for student_id=5, course_id=1 from 'C' to 'B'
-- WHY: UPDATE without a WHERE clause updates EVERY row — one of the
-- most dangerous mistakes in SQL. Always filter to the exact row first.
-- Best practice: run a SELECT with the same WHERE before updating.
SELECT * FROM enrollments WHERE student_id = 5 AND course_id = 1;  -- preview first

UPDATE enrollments
SET    grade = 'B'
WHERE  student_id = 5
AND    course_id  = 1;

-- Verify the change
SELECT * FROM enrollments WHERE student_id = 5 AND course_id = 1;


-- Step 18: Delete enrollments where grade IS NULL
-- WHY: NULL means "no grade assigned" — these represent students
-- who registered but never completed. IS NULL is the correct
-- SQL operator — grade = NULL will NEVER match anything in SQL
-- because NULL is not equal to anything, including itself.
SELECT * FROM enrollments WHERE grade IS NULL;  -- preview before deleting

DELETE FROM enrollments
WHERE grade IS NULL;

-- Verify: all remaining rows should have a grade value
SELECT COUNT(*) AS enrollments_after_delete FROM enrollments;
SELECT * FROM enrollments ORDER BY enrollment_id;


-- ============================================================
-- TASK 2: SINGLE-TABLE QUERIES (Steps 20–24)
--
-- WHY: These are the building blocks. Every complex query you
-- will ever write is a combination of these fundamentals.
-- Master WHERE, ORDER BY, LIKE, and GROUP BY cold — you'll
-- use them every single day as a backend developer.
-- ============================================================

-- Step 20: All students enrolled in 2022, ordered by last_name
-- WHY: WHERE filters rows, ORDER BY sorts them. The sort happens
-- AFTER filtering — the database doesn't sort rows it's going
-- to discard anyway.
SELECT
    student_id,
    first_name,
    last_name,
    email,
    enrollment_year
FROM   students
WHERE  enrollment_year = 2022
ORDER BY last_name ASC;


-- Step 21: Courses with more than 3 credits, sorted descending
-- WHY: > is strict — courses with exactly 3 credits are excluded.
-- If the task said "3 or more", you'd use >= instead.
SELECT
    course_name,
    course_code,
    credits
FROM   courses
WHERE  credits > 3
ORDER BY credits DESC;


-- Step 22: Professors with salary BETWEEN 80,000 and 95,000
-- WHY: BETWEEN is INCLUSIVE on both ends.
-- BETWEEN 80000 AND 95000 is identical to:
-- WHERE salary >= 80000 AND salary <= 95000
SELECT
    prof_name,
    email,
    salary
FROM   professors
WHERE  salary BETWEEN 80000 AND 95000
ORDER BY salary DESC;


-- Step 23: Students whose email ends with '@college.edu'
-- WHY: LIKE with % wildcard matches any prefix.
-- % = zero or more of any character.
-- _ = exactly one character (different wildcard, less commonly used).
-- This pattern is how you'd search for all users on a given domain.
SELECT
    first_name,
    last_name,
    email
FROM   students
WHERE  email LIKE '%@college.edu'
ORDER BY last_name;


-- Step 24: Count students per enrollment_year
-- WHY: GROUP BY splits the result into buckets — one bucket per
-- distinct value of enrollment_year — then COUNT(*) counts rows
-- in each bucket. This is the foundation of every summary report
-- your Django API will ever generate.
SELECT
    enrollment_year,
    COUNT(*) AS student_count
FROM   students
GROUP BY enrollment_year
ORDER BY enrollment_year;
-- Expected: 3 rows — 2021, 2022, 2023


-- ============================================================
-- TASK 3: MULTI-TABLE JOINS (Steps 25–29)
--
-- WHY: Real data lives across multiple tables. A JOIN combines
-- rows from two or more tables based on a related column.
-- INNER JOIN = only matching rows on both sides.
-- LEFT JOIN  = ALL rows from the left table, matched rows from
--              the right (unmatched right side becomes NULL).
-- This is exactly what Django ORM does when you call
-- student.department or course_set.all()
-- ============================================================

-- Step 25: Student full name + department name (2-table INNER JOIN)
-- WHY: student.department_id is a FK — to get the actual
-- department name, you must JOIN to the departments table.
-- This is the most common join pattern in any web application.
SELECT
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name                             AS department
FROM   students s
INNER JOIN departments d ON s.department_id = d.department_id
ORDER BY d.dept_name, s.last_name;


-- Step 26: Each enrollment with student name + course name (3-table JOIN)
-- WHY: enrollments is a junction/bridge table — it links students
-- to courses. To get human-readable names instead of IDs,
-- you JOIN to both sides. This is the pattern behind every
-- "show me what courses this student is taking" API endpoint.
SELECT
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.course_name,
    e.enrollment_date,
    e.grade
FROM   enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses  c ON e.course_id  = c.course_id
ORDER BY s.last_name, c.course_name;


-- Step 27: Students NOT enrolled in any course (LEFT JOIN + IS NULL)
-- WHY: This is the "find missing relationships" pattern.
-- LEFT JOIN keeps ALL students, even those with no enrollment rows.
-- WHERE e.enrollment_id IS NULL filters to ONLY those with no match.
-- This cannot be done with INNER JOIN — INNER JOIN would just
-- exclude unenrolled students silently, with no indication they exist.
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    s.email
FROM   students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE  e.enrollment_id IS NULL;
-- Ananya and Siddharth (our new inserts) should appear here


-- Step 28: Every course + number of enrolled students
-- (courses with zero enrollments must still appear)
-- WHY: INNER JOIN would hide courses with no students.
-- LEFT JOIN + COUNT keeps them visible with a count of 0.
-- This is how you build a course catalog page that shows
-- "0 students enrolled" rather than silently hiding the course.
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS enrolled_students
FROM   courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code
ORDER BY enrolled_students DESC;
-- Expected: all 5 courses appear, even those with 0 enrollments


-- Step 29: Each department + professors + salaries
-- (departments with no professors still appear)
SELECT
    d.dept_name,
    p.prof_name,
    p.salary
FROM   departments d
LEFT JOIN professors p ON d.department_id = p.department_id
ORDER BY d.dept_name, p.salary DESC;


-- ============================================================
-- TASK 4: AGGREGATIONS & GROUPING (Steps 30–34)
--
-- WHY: Aggregations are the engine behind every dashboard,
-- report, and analytics endpoint. COUNT, AVG, SUM, MAX are
-- how raw rows become meaningful numbers.
-- HAVING vs WHERE: WHERE filters individual rows BEFORE grouping.
-- HAVING filters groups AFTER aggregation. You CANNOT use
-- aggregate functions inside a WHERE clause — that's what
-- HAVING is for.
-- ============================================================

-- Step 30: Total enrollments per course
SELECT
    c.course_name,
    COUNT(e.enrollment_id) AS enrollment_count
FROM   courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
ORDER BY enrollment_count DESC;


-- Step 31: Average professor salary per department (rounded to 2dp)
-- WHY: ROUND(AVG(salary), 2) — AVG ignores NULLs automatically.
-- If a department has no professors, AVG returns NULL (not 0).
SELECT
    d.dept_name,
    ROUND(AVG(p.salary), 2) AS avg_salary
FROM   departments d
LEFT JOIN professors p ON d.department_id = p.department_id
GROUP BY d.department_id, d.dept_name
ORDER BY avg_salary DESC;
-- Expected: 4 rows, one per department


-- Step 32: Departments where total budget exceeds 600,000
-- WHY: budget is on the departments table itself — no JOIN needed.
-- WHERE works here because we're filtering individual rows,
-- not filtering on an aggregated result.
SELECT
    dept_name,
    budget
FROM   departments
WHERE  budget > 600000
ORDER BY budget DESC;


-- Step 33: Grade distribution for course CS101
-- WHY: This is a frequency analysis — how many students got
-- each grade. COUNT(*) grouped by grade produces the
-- distribution. NULL grades were deleted in Task 1,
-- so only real grades appear.
SELECT
    e.grade,
    COUNT(*) AS student_count
FROM   enrollments e
INNER JOIN courses c ON e.course_id = c.course_id
WHERE  c.course_code = 'CS101'
GROUP BY e.grade
ORDER BY e.grade;


-- Step 34: Departments where MORE THAN 2 students are enrolled
-- across all courses in that department
-- WHY: HAVING filters on COUNT(*) — a group-level condition.
-- This is impossible with WHERE because WHERE runs before
-- grouping happens and can't see the COUNT result yet.
SELECT
    d.dept_name,
    COUNT(DISTINCT e.student_id) AS enrolled_students
FROM   departments d
INNER JOIN courses    c ON d.department_id = c.department_id
INNER JOIN enrollments e ON c.course_id    = e.course_id
GROUP BY d.department_id, d.dept_name
HAVING COUNT(DISTINCT e.student_id) > 2
ORDER BY enrolled_students DESC;
