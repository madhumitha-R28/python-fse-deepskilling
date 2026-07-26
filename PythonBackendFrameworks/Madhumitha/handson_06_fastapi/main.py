# ============================================================
# Digital Nurture 5.0 | Backend HO6-7 | FastAPI Course Manager
# Author: Madhumitha R
# SETUP: pip install fastapi uvicorn sqlalchemy aiosqlite
# RUN:   uvicorn main:app --reload
# DOCS:  http://127.0.0.1:8000/docs
# ============================================================

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ============================================================
# DATABASE SETUP
# ============================================================
DATABASE_URL = "sqlite:///./fastapi_coursemanager.db"
engine       = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base         = declarative_base()


class CourseDB(Base):
    __tablename__ = "courses"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(150), nullable=False)
    code          = Column(String(20), unique=True, nullable=False)
    credits       = Column(Integer)
    department_id = Column(Integer, nullable=True)


Base.metadata.create_all(bind=engine)


# ============================================================
# PYDANTIC SCHEMAS (HO6 Task 1, Steps 58-59)
# ============================================================
class CourseCreate(BaseModel):
    name:          str
    code:          str
    credits:       int
    department_id: Optional[int] = None


class CourseUpdate(BaseModel):
    # All fields optional for PATCH support
    name:          Optional[str] = None
    code:          Optional[str] = None
    credits:       Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id:            int
    name:          str
    code:          str
    credits:       int
    department_id: Optional[int]

    class Config:
        from_attributes = True   # Pydantic v2: read from ORM objects


# ============================================================
# DEPENDENCY INJECTION — get_db (HO6 Task 2, Step 65)
# Yields a session per request, closes it after
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# FASTAPI APP (HO7 Task 2, Steps 75-77: metadata + tags)
# ============================================================
app = FastAPI(
    title       = "Course Management API",
    description = "Digital Nurture 5.0 — Python FSE Deep Skilling",
    version     = "1.0.0",
    contact     = {"name": "Madhumitha R", "email": "madhumitha.r.2023.cse@ritchennai.edu.in"}
)

# HO9: CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:3000", "http://localhost:5173"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)


# ============================================================
# HELPER
# ============================================================
def get_course_or_404(course_id: int, db: Session):
    course = db.query(CourseDB).filter(CourseDB.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} does not exist")
    return course


# ============================================================
# ROUTES (HO6 + HO7)
# ============================================================
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Course Management API is running"}


@app.get(
    "/api/v1/courses/",
    response_model     = List[CourseResponse],
    tags               = ["Courses"],
    summary            = "List all courses with optional pagination and filtering"
)
async def list_courses(
    skip:          int          = 0,
    limit:         int          = 10,
    department_id: Optional[int] = None,
    search:        Optional[str] = None,
    db:            Session       = Depends(get_db)
):
    # HO8 Task 2, Step 83: offset pagination
    query = db.query(CourseDB)
    if department_id:
        query = query.filter(CourseDB.department_id == department_id)
    if search:
        query = query.filter(
            CourseDB.name.ilike(f"%{search}%") | CourseDB.code.ilike(f"%{search}%")
        )
    total   = query.count()
    courses = query.offset(skip).limit(limit).all()
    return courses


@app.post(
    "/api/v1/courses/",
    response_model      = CourseResponse,
    status_code         = status.HTTP_201_CREATED,
    tags                = ["Courses"],
    summary             = "Create a new course",
    response_description = "The created course object"
)
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = CourseDB(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int, db: Session = Depends(get_db)):
    return get_course_or_404(course_id, db)


@app.put("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: int, course: CourseCreate, db: Session = Depends(get_db)):
    db_course = get_course_or_404(course_id, db)
    for key, val in course.dict().items():
        setattr(db_course, key, val)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.patch("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def partial_update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    # HO8 Task 1, Step 79: PATCH = partial update
    db_course = get_course_or_404(course_id, db)
    for key, val in course.dict(exclude_unset=True).items():
        setattr(db_course, key, val)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.delete(
    "/api/v1/courses/{course_id}",
    status_code = status.HTTP_204_NO_CONTENT,
    tags        = ["Courses"]
)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    # HTTP 204 = correct status for DELETE — no response body
    db_course = get_course_or_404(course_id, db)
    db.delete(db_course)
    db.commit()


# HO7 Task 2, Step 73: Background task
def send_confirmation_email(student_email: str, course_name: str):
    # Runs AFTER the response is sent to the client
    # The client gets 201 immediately; this runs in background
    print(f"[Background] Sending enrollment confirmation to {student_email} for {course_name}")


@app.post("/api/v1/enrollments/", status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
async def create_enrollment(
    student_id:         int,
    course_id:          int,
    background_tasks:   BackgroundTasks,
    db:                 Session = Depends(get_db)
):
    course = get_course_or_404(course_id, db)
    # Add background task — does NOT block the response
    background_tasks.add_task(send_confirmation_email, "student@college.edu", course.name)
    return {"message": "Enrollment created", "course": course.name}
