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