
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
