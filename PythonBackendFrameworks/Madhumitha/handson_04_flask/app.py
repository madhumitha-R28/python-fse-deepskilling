# ============================================================
# Digital Nurture 5.0 | Backend HO4-5 | Flask Course Manager
# Author: Madhumitha R
# Structure: flask_coursemanager/app.py (entry point)
#
# SETUP:
#   pip install flask flask-sqlalchemy flask-migrate
#   export FLASK_APP=app.py
#   flask db init && flask db migrate -m "initial" && flask db upgrade
#   flask run
# ============================================================

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db      = SQLAlchemy()
migrate = Migrate()


# ============================================================
# APPLICATION FACTORY (HO4 Task 1, Step 37)
# WHY: testable, avoids circular imports, multiple configs possible
# ============================================================
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursemanager.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-change-in-prod'

    db.init_app(app)
    migrate.init_app(app, db)

    from courses_routes import courses_bp
    app.register_blueprint(courses_bp)

    # Step 45: JSON error handlers — APIs must never return HTML errors
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": {"code": "NOT_FOUND", "message": str(e)}}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": {"code": "BAD_REQUEST", "message": str(e)}}), 400

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "Server error"}}), 500

    return app


# ============================================================
# MODELS (HO5 Task 1, Step 48)
# ============================================================
class Department(db.Model):
    __tablename__ = 'departments'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget       = db.Column(db.Numeric(12, 2))
    courses      = db.relationship('Course', back_populates='department', lazy='select')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'head_of_dept': self.head_of_dept,
                'budget': float(self.budget) if self.budget else None}


class Course(db.Model):
    __tablename__ = 'courses'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    code          = db.Column(db.String(20), unique=True, nullable=False)
    credits       = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department    = db.relationship('Department', back_populates='courses')
    enrollments   = db.relationship('Enrollment', back_populates='course')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code,
                'credits': self.credits, 'department_id': self.department_id}


class Student(db.Model):
    __tablename__   = 'students'
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer)
    enrollments     = db.relationship('Enrollment', back_populates='student')

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name,
                'email': self.email, 'enrollment_year': self.enrollment_year}


class Enrollment(db.Model):
    __tablename__   = 'enrollments'
    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id       = db.Column(db.Integer, db.ForeignKey('courses.id'))
    enrollment_date = db.Column(db.Date)
    grade           = db.Column(db.String(2))
    student         = db.relationship('Student', back_populates='enrollments')
    course          = db.relationship('Course',  back_populates='enrollments')

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id, 'course_id': self.course_id,
                'grade': self.grade}


# ============================================================
# ROUTES — Blueprint (HO4 Task 1, Step 39)
# Save this section as courses_routes.py alongside app.py
# ============================================================
COURSES_ROUTES_PY = '''
from flask import Blueprint, jsonify, request, abort
from app import db, Course, Student, Enrollment

courses_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


def make_json(data, code=200):
    """Step 44: Consistent JSON envelope."""
    return jsonify({"status": "success", "data": data}), code


@courses_bp.route("/", methods=["GET"])
def list_courses():
    courses = Course.query.all()
    return make_json([c.to_dict() for c in courses])


@courses_bp.route("/", methods=["POST"])
def create_course():
    body = request.get_json()
    if not body:
        abort(400, "Request body must be JSON")
    for field in ("name", "code", "credits"):
        if field not in body:
            abort(400, f"Missing required field: {field}")
    course = Course(name=body["name"], code=body["code"],
                    credits=body["credits"], department_id=body.get("department_id"))
    db.session.add(course)
    db.session.commit()
    return make_json(course.to_dict(), 201)


@courses_bp.route("/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_json(course.to_dict())


@courses_bp.route("/<int:course_id>/", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    body   = request.get_json() or {}
    for field in ("name", "code", "credits", "department_id"):
        if field in body:
            setattr(course, field, body[field])
    db.session.commit()
    return make_json(course.to_dict())


@courses_bp.route("/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return "", 204


@courses_bp.route("/<int:course_id>/students/", methods=["GET"])
def enrolled_students(course_id):
    course   = Course.query.get_or_404(course_id)
    students = Student.query.join(Enrollment).filter(Enrollment.course_id == course_id).all()
    return make_json([s.to_dict() for s in students])
'''

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
