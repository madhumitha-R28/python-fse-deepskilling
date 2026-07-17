# ============================================================
# Digital Nurture 5.0 | Database Integration | Hands-On 6
# Task 1: SQLAlchemy ORM — Define Models and Connect
# Author: Madhumitha R
# File: models.py
#
# WHY ORM MODELS:
# Instead of writing CREATE TABLE SQL manually, you define
# Python classes. SQLAlchemy translates them to SQL at runtime.
# Benefits:
# 1. Database-agnostic — switch from MySQL to PostgreSQL by
#    changing one connection string, zero code changes.
# 2. Python objects — work with Student() instances instead
#    of raw tuples from cursor.fetchall()
# 3. Relationships — student.department gives you the
#    Department object, no JOIN written manually
#
# INSTALL: pip install sqlalchemy mysql-connector-python
# ============================================================

from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    Date, Numeric, Boolean, Time, create_engine
)
from sqlalchemy.orm import relationship, declarative_base

# Base is the registry — every model class inherits from it.
# It tracks all model definitions so create_all() knows what
# tables to create.
Base = declarative_base()


# ============================================================
# MODEL DEFINITIONS
# Column order mirrors hands_on_1.sql intentionally —
# same schema, different syntax (Python vs SQL DDL)
# ============================================================

class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Numeric(12, 2))

    # One department → many students, courses, professors
    # back_populates creates the reverse reference on the other model
    students     = relationship('Student',    back_populates='department')
    courses      = relationship('Course',     back_populates='department')
    professors   = relationship('Professor',  back_populates='department')

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.dept_name}')>"


class Student(Base):
    __tablename__ = 'students'

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50),  nullable=False)
    last_name       = Column(String(50),  nullable=False)
    email           = Column(String(100), nullable=False, unique=True)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey('departments.department_id'))
    enrollment_year = Column(Integer)
    is_active       = Column(Boolean, default=True)   # added in HO7 migration

    # Many students → one department
    department  = relationship('Department', back_populates='students')
    # One student → many enrollments
    enrollments = relationship('Enrollment', back_populates='student')

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.first_name} {self.last_name}')>"


class Course(Base):
    __tablename__ = 'courses'

    course_id   = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20),  unique=True)
    credits     = Column(Integer)
    max_seats   = Column(Integer, default=60)
    department_id = Column(Integer, ForeignKey('departments.department_id'))

    department  = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}', name='{self.course_name}')>"


class Enrollment(Base):
    __tablename__ = 'enrollments'

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey('students.student_id'))
    course_id       = Column(Integer, ForeignKey('courses.course_id'))
    enrollment_date = Column(Date)
    grade           = Column(String(2))

    # Many enrollments → one student / one course
    student = relationship('Student', back_populates='enrollments')
    course  = relationship('Course',  back_populates='enrollments')

    def __repr__(self):
        return (f"<Enrollment(id={self.enrollment_id}, "
                f"student_id={self.student_id}, course_id={self.course_id}, "
                f"grade='{self.grade}')>")


class Professor(Base):
    __tablename__ = 'professors'

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'))
    salary        = Column(Numeric(10, 2))

    department = relationship('Department', back_populates='professors')

    def __repr__(self):
        return f"<Professor(id={self.professor_id}, name='{self.prof_name}')>"


class CourseSchedule(Base):
    """Added in HO7 migration — demonstrates incremental schema evolution."""
    __tablename__ = 'course_schedules'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id   = Column(Integer, ForeignKey('courses.course_id'))
    day_of_week = Column(String(10))   # Monday, Tuesday, etc.
    start_time  = Column(Time)
    end_time    = Column(Time)

    def __repr__(self):
        return (f"<CourseSchedule(course_id={self.course_id}, "
                f"day='{self.day_of_week}')>")


# ============================================================
# ENGINE + TABLE CREATION (Step 76, 79)
#
# create_engine() sets up the connection pool.
# echo=True prints every SQL statement SQLAlchemy generates —
# invaluable during development to see what's happening.
#
# Connection string format for MySQL:
# mysql+mysqlconnector://user:password@host/database
# ============================================================

from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="madhu@mysql",
    host="localhost",
    database="college_db_orm"
)

engine = create_engine(connection_url, echo=True)

if __name__ == '__main__':
    # Step 79: Create all tables defined above in college_db_orm
    # First create the database in MySQL Workbench:
    # CREATE DATABASE college_db_orm;
    # Then run: python models.py
    print("Creating all tables in college_db_orm...")
    Base.metadata.create_all(engine)
    print("\nDone. Verify in MySQL Workbench:")
    print("USE college_db_orm; SHOW TABLES;")
    print("Expected: departments, students, courses, enrollments,")
    print("          professors, course_schedules")
