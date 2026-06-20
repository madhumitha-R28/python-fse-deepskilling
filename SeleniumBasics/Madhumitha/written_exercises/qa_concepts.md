# QA Concepts, Functional Testing & Defect Lifecycle
## Hands-On 1 — Task 1: Map Testing Types to a Real System

**System under test:** Course Management API (Django/Flask/FastAPI — Course Management for a college system)

---

## 1. Test Cases by Testing Level

### Unit Testing
Tests a single function in isolation — no database, no network, no other components involved.

**Test case:** `validate_credits(value)` — a validation function used by the course serializer to check that `credits` is a positive integer between 1 and 6.
- Input: `credits = -2`
- Expected: function returns `False` (or raises `ValidationError`) — purely a function call and a return value, nothing else touched.

### Integration Testing
Tests two components working together — e.g., the API endpoint logic talking to the database.

**Test case:** Call the `POST /api/courses/` view function directly (via Django's test client or FastAPI's `TestClient`) with a valid payload, bypassing the live HTTP server, and verify that a `Course` row is actually written to the test database with the correct field values.
- This checks the *view ↔ ORM ↔ database* boundary specifically — not the full network stack, not authentication middleware.

### System Testing
Tests a full end-to-end flow — real HTTP request in, through every layer, to a real response out.

**Test case:** Send a real authenticated `POST /api/courses/` HTTP request (with JWT header, full JSON body) to a running test server. Verify: the response is `201 Created` with the correct course JSON, **and** a separate `GET /api/courses/{id}/` call confirms the course now exists. This exercises auth middleware → view → serializer → ORM → DB → serialization → response, as one continuous path.

### User Acceptance Testing (UAT)
Tests from the perspective of an actual end user — judged against the business workflow, not the API contract.

**Test case:** A college admin logs into the portal, opens "Add New Course," enters Course Name = "Advanced Algorithms", Code = "CS301", Credits = 4, Department = "Computer Science", clicks Submit, and confirms the course now appears in the course listing the admin sees on screen. The admin doesn't know or care what HTTP status code came back — they care that the course is now visibly there.

---

## 2. Functional vs Non-Functional Classification

| Test case | Classification | Why |
|---|---|---|
| Unit — `validate_credits` | Functional | Checks the function *does the right thing* |
| Integration — view + DB | Functional | Checks data *gets persisted correctly* |
| System — full POST flow | Functional | Checks the *feature works end to end* |
| UAT — admin adds a course | Functional | Checks the *user can accomplish their goal* |

**Non-functional example:**
**Performance test:** When 100 concurrent users send `POST /api/courses/` requests simultaneously, 95% of requests must complete within 500ms, and the API must not return any `500` errors under that load.

This doesn't ask "does it work" — it asks "how well does it work under pressure." Functional tests would all pass even if the API took 8 seconds per request; only a non-functional (performance) test catches that.

---

## 3. Black-Box vs White-Box Testing

**Black-box testing** is done without knowledge of the internal code — the tester only knows the inputs and the expected outputs (the API contract / requirements). You send `POST /api/courses/` with a payload and check the response status and body. You have no idea whether the view uses an `if/else` chain or a serializer to validate — you only judge it by what goes in and what comes out.

**White-box testing** is done *with* knowledge of the internal code — the tester (usually the developer) looks at `validate_credits()`'s actual source, sees every branch (`credits <= 0`, `credits is None`, `credits > 6`, `credits` valid), and writes a test for each branch specifically because they can see it exists in the code, even if it's not obvious from the API spec alone.

**Who does which:** QA testers typically perform black-box testing — they validate the system the same way a real consumer or client application would, through its public interface. Developers typically perform white-box testing — usually as unit tests — because they're the ones who can see (and therefore must cover) every internal code path.

---

## 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-001 | Create a course with valid data | User is authenticated with a valid JWT; department `id=1` ("Computer Science") exists | 1. Send `POST /api/courses/` with body `{"name": "Advanced Algorithms", "code": "CS301", "credits": 4, "department_id": 1}`<br>2. Inspect response | API returns `201 Created`; response body contains the new course with a generated `id`; `GET /api/courses/{id}/` confirms it now exists | | |
| TC-002 | Reject creation when a required field is missing | User is authenticated | 1. Send `POST /api/courses/` with body `{"name": "Advanced Algorithms", "credits": 4}` (missing `code`)<br>2. Inspect response | API returns `400 Bad Request`; response body indicates `code` is required; no course is created in the database | | |
| TC-003 | Reject creation of a duplicate course code | A course with `code = "CS101"` already exists | 1. Send `POST /api/courses/` with body `{"name": "Intro to Programming v2", "code": "CS101", "credits": 3, "department_id": 1}`<br>2. Inspect response | API returns `400 Bad Request` (or `409 Conflict`) due to the unique constraint on `code`; the original `CS101` course is unchanged | | |
