-- ============================================================
-- Digital Nurture 5.0 | Database Integration | Hands-On 4
-- Query Optimisation — Indexes, EXPLAIN & the N+1 Problem
-- Author: Madhumitha R
-- Prerequisite: hands_on_1.sql + hands_on_2.sql + hands_on_3.sql
-- ============================================================

USE college_db;

-- ============================================================
-- TASK 1: BASELINE — EXPLAIN BEFORE INDEXES (Steps 48–50)
--
-- WHY: EXPLAIN shows you how MySQL plans to execute a query
-- WITHOUT actually running it. It tells you:
-- - which tables are scanned in what order
-- - how many rows MySQL estimates it will examine
-- - whether it uses an index or a full table scan
--
-- A Full Table Scan (type=ALL in MySQL EXPLAIN) means MySQL
-- reads every single row in the table to find matches.
-- Fine for 10 rows. Catastrophic for 1,000,000 rows.
-- ============================================================

-- Step 48: Run EXPLAIN on the 3-table join query BEFORE indexes
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM   enrollments e
JOIN   students s ON s.student_id = e.student_id
JOIN   courses  c ON c.course_id  = e.course_id
WHERE  s.enrollment_year = 2022;

-- ---------------------------------------------------------------
-- BASELINE EXPLAIN OUTPUT (captured from MySQL 9.7 on sample data)
-- ---------------------------------------------------------------
-- Key observations from the output:
--
-- 1. students table: type = "ALL" → FULL TABLE SCAN
--    rows_examined_per_scan ≈ 10 (all student rows checked)
--    used_key_parts = [] → NO index used for enrollment_year filter
--    This means MySQL reads every student row and checks whether
--    enrollment_year = 2022. With 1M students, that's 1M row reads.
--
-- 2. enrollments table: type = "ALL" → FULL TABLE SCAN
--    No index on student_id (FK exists but index not yet created)
--
-- 3. courses table: type = "eq_ref" → PRIMARY KEY lookup (fast)
--    This is already efficient because course_id is the PK.
--
-- CONCLUSION: Two full table scans. This query does not scale.
-- Adding an index on students.enrollment_year will fix scan #1.
-- Adding a composite index on enrollments(student_id, course_id)
-- will fix scan #2 and also enforce duplicate enrollment prevention.
-- ---------------------------------------------------------------


-- ============================================================
-- TASK 2: ADD INDEXES AND COMPARE PLANS (Steps 51–55)
--
-- WHY INDEXES WORK:
-- A B-Tree index is like a book's index — instead of reading
-- every page to find "enrollment_year = 2022", MySQL looks up
-- 2022 in the index tree (O(log n) lookup) and jumps directly
-- to the matching rows. For high-cardinality columns, this
-- reduces rows examined from millions to dozens.
--
-- TRADE-OFF: Every index speeds up reads but slows down
-- writes (INSERT/UPDATE/DELETE must update the index too).
-- Don't index every column — index columns you actually
-- filter or join on in frequent queries.
-- ============================================================

-- Step 51: B-Tree index on students.enrollment_year
-- WHY: The WHERE s.enrollment_year = 2022 filter in our query
-- was causing a full table scan. This index lets MySQL jump
-- directly to the 2022 bucket.
CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);


-- Step 52: Composite UNIQUE index on enrollments(student_id, course_id)
-- WHY TWO BENEFITS IN ONE:
-- 1. Performance: JOIN on student_id becomes an index lookup
--    instead of a full scan of the enrollments table.
-- 2. Data integrity: UNIQUE constraint prevents the same student
--    from being enrolled in the same course twice at the DB level,
--    independent of application-layer checks.
-- Column order matters: student_id first because queries
-- filter/join on student_id more often than course_id alone.
CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);


-- Step 53: Index on courses.course_code
-- WHY: course_code is used in WHERE clauses constantly
-- (e.g. WHERE course_code = 'CS101'). Without this index,
-- every such query scans the entire courses table.
CREATE INDEX idx_courses_course_code
ON courses(course_code);


-- Step 54: Re-run EXPLAIN and compare to baseline
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM   enrollments e
JOIN   students s ON s.student_id = e.student_id
JOIN   courses  c ON c.course_id  = e.course_id
WHERE  s.enrollment_year = 2022;

-- ---------------------------------------------------------------
-- POST-INDEX EXPLAIN OUTPUT — comparison to baseline
-- ---------------------------------------------------------------
-- Key changes after adding indexes:
--
-- 1. students table: type changed from "ALL" → "ref"
--    key = "idx_students_enrollment_year"
--    rows_examined_per_scan drops significantly
--    MySQL now uses the index to jump directly to 2022 students.
--    On a 1M-row table, rows examined: ~1,000,000 → ~50,000
--    (assuming ~5% enrolled in 2022)
--
-- 2. enrollments table: type changed from "ALL" → "ref"
--    key = "idx_enrollments_student_course"
--    MySQL now uses the composite index to find enrollments
--    for each student_id without scanning the whole table.
--
-- 3. courses table: unchanged — was already using PRIMARY KEY.
--
-- CONCLUSION: Two index scans instead of two full table scans.
-- The query now scales with data volume rather than degrading.
-- ---------------------------------------------------------------


-- Step 55: Partial index concept — documented as comments
-- (MySQL 8 does not support partial indexes with WHERE clause
-- the way PostgreSQL does — CREATE INDEX ... WHERE grade IS NULL
-- is a PostgreSQL feature. In MySQL, the equivalent strategy
-- is a composite index or a generated column.)

-- PARTIAL INDEX CONCEPT (PostgreSQL syntax for reference):
-- CREATE INDEX idx_enrollments_unevaluated
-- ON enrollments(student_id)
-- WHERE grade IS NULL;
--
-- WHY: A partial index only indexes rows matching the WHERE
-- condition. In this case, only unenrolled/unevaluated students.
-- If 5% of enrollments are ungraded, the partial index is 95%
-- smaller than a full index — faster to scan, less memory.
-- Use case: finding all students who haven't received a grade yet
-- for follow-up notifications. This query runs hundreds of times
-- per day on a real system; the partial index makes it instant.
--
-- MySQL equivalent: use a composite index or filter via
-- a generated column:
ALTER TABLE enrollments
    ADD COLUMN is_ungraded TINYINT(1)
    GENERATED ALWAYS AS (grade IS NULL) STORED;

CREATE INDEX idx_enrollments_ungraded
ON enrollments(is_ungraded);

-- Verify all indexes created
SHOW INDEX FROM students;
SHOW INDEX FROM enrollments;
SHOW INDEX FROM courses;
