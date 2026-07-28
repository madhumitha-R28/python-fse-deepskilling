# 🎓 Python Full Stack Engineer — Deep Skilling Portfolio
**Digital Nurture 5.0 | Cognizant Technology Solutions**

| | |
|---|---|
| **Candidate** | Madhumitha R |
| **Program** | DN 5.0 — Python Full Stack Engineer Deep Skilling |
| **Institution** | RIT Chennai — CSE 2023 |
| **Completion Date** | July 28, 2026 |
| **GitHub** | [@madhumitha-R28](https://github.com/madhumitha-R28) |

---

## 📦 Repository Structure

| Track | Folder | Hands-On | Status |
|---|---|---|---|
| QA & Selenium | `SeleniumBasics/Madhumitha/` | HO1–7 | ✅ Complete |
| Database Integration | `Module3_DatabaseIntegration/Madhumitha/` | HO1–7 | ✅ Complete |
| Python Backend Frameworks | `PythonBackendFrameworks/Madhumitha/` | HO1–10 | ✅ Complete |
| Frontend Development | `Module2_FrontendDev/Madhumitha/` | HO1–10 | ✅ Complete |

**Total: 34 hands-on exercises across 4 tracks**

---

## 🛠️ Tech Stack

**Backend:** Python 3.10, Django 5.2 + DRF, Flask 3.1, FastAPI, SQLAlchemy, Alembic

**Frontend:** HTML5, CSS3, Vanilla JS (ES6+), React 18 (Redux Toolkit, React Router), Angular 19, Vue 3 (Pinia, Vue Router)

**Database:** MySQL 9.7, MongoDB 8.3, SQLite

**Testing:** Selenium 4, pytest, pytest-html, Page Object Model

**Auth:** JWT (python-jose), bcrypt (passlib)

**Tools:** Git, GitHub, VS Code, MySQL Workbench, MongoDB Compass, Postman

---

## 🗂️ Track Summaries

### QA & Selenium (`SeleniumBasics/Madhumitha/`)
- **HO1–3:** QA concepts, V-Model, Agile QA, Shift-Left, Gherkin, automation ROI, hybrid framework design
- **HO4:** WebDriver setup, headless Chrome, window/tab management, screenshots
- **HO5:** All 6 locator strategies, XPath/CSS selectors, explicit waits vs implicit waits vs FluentWait
- **HO6:** pytest fixtures, parametrize, conftest.py, pytest-html reports, screenshot on failure
- **HO7:** Page Object Model — BasePage, SimpleFormPage, CheckboxPage, DropdownPage, InputFormPage

### Database Integration (`Module3_DatabaseIntegration/Madhumitha/`)
- **HO1:** `college_db` schema — 5 tables, FK constraints, normalization (1NF/2NF/3NF), ALTER TABLE
- **HO2:** DML (INSERT/UPDATE/DELETE), single-table queries, INNER/LEFT JOINs, aggregations (COUNT/AVG/HAVING)
- **HO3:** Subqueries (correlated + non-correlated), views with WITH CHECK OPTION, stored procedures, transactions, SAVEPOINT
- **HO4:** B-Tree indexes, EXPLAIN plan (COLLSCAN → IXSCAN), N+1 problem demo + fix in Python
- **HO5:** MongoDB — feedback collection, CRUD, aggregation pipeline ($unwind, $group), index + explain
- **HO6:** SQLAlchemy ORM — 6 model classes, CRUD via session, joinedload (N+1 fix verified in echo output)
- **HO7:** Alembic migrations — baseline, incremental (is_active column, CourseSchedule table), rollback verified

### Python Backend Frameworks (`PythonBackendFrameworks/Madhumitha/`)
- **HO1–3:** Django 5.2 — models, migrations, admin, DRF serializers, APIView + ModelViewSet, DefaultRouter
- **HO4–5:** Flask — application factory pattern, blueprints, SQLAlchemy integration, JSON error handlers
- **HO6–7:** FastAPI — Pydantic schemas, async endpoints, dependency injection, background tasks, Swagger/OpenAPI
- **HO8:** REST best practices — PATCH, pagination (offset), status codes (201/204/400/404/503)
- **HO9:** JWT authentication — bcrypt password hashing, OAuth2PasswordBearer, register/login endpoints
- **HO10:** Microservices — CourseService (5001), StudentService (5002), API Gateway (5000), graceful 503 fallback

### Frontend Development (`Module2_FrontendDev/Madhumitha/`)
- **HO1:** Semantic HTML5 — header/nav/main/section/article/footer, W3C validated
- **HO2:** Flexbox (header + stats bar), CSS Grid (auto-fit/minmax), mobile-first media queries, clamp()
- **HO3:** ES6+ — destructuring, map/filter/reduce, DOM rendering with DocumentFragment, event delegation
- **HO4:** Fetch API, Promises, async/await, Promise.all, Axios with interceptors, error handling + retry
- **HO5–6:** React 18 — functional components, hooks (useState/useEffect), React Router, Context API, Redux Toolkit
- **HO7:** Angular 19 — standalone components, services, HttpClient, reactive forms, ngFor/ngIf, routing
- **HO8:** Vue 3 — Composition API, Pinia store, Vue Router, v-model, computed, onMounted
- **HO9:** WCAG accessibility — ARIA labels, aria-live, keyboard navigation, focus indicators, contrast ratios
- **HO10:** Advanced state — createAsyncThunk, Axios interceptors, error boundaries, framework comparison

---

## 🚀 Running the Projects

### Django API
```bash
cd PythonBackendFrameworks/Madhumitha/handson_01_django
python manage.py runserver
# http://127.0.0.1:8000/api/
```

### FastAPI
```bash
cd PythonBackendFrameworks/Madhumitha/handson_06_fastapi
uvicorn main:app --reload
# http://127.0.0.1:8000/docs
```

### Microservices
```bash
cd PythonBackendFrameworks/Madhumitha/handson_10_microservices
# Terminal 1:
cd course_service && python app.py
# Terminal 2:
cd student_service && python app.py
# Terminal 3:
cd gateway && python app.py
```

### React Portal
```bash
cd Module2_FrontendDev/Madhumitha/handson_05_react
npm install && npm run dev
# http://localhost:5173
```

### Angular Portal
```bash
cd Module2_FrontendDev/Madhumitha/handson_07_angular
ng serve
# http://localhost:4200
```

### Vue Portal
```bash
cd Module2_FrontendDev/Madhumitha/handson_08_vue
npm install && npm run dev
# http://localhost:5173
```

### Selenium Tests
```bash
cd SeleniumBasics/Madhumitha
pytest test_playground.py -v --html=report.html --self-contained-html
```

---

## 📈 Daily Progress

See [PROGRESS.md](./PROGRESS.md) for the full day-by-day learning log.