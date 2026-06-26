-- ============================================================
-- Digital Nurture 5.0 | Database Integration | Hands-On 1
-- Schema Design & Core SQL — DDL and Normalisation
-- Author: Madhumitha R
-- File: hands_on_1.sql
-- Usage: Run in MySQL Workbench against a fresh MySQL 9.7 connection
-- ============================================================


-- ============================================================
-- TASK 1: Create the Database and Tables
-- ============================================================

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS college_db;
USE college_db;

-- ------------------------------------------------------------
-- Step 2 & 3 & 4: CREATE TABLE statements
-- Order matters — departments has no FK dependencies,
-- so it must be created first. students, courses, professors
-- all reference departments. enrollments references both
-- students and courses, so it goes last.
-- ------------------------------------------------------------

-- Table 1: departments (no FK dependencies — create first)
CREATE TABLE IF NOT EXISTS departments (
    department_id   INT             PRIMARY KEY AUTO_INCREMENT,
    dept_name       VARCHAR(100)    NOT NULL,
    hod_name        VARCHAR(100),                       -- Head of Department
    budget          DECIMAL(12, 2)
);

-- Table 2: students (references departments)
CREATE TABLE IF NOT EXISTS students (
    student_id      INT             PRIMARY KEY AUTO_INCREMENT,
    first_name      VARCHAR(50)     NOT NULL,
    last_name       VARCHAR(50)     NOT NULL,
    email           VARCHAR(100)    NOT NULL UNIQUE,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Table 3: courses (references departments)
CREATE TABLE IF NOT EXISTS courses (
    course_id       INT             PRIMARY KEY AUTO_INCREMENT,
    course_name     VARCHAR(150)    NOT NULL,
    course_code     VARCHAR(20)     UNIQUE,
    credits         INT,
    department_id   INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Table 4: professors (references departments)
CREATE TABLE IF NOT EXISTS professors (
    professor_id    INT             PRIMARY KEY AUTO_INCREMENT,
    prof_name       VARCHAR(100)    NOT NULL,
    email           VARCHAR(100)    UNIQUE,
    department_id   INT,
    salary          DECIMAL(10, 2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- Table 5: enrollments (references students AND courses — create last)
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id   INT             PRIMARY KEY AUTO_INCREMENT,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(2),                            -- A, B, C, D, F — nullable
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

-- Step 5: Verify — run these after creation to confirm all tables and constraints
-- DESCRIBE departments;
-- DESCRIBE students;
-- DESCRIBE courses;
-- DESCRIBE professors;
-- DESCRIBE enrollments;
-- SHOW CREATE TABLE enrollments;   -- shows FK definitions clearly


-- ============================================================
-- TASK 2: Verify Normalisation (Steps 6–9)
-- Analysis documented as SQL comments as required by the task
-- ============================================================

-- ------------------------------------------------------------
-- NORMALISATION ANALYSIS FOR college_db
-- ------------------------------------------------------------

-- 1NF (First Normal Form) — Atomic values, no repeating groups
-- ---------------------------------------------------------------
-- COMPLIANT.
-- Every column in every table holds exactly one atomic value per row.
-- Example: students.email holds one email address per row — not a
-- comma-separated list like 'a@x.com, b@x.com'.
-- Example: enrollments stores one (student, course) pair per row —
-- not a list of course IDs in a single cell.
--
-- HYPOTHETICAL VIOLATION (if poorly designed):
-- If we had stored multiple phone numbers in one column like:
--   phone_numbers VARCHAR(200) -- e.g. '9876543210, 9123456789'
-- that would violate 1NF because the column is no longer atomic.
-- Fix: create a separate student_phones table with one row per number.

-- 2NF (Second Normal Form) — No partial dependencies on a composite key
-- -----------------------------------------------------------------------
-- COMPLIANT.
-- 2NF only applies to tables with a composite primary key.
-- The enrollments table has a surrogate PK (enrollment_id), so technically
-- it has no composite PK to worry about. However, the natural/candidate key
-- of enrollments is (student_id + course_id).
--
-- Checking for partial dependencies on (student_id, course_id):
--   - enrollment_date depends on BOTH student_id and course_id (the specific
--     enrollment event) — NOT a partial dependency. Compliant.
--   - grade depends on BOTH (it's the grade for that student in that course)
--     — NOT a partial dependency. Compliant.
--
-- A PARTIAL DEPENDENCY would look like:
--   If we stored student.first_name inside enrollments — that depends only
--   on student_id, not on the full (student_id, course_id) key. That would
--   violate 2NF. We avoid this by keeping student data in the students table.

-- 3NF (Third Normal Form) — No transitive dependencies
-- -------------------------------------------------------
-- COMPLIANT.
-- A transitive dependency exists when: non-key column C depends on
-- non-key column B, which depends on primary key A.
-- (A → B → C, meaning C is only indirectly dependent on A.)
--
-- ENROLLMENTS TABLE — 3NF CHECK:
--   enrollment_id (PK) → student_id → [student data lives in students table]
--   enrollment_id (PK) → course_id  → [course data lives in courses table]
--   enrollment_id (PK) → enrollment_date (direct dependency) — OK
--   enrollment_id (PK) → grade (direct dependency) — OK
--   No transitive dependencies exist in enrollments. COMPLIANT.
--
-- HYPOTHETICAL TRANSITIVE VIOLATION:
--   If we stored dept_name inside the students table:
--     student_id → department_id → dept_name
--   Then dept_name would transitively depend on student_id via department_id.
--   This violates 3NF. We fix it by storing dept_name only in departments
--   and referencing it via the department_id foreign key — exactly what
--   the current schema does.
--
-- STUDENTS TABLE — 3NF CHECK:
--   student_id → department_id (direct FK — fine)
--   student_id → first_name, last_name, email, dob, enrollment_year
--   All non-key columns depend directly on student_id. COMPLIANT.


-- ============================================================
-- TASK 3: Alter and Extend the Schema (Steps 10–14)
-- ============================================================

-- Step 10: Add phone_number column to students
ALTER TABLE students
    ADD COLUMN phone_number VARCHAR(15);

-- Verify:
-- SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
-- FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_SCHEMA = 'college_db' AND TABLE_NAME = 'students';

-- Step 11: Add max_seats column with default to courses
ALTER TABLE courses
    ADD COLUMN max_seats INT DEFAULT 60;

-- Step 12: Add CHECK constraint on enrollments.grade
-- In MySQL 8+, CHECK constraints are enforced (unlike older versions).
-- This ensures grade can only be A, B, C, D, F — or NULL (unenrolled).
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade
    CHECK (grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL);

-- Step 13: Rename hod_name → head_of_dept in departments
-- MySQL syntax: ALTER TABLE ... CHANGE old_name new_name datatype
ALTER TABLE departments
    CHANGE hod_name head_of_dept VARCHAR(100);

-- Verify rename:
-- DESCRIBE departments;

-- Step 14: Drop the phone_number column (simulate schema rollback)
ALTER TABLE students
    DROP COLUMN phone_number;

-- Final verification — expected outcome:
-- departments : department_id, dept_name, head_of_dept, budget
-- students    : student_id, first_name, last_name, email,
--               date_of_birth, department_id, enrollment_year
--               (phone_number should be GONE)
-- courses     : course_id, course_name, course_code, credits,
--               department_id, max_seats
-- DESCRIBE departments;
-- DESCRIBE students;
-- DESCRIBE courses;


-- ============================================================
-- SAMPLE DATA (from Common Schema — run after schema is ready)
-- Keep here so the file is fully self-contained for submission
-- ============================================================

INSERT INTO departments (dept_name, head_of_dept, budget) VALUES
    ('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
    ('Electronics',      'Dr. Priya Nair',   620000.00),
    ('Mechanical',       'Dr. Suresh Iyer',  540000.00),
    ('Civil',            'Dr. Ananya Sharma',430000.00);

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
    ('Arjun',   'Mehta',  'arjun.mehta@college.edu',  '2003-04-12', 1, 2022),
    ('Priya',   'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
    ('Rohan',   'Verma',  'rohan.verma@college.edu',  '2002-11-08', 2, 2021),
    ('Sneha',   'Patel',  'sneha.patel@college.edu',  '2004-01-30', 3, 2023),
    ('Vikram',  'Das',    'vikram.das@college.edu',   '2003-09-14', 1, 2022),
    ('Kavya',   'Menon',  'kavya.menon@college.edu',  '2002-05-17', 2, 2021),
    ('Aditya',  'Singh',  'aditya.singh@college.edu', '2004-03-22', 4, 2023),
    ('Deepika', 'Rao',    'deepika.rao@college.edu',  '2003-08-09', 1, 2022);

INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
    ('Data Structures & Algorithms', 'CS101', 4, 1),
    ('Database Management Systems',  'CS102', 3, 1),
    ('Object Oriented Programming',  'CS103', 4, 1),
    ('Circuit Theory',               'EC101', 3, 2),
    ('Thermodynamics',               'ME101', 3, 3);

INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
    (1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
    (2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
    (3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
    (5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
    (6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
    (8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

INSERT INTO professors (prof_name, email, department_id, salary) VALUES
    ('Dr. Anand Krishnan', 'anand.k@college.edu',  1, 95000.00),
    ('Dr. Meena Pillai',   'meena.p@college.edu',  1, 88000.00),
    ('Dr. Sunil Rajan',    'sunil.r@college.edu',  2, 82000.00),
    ('Dr. Latha Gopal',    'latha.g@college.edu',  3, 79000.00),
    ('Dr. Kartik Bose',    'kartik.b@college.edu', 4, 76000.00);
