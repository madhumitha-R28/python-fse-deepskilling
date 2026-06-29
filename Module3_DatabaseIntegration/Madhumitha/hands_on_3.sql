-- ============================================================
-- Digital Nurture 5.0 | Database Integration | Hands-On 3
-- Advanced SQL — Subqueries, Views & Transactions
-- Author: Madhumitha R
-- Prerequisite: hands_on_1.sql + hands_on_2.sql run first
-- ============================================================

USE college_db;

-- ============================================================
-- TASK 1: SUBQUERIES (Steps 35–38)
--
-- WHY: Some questions require two steps — first compute
-- a value, then use it to filter. Subqueries let you nest
-- one SELECT inside another. The key distinction:
--
-- NON-CORRELATED subquery: runs ONCE, produces a single
-- value or table, and the outer query uses it.
-- e.g. WHERE count > (SELECT AVG(...) FROM ...)
--
-- CORRELATED subquery: re-runs for EVERY row of the outer
-- query, referencing the outer row each time.
-- e.g. WHERE salary = (SELECT MAX(salary) FROM professors
--                      WHERE department_id = p.department_id)
-- Use sparingly — can be slow on large tables.
-- ============================================================

-- Step 35: Students enrolled in MORE courses than the average
-- This is a non-correlated subquery — the inner SELECT runs
-- once, calculates the average enrollment count, and the
-- outer query compares each student's count against that value.
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    COUNT(e.enrollment_id)                  AS course_count
FROM   students s
INNER JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.enrollment_id) > (
    -- Non-correlated subquery: runs once
    -- Calculates average enrollments per student across all students
    SELECT AVG(enrollment_count)
    FROM (
        SELECT student_id, COUNT(*) AS enrollment_count
        FROM   enrollments
        GROUP BY student_id
    ) AS per_student_counts
)
ORDER BY course_count DESC;
-- Expected: students enrolled in 3+ courses based on sample data


-- Step 36: Courses where ALL enrolled students received grade 'A'
-- Uses NOT EXISTS — the cleanest way to express "find courses
-- where there is NO student who did NOT get an A."
-- Reading NOT EXISTS: "give me courses where there does not
-- exist any enrollment for this course that has a grade != 'A'"
SELECT
    c.course_id,
    c.course_name,
    c.course_code
FROM   courses c
WHERE  EXISTS (
    -- At least one enrollment exists (course is not empty)
    SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    -- No enrollment exists for this course with a grade other than 'A'
    SELECT 1
    FROM   enrollments e
    WHERE  e.course_id = c.course_id
    AND    (e.grade != 'A' OR e.grade IS NULL)
);


-- Step 37: Professor with the HIGHEST salary in each department
-- Correlated subquery — for each professor row, the inner query
-- re-runs finding the max salary in THAT professor's department.
-- The outer query only keeps professors whose salary matches
-- that max. This is a classic correlated subquery use case.
SELECT
    p.prof_name,
    p.salary,
    d.dept_name
FROM   professors p
INNER JOIN departments d ON p.department_id = d.department_id
WHERE  p.salary = (
    -- Correlated: references p.department_id from outer query
    SELECT MAX(p2.salary)
    FROM   professors p2
    WHERE  p2.department_id = p.department_id
)
ORDER BY p.salary DESC;


-- Step 38: Derived table (subquery in FROM clause) —
-- departments where average professor salary exceeds 85,000
-- WHY: You can't write WHERE AVG(salary) > 85000 directly
-- because WHERE runs before GROUP BY. The solution is to
-- compute the averages first in a subquery (derived table),
-- then filter the result. Derived tables must have an alias.
SELECT
    dept_averages.dept_name,
    dept_averages.avg_salary
FROM (
    -- This derived table runs first, produces one row per dept
    SELECT
        d.dept_name,
        ROUND(AVG(p.salary), 2) AS avg_salary
    FROM   departments d
    INNER JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_averages          -- alias is REQUIRED for derived tables
WHERE dept_averages.avg_salary > 85000
ORDER BY dept_averages.avg_salary DESC;


-- ============================================================
-- TASK 2: VIEWS (Steps 39–43)
--
-- WHY: A VIEW is a saved SELECT query stored in the database
-- with a name. You query it exactly like a table. The value:
-- 1. Simplicity — hide a complex 4-table JOIN behind a name
-- 2. Security — grant access to the view but not the raw tables
-- 3. Consistency — one definition, used everywhere; change the
--    view and all queries that use it get the fix automatically
--
-- Views do NOT store data — they re-run the SELECT every time
-- you query them. For performance-critical cases, use a
-- MATERIALIZED VIEW (PostgreSQL) or a summary table instead.
-- ============================================================

-- Step 39: Create vw_student_enrollment_summary
-- Grade → GPA conversion using CASE WHEN expression:
-- A=4, B=3, C=2, D=1, F=0, NULL=excluded from AVG
DROP VIEW IF EXISTS vw_student_enrollment_summary;

CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name)  AS full_name,
    d.dept_name                              AS department,
    COUNT(e.enrollment_id)                   AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL          -- NULL grades excluded from average
        END
    ), 2)                                    AS gpa
FROM   students s
LEFT  JOIN enrollments  e ON s.student_id  = e.student_id
INNER JOIN departments  d ON s.department_id = d.department_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;


-- Step 40: Create vw_course_stats
DROP VIEW IF EXISTS vw_course_stats;

CREATE VIEW vw_course_stats AS
SELECT
    c.course_id,
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id)  AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2)                   AS avg_gpa
FROM   courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;


-- Step 41: Query the view — students with GPA above 3.0
-- Note: this reads exactly like a table query.
-- Behind the scenes MySQL is running the full JOIN + CASE logic.
SELECT * FROM vw_student_enrollment_summary
WHERE  gpa > 3.0
ORDER BY gpa DESC;


-- Step 42: Attempt UPDATE through the multi-table view
-- Uncomment to test — this WILL fail with an error:
-- Error Code: 1288. The target table vw_student_enrollment_summary
-- of the UPDATE is not updatable
--
-- UPDATE vw_student_enrollment_summary
-- SET    full_name = 'Test Name'
-- WHERE  student_id = 1;
--
-- WHY multi-table views are not updatable:
-- A view that joins multiple tables, uses GROUP BY, or uses
-- aggregate functions cannot be updated because MySQL cannot
-- determine which underlying table row to modify. If you UPDATE
-- full_name through this view, does it update students.first_name,
-- students.last_name, both? And which row? The engine cannot
-- safely resolve this — so it refuses entirely.
-- Single-table views without aggregation ARE updatable.


-- Step 43: DROP views and recreate with WITH CHECK OPTION
-- WITH CHECK OPTION only makes sense on a filtered single-table
-- view — it prevents INSERT/UPDATE of rows that would "disappear"
-- from the view after the operation.
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Recreate vw_course_stats (no check option — multi-table)
CREATE VIEW vw_course_stats AS
SELECT
    c.course_id,
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id)  AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2)                   AS avg_gpa
FROM   courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Single-table view WITH CHECK OPTION — only CS department students
-- WITH CHECK OPTION: if you try to INSERT a student with
-- department_id != 1 through this view, MySQL blocks it
-- because the resulting row would not be visible through the view.
CREATE VIEW vw_cs_students AS
SELECT
    student_id,
    first_name,
    last_name,
    email,
    department_id,
    enrollment_year
FROM   students
WHERE  department_id = 1
WITH CHECK OPTION;

-- Verify both views work
SELECT * FROM vw_course_stats ORDER BY total_enrollments DESC;
SELECT * FROM vw_cs_students  ORDER BY last_name;


-- ============================================================
-- TASK 3: STORED PROCEDURES & TRANSACTIONS (Steps 44–47)
--
-- WHY STORED PROCEDURES:
-- A stored procedure is named, reusable SQL logic stored inside
-- the database itself. Instead of your Python/Django code
-- sending 3 separate SQL statements for an enrollment, it calls
-- sp_enroll_student(1, 2, '2026-07-01') and the database
-- handles the duplicate check and insert atomically.
-- Benefit: business rules enforced at the DB layer, not just
-- the application layer — even if someone queries the DB
-- directly (from MySQL Workbench, a script, another service),
-- the rules still apply.
--
-- WHY TRANSACTIONS:
-- A transaction groups multiple SQL statements into one atomic
-- unit. Either ALL succeed (COMMIT) or ALL are undone (ROLLBACK).
-- Without transactions, a crash or error halfway through a
-- "transfer student" operation leaves the DB in a broken state:
-- the student is removed from dept A but never added to dept B.
-- Transactions prevent that class of problem entirely.
-- ACID properties: Atomicity, Consistency, Isolation, Durability
-- ============================================================

-- Step 44: Stored procedure — enroll a student with duplicate check
-- DELIMITER changes the statement terminator from ; to $$
-- so MySQL doesn't interpret the ; inside the procedure body
-- as "end of the whole CREATE PROCEDURE statement"
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_enroll_student $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id     INT,
    IN p_course_id      INT,
    IN p_enroll_date    DATE
)
BEGIN
    -- Check for duplicate enrollment
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE  student_id = p_student_id
        AND    course_id  = p_course_id
    ) THEN
        -- SIGNAL is MySQL's way of raising a descriptive error
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Duplicate enrollment: student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enroll_date);
        SELECT 'Enrollment successful.' AS result;
    END IF;
END $$

DELIMITER ;

-- Test sp_enroll_student
-- Valid enrollment (Ananya — student_id 9 — into CS101 — course_id 1)
CALL sp_enroll_student(9, 1, '2026-07-01');

-- Duplicate enrollment — should SIGNAL an error
-- CALL sp_enroll_student(1, 1, '2026-07-01');


-- Step 45: sp_transfer_student — move student between departments
-- Creates a log table first, then wraps the transfer in a transaction
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id          INT         PRIMARY KEY AUTO_INCREMENT,
    student_id      INT         NOT NULL,
    from_dept_id    INT         NOT NULL,
    to_dept_id      INT         NOT NULL,
    transfer_date   DATETIME    DEFAULT CURRENT_TIMESTAMP,
    transferred_by  VARCHAR(50) DEFAULT 'system'
);

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_transfer_student $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id     INT,
    IN p_new_dept_id    INT
)
BEGIN
    DECLARE v_old_dept_id   INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Any SQL error triggers this handler — rolls back everything
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transfer failed — transaction rolled back.';
    END;

    -- Get current department before we change it
    SELECT department_id INTO v_old_dept_id
    FROM   students
    WHERE  student_id = p_student_id;

    START TRANSACTION;

        -- Statement 1: update the student's department
        UPDATE students
        SET    department_id = p_new_dept_id
        WHERE  student_id    = p_student_id;

        -- Statement 2: log the transfer
        INSERT INTO department_transfer_log
            (student_id, from_dept_id, to_dept_id)
        VALUES
            (p_student_id, v_old_dept_id, p_new_dept_id);

    COMMIT;

    SELECT CONCAT('Student ', p_student_id, ' transferred from dept ',
                  v_old_dept_id, ' to dept ', p_new_dept_id) AS result;
END $$

DELIMITER ;

-- Test: transfer Arjun (student_id=1) from CS (dept 1) to Electronics (dept 2)
CALL sp_transfer_student(1, 2);

-- Verify
SELECT student_id, first_name, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log;


-- Step 46: Test ROLLBACK by introducing an invalid FK
-- Transfer to department_id = 999 (does not exist)
-- The EXIT HANDLER catches the FK violation and rolls back
-- CALL sp_transfer_student(1, 999);
-- After calling this, verify student 1 still has department_id = 2
-- (the rollback means the UPDATE never committed)
SELECT student_id, first_name, department_id FROM students WHERE student_id = 1;


-- Step 47: SAVEPOINT — partial rollback within a transaction
-- WHY: SAVEPOINT lets you mark a checkpoint inside a transaction.
-- If the second operation fails, you can roll back to the checkpoint
-- and keep the first operation — instead of losing everything.
-- Use case: batch inserts where partial success is acceptable.

START TRANSACTION;

    -- First enrollment: Siddharth (student_id=10) into CS101 (course_id=1)
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (10, 1, '2026-07-01', NULL);

    SAVEPOINT after_first_insert;   -- checkpoint saved here

    -- Second enrollment: deliberately invalid — course_id 999 does not exist
    -- This will trigger FK constraint violation
    -- INSERT INTO enrollments (student_id, course_id, enrollment_date)
    -- VALUES (10, 999, '2026-07-01');
    -- If uncommented, the above fails → ROLLBACK TO after_first_insert
    -- → only the second insert is undone, the first survives

ROLLBACK TO SAVEPOINT after_first_insert;  -- undo only from savepoint forward

COMMIT;  -- commit everything up to and including the savepoint

-- Verify: Siddharth's enrollment in CS101 exists (first insert survived)
SELECT * FROM enrollments WHERE student_id = 10;
