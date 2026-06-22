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
