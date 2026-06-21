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

---

## Task 2: Defect Lifecycle & Severity Classification

### 1. Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
                                    ↑         |
                                    └── Reopened ←┘  (fix didn't actually resolve it)

At triage, a defect can branch off the main path instead of proceeding to Assigned:
  → Rejected   (not reproducible, working as designed, duplicate, or invalid — no fix needed)
  → Deferred   (valid and reproducible, but consciously pushed to a future release)
```

- **New** — QA logs the defect; nobody has reviewed it yet.
- **Assigned** — Triaged and handed to a developer to investigate.
- **Open** — Developer has acknowledged it and is actively working on a fix.
- **Fixed** — Developer believes the issue is resolved and the fix is deployed to the test environment.
- **Retest** — QA re-runs the original failing steps against the fix.
- **Verified** — QA confirms the fix actually resolves the issue with no regressions.
- **Closed** — Lifecycle complete.
- **Reopened** — If Retest shows the fix didn't work (or broke something else), the defect goes back into the Assigned/Open cycle instead of moving to Verified.
- **Rejected** — Used when the report turns out not to be a real defect (can't reproduce, intended behavior, duplicate of an existing ticket, or invalid environment/user error).
- **Deferred** — Used when the defect is real and confirmed, but the team consciously decides to fix it in a later release rather than now (common for low severity/priority items near a deadline).

### 2. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| a) `POST /api/courses/` returns 500 for all requests | **Critical** | **P1** | The entire course-creation feature is completely unusable — not degraded, *dead*. Both axes are maxed because it's both severely broken and urgently needed by every dependent workflow. |
| b) Course names >150 chars silently truncated, no error | **Medium** | **P3** | Silent data loss is a genuine correctness bug (worse than a visible error, since nobody is alerted), but the trigger condition — a 150+ character course name — is rare in real usage, so it doesn't block normal operation. Fine to schedule into a regular sprint. |
| c) `/docs` Swagger page has a typo in the API description | **Low** | **P4** | Purely cosmetic/documentation. Zero impact on functionality, data, or any user's ability to use the system. Fix whenever convenient. |
| d) Login with correct credentials occasionally returns 401 (intermittent) | **High** | **P1/P2** | Authentication is core-path functionality, and *intermittent* failures are a red flag for a deeper systemic issue (race condition, token timing, cache inconsistency) rather than a simple logic bug. Hard-to-reproduce bugs like this tend to get prioritized urgently precisely because they're unpredictable and erode user trust — you can't tell a user "just try logging in again" as an acceptable answer. |

### 3. Defect Report — Bug (a)

| Field | Value |
|---|---|
| **Defect ID** | DEF-2026-001 |
| **Title** | `POST /api/courses/` returns 500 Internal Server Error for all requests |
| **Environment** | Staging / QA Test Environment |
| **Build Version** | v1.2.0-rc1 |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Authenticate as an admin user and obtain a valid JWT token.<br>2. Send `POST /api/courses/` with a valid payload: `{"name": "Intro to Python", "code": "CS101", "credits": 3, "department_id": 1}`, including header `Authorization: Bearer <token>`.<br>3. Submit the request. |
| **Expected Result** | API returns `201 Created` with the new course object in the response body. |
| **Actual Result** | API returns `500 Internal Server Error` for every attempt; no course record is created. |
| **Attachments** | screenshot of 500 error |

### 4. Severity vs Priority

**Severity** measures the *technical impact* of a defect on the system — how broken is it, objectively, from a functionality/data standpoint. **Priority** measures *business urgency* — how soon does this need to be fixed relative to everything else on the team's plate. They're independent axes that often correlate but don't have to.

**Example where High Severity ≠ High Priority:** A bug in the year-end financial report generator produces incorrect totals. That's **High Severity** — incorrect financial data is a serious data-integrity issue, full stop. But the report only runs once a year, and the next run isn't due for eleven months. There's no immediate user impact today, so it's reasonable to mark it **Low-to-Medium Priority** — scheduled into a normal upcoming sprint rather than treated as a drop-everything emergency, even though the underlying bug is severe.
