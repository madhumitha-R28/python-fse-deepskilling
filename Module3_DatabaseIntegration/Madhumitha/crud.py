# ============================================================
# Digital Nurture 5.0 | Database Integration | Hands-On 6
# Tasks 2 & 3: CRUD Operations + Eager Loading (N+1 Fix)
# Author: Madhumitha R
# File: crud.py
#
# N+1 QUERY COUNT COMPARISON (documented as required by Step 90):
# ---------------------------------------------------------------
# WITHOUT joinedload (Task 2, Step 84):
#   - 1 query to fetch all enrollments
#   - 1 query PER enrollment to lazy-load enrollment.student
#   - 1 query PER enrollment to lazy-load enrollment.course
#   - Total with 4 enrollments: 1 + 4 + 4 = 9 queries
#   - Total with 1000 enrollments: 2001 queries
#
# WITH joinedload (Task 3, Step 88):
#   - 1 single SQL query with LEFT OUTER JOINs on both
#     students and courses tables
#   - Total regardless of enrollment count: 1 query
#
# HOW TO SEE IT:
#   Set echo=True on the engine in models.py, then run this
#   file. Watch the terminal — count the SELECT statements.
#   First run (N+1): many SELECTs. Second run (joinedload): 1.
# ============================================================

from datetime import date
from sqlalchemy.orm import sessionmaker, joinedload
from models import (
    engine, Base,
    Department, Student, Course, Enrollment, Professor
)


# sessionmaker creates a Session factory bound to our engine.
# Session = unit of work — tracks all changes until commit().
# Think of it as a transaction wrapper around your Python objects.
Session = sessionmaker(bind=engine)


# ============================================================
# TASK 2: CRUD OPERATIONS (Steps 80–86)
# ============================================================

def run_crud():
    session = Session()

    try:
        # --------------------------------------------------------
        # Step 81: INSERT — 3 Departments + 5 Students
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 81: Inserting Departments and Students")
        print("="*60)

        cs_dept   = Department(dept_name='Computer Science', head_of_dept='Dr. Ramesh Kumar', budget=850000)
        ec_dept   = Department(dept_name='Electronics',      head_of_dept='Dr. Priya Nair',   budget=620000)
        me_dept   = Department(dept_name='Mechanical',       head_of_dept='Dr. Suresh Iyer',  budget=540000)

        session.add_all([cs_dept, ec_dept, me_dept])
        session.flush()  # flush to get auto-generated IDs without committing
        # After flush, cs_dept.department_id is populated
        print(f"  Departments created: {cs_dept}, {ec_dept}, {me_dept}")

        students = [
            Student(first_name='Arjun',   last_name='Mehta',  email='arjun.mehta@college.edu',
                    date_of_birth=date(2003, 4, 12),  department_id=cs_dept.department_id, enrollment_year=2022),
            Student(first_name='Priya',   last_name='Suresh', email='priya.suresh@college.edu',
                    date_of_birth=date(2003, 7, 25),  department_id=cs_dept.department_id, enrollment_year=2022),
            Student(first_name='Rohan',   last_name='Verma',  email='rohan.verma@college.edu',
                    date_of_birth=date(2002, 11, 8),  department_id=ec_dept.department_id, enrollment_year=2021),
            Student(first_name='Sneha',   last_name='Patel',  email='sneha.patel@college.edu',
                    date_of_birth=date(2004, 1, 30),  department_id=me_dept.department_id, enrollment_year=2023),
            Student(first_name='Vikram',  last_name='Das',    email='vikram.das@college.edu',
                    date_of_birth=date(2003, 9, 14),  department_id=cs_dept.department_id, enrollment_year=2022),
        ]
        session.add_all(students)
        session.commit()
        print(f"  {len(students)} students committed.")

        # --------------------------------------------------------
        # Step 82: INSERT — 3 Courses + 4 Enrollments
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 82: Inserting Courses and Enrollments")
        print("="*60)

        courses = [
            Course(course_name='Data Structures & Algorithms', course_code='CS101', credits=4, department_id=cs_dept.department_id),
            Course(course_name='Database Management Systems',  course_code='CS102', credits=3, department_id=cs_dept.department_id),
            Course(course_name='Object Oriented Programming',  course_code='CS103', credits=4, department_id=cs_dept.department_id),
        ]
        session.add_all(courses)
        session.flush()

        # Re-query to get IDs cleanly after flush
        cs101 = session.query(Course).filter_by(course_code='CS101').first()
        cs102 = session.query(Course).filter_by(course_code='CS102').first()
        cs103 = session.query(Course).filter_by(course_code='CS103').first()
        arjun = session.query(Student).filter_by(email='arjun.mehta@college.edu').first()
        priya = session.query(Student).filter_by(email='priya.suresh@college.edu').first()

        enrollments = [
            Enrollment(student_id=arjun.student_id, course_id=cs101.course_id,
                       enrollment_date=date(2022, 7, 1), grade='A'),
            Enrollment(student_id=arjun.student_id, course_id=cs102.course_id,
                       enrollment_date=date(2022, 7, 1), grade='B'),
            Enrollment(student_id=priya.student_id, course_id=cs101.course_id,
                       enrollment_date=date(2022, 7, 1), grade='B'),
            Enrollment(student_id=priya.student_id, course_id=cs103.course_id,
                       enrollment_date=date(2022, 7, 1), grade='A'),
        ]
        session.add_all(enrollments)
        session.commit()
        print(f"  {len(courses)} courses and {len(enrollments)} enrollments committed.")

        # --------------------------------------------------------
        # Step 83: READ — Students in Computer Science dept
        # This generates a JOIN query behind the scenes.
        # ORM syntax:  session.query(Student).join(Department)
        # SQL produced: SELECT students.* FROM students
        #               INNER JOIN departments ON ...
        #               WHERE departments.dept_name = 'Computer Science'
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 83: READ — CS department students")
        print("="*60)

        cs_students = (
            session.query(Student)
            .join(Department)
            .filter(Department.dept_name == 'Computer Science')
            .all()
        )
        for s in cs_students:
            print(f"  {s.first_name} {s.last_name} | Year: {s.enrollment_year}")

        # --------------------------------------------------------
        # Step 84: READ — All enrollments, print student + course
        # This is where N+1 appears if relationships are lazy-loaded.
        # With echo=True on the engine, watch the SELECT count.
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 84: READ — Enrollments (N+1 version — watch echo output)")
        print("="*60)

        all_enrollments = session.query(Enrollment).all()
        for e in all_enrollments:
            # Each access to e.student and e.course fires a separate
            # lazy-load SELECT if not already in session cache.
            # With 4 enrollments this is manageable but with 1000 it
            # becomes 2001 queries.
            print(f"  {e.student.first_name} {e.student.last_name} → "
                  f"{e.course.course_name} | Grade: {e.grade}")

        # --------------------------------------------------------
        # Step 85: UPDATE — change enrollment_year for a student
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 85: UPDATE — enrollment_year")
        print("="*60)

        student_to_update = (
            session.query(Student)
            .filter(Student.email == 'sneha.patel@college.edu')
            .first()
        )
        print(f"  Before: {student_to_update.first_name} | Year: {student_to_update.enrollment_year}")
        student_to_update.enrollment_year = 2024   # just assign — ORM tracks the change
        session.commit()
        print(f"  After:  {student_to_update.first_name} | Year: {student_to_update.enrollment_year}")

        # --------------------------------------------------------
        # Step 86: DELETE — remove one enrollment
        # --------------------------------------------------------
        print("\n" + "="*60)
        print("STEP 86: DELETE — remove one enrollment")
        print("="*60)

        enrollment_to_delete = (
            session.query(Enrollment)
            .filter(
                Enrollment.student_id == priya.student_id,
                Enrollment.course_id  == cs103.course_id
            )
            .first()
        )
        if enrollment_to_delete:
            print(f"  Deleting: {enrollment_to_delete}")
            session.delete(enrollment_to_delete)
            session.commit()
            print("  Deleted and committed.")

        remaining = session.query(Enrollment).count()
        print(f"  Remaining enrollments: {remaining}")

    except Exception as e:
        session.rollback()
        print(f"\nError — rolled back: {e}")
        raise
    finally:
        session.close()


# ============================================================
# TASK 3: EAGER LOADING — FIX THE N+1 PROBLEM (Steps 87–90)
# ============================================================

def run_eager_loading():
    session = Session()

    try:
        print("\n" + "="*60)
        print("TASK 3: EAGER LOADING with joinedload")
        print("Watch echo output — should be 1 SQL query, not N+1")
        print("="*60)

        # Step 88: joinedload tells SQLAlchemy to fetch student
        # and course data in the SAME query using LEFT OUTER JOINs.
        # SQL produced (one query):
        # SELECT enrollments.*, students.*, courses.*
        # FROM enrollments
        # LEFT OUTER JOIN students ON enrollments.student_id = students.student_id
        # LEFT OUTER JOIN courses  ON enrollments.course_id  = courses.course_id
        #
        # Compare this to Step 84 which produced:
        # 1 SELECT from enrollments
        # + 1 SELECT per enrollment for student  (lazy load)
        # + 1 SELECT per enrollment for course   (lazy load)
        all_enrollments = (
            session.query(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.course)
            )
            .all()
        )

        for e in all_enrollments:
            # student and course are already loaded — no extra queries
            print(f"  {e.student.first_name} {e.student.last_name} → "
                  f"{e.course.course_name} | Grade: {e.grade}")

        # Step 89: Count lines in echo output that say "SELECT"
        # Step 84 (N+1):    many SELECTs
        # Step 88 (joined): 1 SELECT with 2 LEFT OUTER JOINs

        # Step 91 (Bonus): Django ORM equivalent
        # from courses.models import Enrollment
        # enrollments = Enrollment.objects.select_related('student', 'course').all()
        # for e in enrollments:
        #     print(e.student.first_name, e.course.course_name)
        # Django's select_related does the same JOIN under the hood.

    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    # Create tables first if not already created
    Base.metadata.create_all(engine)

    run_crud()
    run_eager_loading()
