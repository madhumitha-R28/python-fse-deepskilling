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