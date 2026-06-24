# SDLC vs TDLC — V-Model & Agile QA Integration
## Hands-On 2 — Task 1: V-Model Mapping

**System under test:** Course Management API (Django/Flask/FastAPI)

---

## 1. The V-Model Diagram

The V-Model shows development phases on the left side going down, and their corresponding testing phases on the right side going up. Coding sits at the bottom vertex connecting both sides. The key idea is that every development phase on the left has a corresponding test phase on the right — and the test plan for each right-side phase is written *during* its paired left-side phase, not after.

```
DEVELOPMENT (Left)                          TESTING (Right)
─────────────────────────────────────────────────────────────

Requirements Analysis  ◄──────────────────►  User Acceptance Testing
        │                                              │
        ▼                                              ▲
  System Design        ◄──────────────────►   System Testing
        │                                              │
        ▼                                              ▲
Architecture Design    ◄──────────────────►  Integration Testing
        │                                              │
        ▼                                              ▲
  Module Design        ◄──────────────────►    Unit Testing
        │                                              │
        └──────────────────► Coding ◄─────────────────┘
                           (Bottom vertex)
```

The horizontal arrows mean: the test plan/cases for each testing phase on the right are *prepared* during the corresponding development phase on the left, even though those tests are *executed* later.

---

## 2. SDLC Phase → Test Artifact Produced

| SDLC Phase (Left) | Corresponding Test Phase (Right) | Test Artifact Produced During This Development Phase |
|---|---|---|
| **Requirements Analysis** | User Acceptance Testing | **Acceptance Test Plan** — UAT scenarios are derived directly from business requirements. For the Course Management API: "Admin can create a course," "Student can enroll," "Login returns a token." These acceptance criteria are written at requirements time so both sides agree on what 'done' means. |
| **System Design** | System Testing | **System Test Plan** — End-to-end test scenarios covering the full request-to-response flow. For the Course Management API: complete API flow tests like "POST /api/enrollments/ correctly links a student to a course and is retrievable via GET." |
| **Architecture Design** | Integration Testing | **Integration Test Plan** — Tests focusing on component boundaries and interfaces. For the Course Management API: how the view layer talks to the ORM, how the ORM talks to the database, how JWT middleware interacts with the request pipeline. |
| **Module Design** | Unit Testing | **Unit Test Plan / Test Case Specifications** — Tests for individual functions and classes in isolation. For the Course Management API: test cases for `validate_credits()`, the serializer's `to_representation()` method, individual model `save()` logic. |
| **Coding** | (Execution begins here) | Developers write and run unit tests alongside code. The test artifacts from the phases above are now executed bottom-up as code is completed. |

---

## 3. Entry and Exit Criteria for Each Testing Level

### Unit Testing

| | Criteria |
|---|---|
| **Entry Criteria** | Individual module/function code is complete and peer-reviewed; unit test cases have been written and reviewed; a test environment with mocked dependencies is available. |
| **Exit Criteria** | All planned unit test cases executed; minimum 80% code coverage achieved; no open Critical or High defects; all test results documented. |

**Course Management API context:** Unit testing begins when the `validate_credits()` function, the `CourseSerializer`, and individual model methods are coded. It's considered done when every function has test coverage and no critical bugs remain in isolation.

---

### Integration Testing

| | Criteria |
|---|---|
| **Entry Criteria** | All modules that will be integrated are individually unit-tested and passing; integration test cases are written; a test database is provisioned and seeded with baseline data; the API server can be started in a test configuration. |
| **Exit Criteria** | All integration test cases executed; all component interfaces (view ↔ ORM ↔ DB) verified; no Critical defects open; integration test report produced. |

**Course Management API context:** Integration testing begins when the view, serializer, ORM model, and database are all built and unit-tested individually. The integration test checks that `POST /api/courses/` via the test client actually writes a row to the test database.

---

### System Testing

| | Criteria |
|---|---|
| **Entry Criteria** | All components are integrated and integration-tested; the full application stack is deployed in a staging environment that mirrors production; system test plan is approved; test data is prepared for all scenarios. |
| **Exit Criteria** | All planned system test cases executed against the full stack; all Critical and High defects resolved; performance benchmarks met (e.g., 95% of API responses under 500ms); system test report signed off by QA lead. |

**Course Management API context:** System testing begins when the complete API — all endpoints, middleware, auth, and database — is deployed to staging. It ends when all end-to-end scenarios (course CRUD, enrollment, authentication) pass reliably with no unresolved Critical/High defects.

---

### User Acceptance Testing (UAT)

| | Criteria |
|---|---|
| **Entry Criteria** | System testing is complete and signed off; no Critical defects are open; UAT environment is provisioned with production-like data; actual business stakeholders (college admins, instructors) are available and briefed; UAT test cases are approved by stakeholders. |
| **Exit Criteria** | All UAT scenarios executed by stakeholders; all business-critical scenarios pass; any remaining defects are accepted by stakeholders as known/deferred; formal UAT sign-off received from the product owner or business representative. |

**Course Management API context:** UAT begins when QA signs off on system testing. College admin staff execute real-world workflows — adding courses, enrolling students, generating reports — using the actual UI or Postman-style tooling, and confirm the system meets their real operational needs.

---

## 4. Two Early QA Engagement Points in the V-Model

The V-Model's most important lesson is that QA's value isn't limited to the right side. Two specific left-side engagement points matter most:

### Engagement Point 1: Requirements Analysis Phase

**What QA does here:** Reviews requirements for testability, ambiguity, and completeness *before any design or code begins*.

**Why it matters for the Course Management API:** Suppose the requirements document says: *"The API should handle many concurrent requests efficiently."* That sentence is untestable — "many" and "efficiently" have no measurable definition. QA catches this during requirements review and pushes back: *"Define 'many' as a specific concurrent user count, and 'efficiently' as a maximum response time at that load."* The resulting requirement becomes: *"The API must serve 100 concurrent requests with 95% of responses under 500ms."* Now it can be tested.

Catching this ambiguity at requirements time costs one conversation. Discovering it during system testing — when code has already been written to a vague spec — costs a redesign.

### Engagement Point 2: Architecture/Module Design Phase

**What QA does here:** Reviews the technical design to identify components that will be difficult to test, spots missing error handling in API contracts, and raises concerns about testability of the system's internal boundaries.

**Why it matters for the Course Management API:** If the architecture shows that the authentication layer and the course-creation logic are tightly coupled in a single function with no separation of concerns, a QA engineer can flag this at design time: *"This will be impossible to unit test the course logic without going through real auth — can we separate these?"* Raising this during design phase costs a design revision. Raising it after the code is shipped costs a refactor plus regression testing of everything that touched that function.

---

## Task 2: Agile QA and Shift-Left Testing

---

### 1. Three Problems with Waterfall Testing (Late Testing)

**Problem 1: Defects are discovered too late and are expensive to fix**

In Waterfall, testing starts only after the entire Course Management API is built — all 10 endpoints, auth, ORM, serializers. If a tester then discovers that the `POST /api/enrollments/` endpoint has a fundamental design flaw (e.g., it allows a student to enroll in the same course twice with no uniqueness check), the fix requires going back to the model layer, the serializer, the view, and possibly the database schema. Every layer built on top of that broken foundation needs retesting. The cost of fixing a defect found during system testing is estimated to be 10–100× more expensive than fixing the same defect if caught at the requirements or design stage.

**Problem 2: No feedback loop between developers and testers during development**

Since testers only receive the finished product, a misunderstanding in the requirements spec can silently propagate through the entire development cycle. For the Course Management API, suppose the requirements said "only admins can create courses" but the developer interpreted that as "only authenticated users" — a slightly different and less secure rule. In Waterfall, this misinterpretation is discovered at the end of the project during system testing, by which time the access control logic is baked into every endpoint's view, serializer, and permission class. In Agile, QA catches this in Sprint 1 before a single line of that logic is written.

**Problem 3: Testing is time-pressured and shortcuts are taken**

In Waterfall, if development overruns its timeline (which it almost always does), the testing window gets compressed — because the release date doesn't move. For the Course Management API, this means regression coverage gets sacrificed. Testers end up manually spot-checking happy paths for the most visible endpoints and skipping edge cases (empty payloads, boundary values for `credits`, cascading delete behaviour on enrollment when a course is removed). Defects from those skipped cases ship to production.

---

### 2. QA Engineer's Role in Each Agile Ceremony

**Sprint Planning**

The QA engineer's job in Sprint Planning is not to estimate development effort — it's to define what "done" means before any code is written.

For the Course Management API, when the team picks up the story *"As an admin, I want to create a course"*, the QA engineer asks: What happens if `code` is missing? What if the course code already exists? What's the maximum allowed length for `name`? Is `credits` validated as a positive integer? Can a non-admin user hit this endpoint? These questions produce the story's **acceptance criteria**, written in Given-When-Then format (see Section 4 below). Developers now know exactly what they're coding to, and QA knows exactly what they'll be testing. Ambiguity is killed before a single line is written.

**Daily Standup**

The QA engineer surfaces any **blocking issues** that are stopping test progress and flags items that are ready for testing today.

Example standups: *"I'm blocked on the `GET /api/enrollments/` test — the endpoint keeps returning 500 in the test environment even for valid requests. Dev, is the test DB seeded? I need that unblocked today or it delays the sprint."* Or: *"I've completed testing on `POST /api/courses/` — all 8 test cases pass including the duplicate code scenario. That story is ready for demo."* The standup keeps the testing pipeline visible and avoids the classic Waterfall problem where a feature sits "dev complete" for days before anyone tests it.

**Sprint Review (Demo)**

The QA engineer verifies that what's being demoed to stakeholders actually matches the acceptance criteria that were agreed in Sprint Planning — not just that it works in the happy path.

During the demo of the Course Management API's enrollment feature, the QA engineer watches and asks: *"Can we also see what happens when a student tries to enroll in a course that's already full?"* or *"Can we demo the authentication failure path — what does the API return if the JWT is expired?"* This keeps the demo honest and ensures stakeholders are signing off on the full feature, not just the happy path the developer prepared.

**Sprint Retrospective**

The QA engineer contributes **process improvement observations** — not blame, but systemic patterns.

Example retrospective inputs from QA: *"We found 3 bugs in `POST /api/courses/` during testing that could have been caught by a simple validator unit test — can we agree that all serializers get unit tests before they're marked dev-complete?"* Or: *"The test environment was unstable for 2 days this sprint because the seeding script was broken — can we add DB seeding to the definition of done for environment setup stories?"* These inputs close the loop and make the next sprint cheaper.

---

### 3. Four Shift-Left Practices Applied to the Course Management API

**Shift-Left Practice (a): Reviewing requirements for testability**

Instead of receiving a requirements document and only asking "can we build this?", QA reviews it simultaneously and asks "can we *test* this?"

Applied to the Course Management API: The requirement *"The API should handle courses with appropriate fields"* is not testable — what fields? What validation? QA flags this immediately: *"We need a complete field list with data types, required/optional status, and validation rules for each. Without that, we cannot write test cases."* The result is a revised, specific requirement: *"A course must have: `name` (string, required, max 200 chars), `code` (string, required, unique, max 10 chars), `credits` (integer, required, 1–6), `department_id` (FK, required)."* Now it's testable.

**Shift-Left Practice (b): Writing test cases before code — TDD/BDD**

In Test-Driven Development (TDD), the developer writes a failing unit test *first*, then writes the code that makes it pass. In BDD, the acceptance criteria written in Sprint Planning (Given-When-Then) become automated integration tests that are written before the feature is coded.

Applied to the Course Management API: Before writing the `POST /api/courses/` view, a developer using TDD writes: `test_create_course_with_missing_code_returns_400()`. The test fails (the view doesn't exist yet). Now they write the view to make it pass. This guarantees that validation logic is never an afterthought — it's in the test before it's in the code.

**Shift-Left Practice (c): Static code analysis**

Static analysis tools examine code for bugs, security issues, style violations, and complexity problems *without running the code* — so they can be run on every commit before any human tests anything.

Applied to the Course Management API: Integrate `flake8` (style) and `bandit` (security) into the GitHub Actions CI pipeline. Every push to the repository runs these tools automatically. `bandit` catches common Django/Flask security issues like hardcoded secrets or SQL injection risks before they ever reach a tester's environment. A developer gets feedback in 30 seconds rather than waiting for a QA cycle.

**Shift-Left Practice (d): API contract testing before integration**

An API contract defines exactly what a request and response look like — field names, types, required/optional status, status codes. Contract testing verifies that the API implementation matches the contract, independently of whether the frontend that consumes it is built yet.

Applied to the Course Management API: Write a `openapi.json` or `schema.yml` contract for `POST /api/courses/` before building the endpoint. Use a tool like `schemathesis` or `dredd` to automatically test every response the API produces against the contract on every commit. If the Backend team changes the response shape (e.g., renames `department_id` to `department`), the contract test fails immediately — before the Frontend team discovers their React app is broken because the field name changed underneath them.

---

### 4. Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** *"As a college admin, I want to create a new course, so that students can enroll in it."*

---

**Scenario 1: Happy path — successful course creation**

```gherkin
Feature: Course Management

  Scenario: Admin successfully creates a new course
    Given I am authenticated as a college admin with a valid JWT token
    And no course with code "CS301" exists in the system
    When I send a POST request to /api/courses/ with the following payload:
      | name                | code  | credits | department_id |
      | Advanced Algorithms | CS301 | 4       | 1             |
    Then the response status code should be 201
    And the response body should contain the created course with a generated id
    And a GET request to /api/courses/{id}/ should return the same course data
```

---

**Scenario 2: Failure — duplicate course code**

```gherkin
  Scenario: Admin attempts to create a course with a duplicate code
    Given I am authenticated as a college admin with a valid JWT token
    And a course with code "CS101" already exists in the system
    When I send a POST request to /api/courses/ with the following payload:
      | name                       | code  | credits | department_id |
      | Introduction to CS (Again) | CS101 | 3       | 1             |
    Then the response status code should be 400
    And the response body should contain an error message indicating that course code "CS101" already exists
    And no new course record should be created in the database
```

---

**Scenario 3: Failure — missing required fields**

```gherkin
  Scenario: Admin attempts to create a course without providing the course code
    Given I am authenticated as a college admin with a valid JWT token
    When I send a POST request to /api/courses/ with the following payload:
      | name                | credits | department_id |
      | Advanced Algorithms | 4       | 1             |
    Then the response status code should be 400
    And the response body should contain a validation error message for the "code" field
    And no course record should be created in the database
```
