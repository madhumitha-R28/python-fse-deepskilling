# ============================================================
# Digital Nurture 5.0 | Backend HO10 | Microservices
# Author: Madhumitha R
#
# FOLDER STRUCTURE:
#   handson_10_microservices/
#   ├── course_service/app.py    (port 5001)
#   ├── student_service/app.py   (port 5002)
#   └── gateway/app.py           (port 5000)
#
# RUN (3 separate terminals):
#   cd course_service  && python app.py
#   cd student_service && python app.py
#   cd gateway         && python app.py
# ============================================================

# ============================================================
# SERVICE DECOMPOSITION ANALYSIS (Step 96-97)
# ============================================================
DECOMPOSITION_README = """
# Course Management — Microservices Decomposition

## Bounded Contexts Identified

| Service | Responsibility | Endpoints Owned | Database |
|---|---|---|---|
| Course Service | Department + Course CRUD | /api/courses/, /api/departments/ | courses.db (SQLite) |
| Student Service | Student CRUD + Enrollment | /api/students/, /api/enrollments/ | students.db (SQLite) |
| Auth Service | Registration, Login, Token validation | /api/auth/ | auth.db (SQLite) |
| Notification Service | Email confirmations, SMS | (async, no direct endpoint) | None (stateless) |

## Key Microservices Principles Applied
1. Each service owns its own database — no shared DB access
2. Services communicate via HTTP (synchronous) for this demo
3. The API Gateway is the single entry point for all clients
4. If a service is unavailable, the gateway returns 503 (not a crash)

## Trade-offs: Synchronous (HTTP) vs Asynchronous (Message Queue)

**Synchronous (HTTP — what we built):**
- Simple to understand and debug
- Tight coupling: if Course Service is down, enrollment fails immediately
- Client waits for the full chain to complete

**Asynchronous (Message Queue — RabbitMQ/Kafka):**
- Student Service publishes "EnrollmentRequested" event to queue
- Course Service consumes and validates asynchronously
- Services are decoupled: Student Service succeeds even if Course Service is temporarily down
- Trade-off: eventual consistency (enrollment confirmed later, not instantly)
- Use when: high volume, services need to scale independently, downtime tolerance needed
"""


# ============================================================
# COURSE SERVICE (port 5001)
# Save as: course_service/app.py
# ============================================================
COURSE_SERVICE = '''
from flask import Flask, jsonify, request

app   = Flask(__name__)
PORT  = 5001

# In-memory store (replace with SQLite for persistence)
courses = [
    {"id": 1, "name": "Data Structures", "code": "CS101", "credits": 4},
    {"id": 2, "name": "Database Systems", "code": "CS102", "credits": 3},
    {"id": 3, "name": "OOP",              "code": "CS103", "credits": 4},
]
next_id = 4


@app.route("/api/courses/", methods=["GET"])
def list_courses():
    return jsonify({"status": "success", "data": courses})


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return jsonify({"error": f"Course {course_id} not found"}), 404
    return jsonify({"status": "success", "data": course})


@app.route("/api/courses/", methods=["POST"])
def create_course():
    global next_id
    body = request.get_json()
    if not body or not all(k in body for k in ("name", "code", "credits")):
        return jsonify({"error": "Missing required fields"}), 400
    course = {"id": next_id, "name": body["name"], "code": body["code"], "credits": body["credits"]}
    courses.append(course)
    next_id += 1
    return jsonify({"status": "success", "data": course}), 201


if __name__ == "__main__":
    print(f"Course Service running on port {PORT}")
    app.run(port=PORT, debug=True)
'''


# ============================================================
# STUDENT SERVICE (port 5002)
# Save as: student_service/app.py
# ============================================================
STUDENT_SERVICE = '''
import requests
from flask import Flask, jsonify, request

app          = Flask(__name__)
PORT         = 5002
COURSE_SVC   = "http://localhost:5001"

students = [
    {"id": 1, "first_name": "Arjun",  "last_name": "Mehta",  "email": "arjun@college.edu"},
    {"id": 2, "first_name": "Priya",  "last_name": "Suresh", "email": "priya@college.edu"},
]
enrollments = []


@app.route("/api/students/", methods=["GET"])
def list_students():
    return jsonify({"status": "success", "data": students})


@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    """Step 100: Verify course exists via Course Service call."""
    body      = request.get_json() or {}
    course_id = body.get("course_id")
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Step 101: Call Course Service — handle unavailability gracefully
    try:
        resp = requests.get(f"{COURSE_SVC}/api/courses/{course_id}/", timeout=3)
        if resp.status_code == 404:
            return jsonify({"error": f"Course {course_id} does not exist"}), 404
        course = resp.json()["data"]
    except requests.exceptions.ConnectionError:
        # Step 101: Course Service is down — return 503 Service Unavailable
        return jsonify({
            "error": "Course Service is temporarily unavailable. Please try again later."
        }), 503

    enrollment = {
        "student_id": student_id,
        "course_id":  course_id,
        "course_name": course["name"]
    }
    enrollments.append(enrollment)
    return jsonify({"status": "success", "data": enrollment}), 201


if __name__ == "__main__":
    print(f"Student Service running on port {PORT}")
    app.run(port=PORT, debug=True)
'''


# ============================================================
# API GATEWAY (port 5000)
# Save as: gateway/app.py
# ============================================================
GATEWAY = '''
import requests
from flask import Flask, jsonify, request, Response

app          = Flask(__name__)
PORT         = 5000
COURSE_SVC   = "http://localhost:5001"
STUDENT_SVC  = "http://localhost:5002"

ROUTES = {
    "/api/courses":  COURSE_SVC,
    "/api/students": STUDENT_SVC,
}


def proxy(target_url):
    """Forward the current request to the target service."""
    try:
        resp = requests.request(
            method  = request.method,
            url     = target_url,
            headers = {k: v for k, v in request.headers if k != "Host"},
            json    = request.get_json(silent=True),
            params  = request.args,
            timeout = 5
        )
        return Response(resp.content, status=resp.status_code,
                        content_type=resp.headers.get("Content-Type", "application/json"))
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Service temporarily unavailable"}), 503


@app.route("/api/courses/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/api/courses/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def courses_proxy(path):
    return proxy(f"{COURSE_SVC}/api/courses/{path}")


@app.route("/api/students/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/api/students/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def students_proxy(path):
    return proxy(f"{STUDENT_SVC}/api/students/{path}")


@app.route("/health")
def health():
    return jsonify({"gateway": "ok", "port": PORT})


if __name__ == "__main__":
    print(f"API Gateway running on port {PORT}")
    app.run(port=PORT, debug=True)
'''


if __name__ == "__main__":
    import os

    for folder, filename, content in [
        ("course_service",  "app.py", COURSE_SERVICE),
        ("student_service", "app.py", STUDENT_SERVICE),
        ("gateway",         "app.py", GATEWAY),
    ]:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "app.py"), "w") as f:
            f.write(content.strip())
        print(f"Created {folder}/app.py")

    with open("README.md", "w") as f:
        f.write(DECOMPOSITION_README)
    print("Created README.md")
    print("\nRun each service in a separate terminal:")
    print("  cd course_service  && python app.py")
    print("  cd student_service && python app.py")
    print("  cd gateway         && python app.py")
