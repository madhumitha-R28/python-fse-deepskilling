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