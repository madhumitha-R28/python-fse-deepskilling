\# Cognizant Digital Nurture 5.0 Progress Log



\## Day 1 - Selenium Basics HO1 Task 1



Completed:

\- QA Concepts

\- Testing Levels

\- Functional vs Non-Functional Testing

\- Black Box vs White Box Testing

\- API Test Cases



Status: Completed

## Day 2 — Sun Jun 21, 2026

\*\*Track:\*\* Selenium HO1, Task 2 (Defect Lifecycle \& Severity Classification) — HO1 complete ✅



\*\*Time spent:\*\* \~40 min



\*\*What I did:\*\* Mapped the full defect lifecycle including Rejected/Deferred/Reopened paths,

classified severity and priority for 4 hypothetical API bugs, wrote a complete formal defect

report, explained severity vs priority with a worked example.



\*\*Takeaway:\*\* understood the lifecycle of defect like how a unreviewed defect is identified and fixed by developer and also learnt about the difference between priority and severity in testing. thus the 1st hands-on task in selenium has been completed by completing 2 tasks.those 2 tasks were about understanding the concept , no practical stuff.



\*\*Files:\*\* SeleniumBasics/Madhumitha/written\_exercises/qa\_concepts.md

## Day 3 — Mon Jun 22, 2026



\*\*Track:\*\* Selenium HO2, Task 1 (V-Model Mapping)



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Drew the V-Model with all phase mappings, documented the test artifact



produced during each development phase, defined entry/exit criteria for all 4 testing



levels, identified 2 early QA engagement points on the left side of the V-Model.



\*\*Takeaway:\*\* learnt about the process of v-model in which dev phase along with its corresponding test phase occurs simultaneously, though tests are executed later.which means only test plans are decided earlier during corresponding dev phase. then entry and exut criteria for each testing. then 2 engagement points of QA(quality assurance) in left dev phase.



\*\*Files:\*\* SeleniumBasics/Madhumitha/written\_exercises/v\_model\_analysis.md

## Day 4 — Tue Jun 23, 2026

\*\*Track:\*\* Selenium HO2, Task 2 (Agile QA \& Shift-Left) — HO2 complete ✅



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Described 3 waterfall testing problems, mapped QA's role in all 4 Agile

ceremonies, applied 4 Shift-Left practices to the Course Management API, wrote 3

Given-When-Then Gherkin scenarios for the course creation user story.



\*\*Takeaway:\*\* learnt about three problems with waterfall testing.qa engineer role in each agile ceremony , then about shift left practices and atlast 3 scenarios in integration testing.





\*\*Files:\*\* SeleniumBasics/Madhumitha/written\_exercises/v\_model\_analysis.md



\## Day 5 — Wed Jun 24, 2026



\*\*Track:\*\* Selenium HO3, Task 1 (Automation Decision \& ROI)



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Applied 5 automation criteria to POST /api/courses/, classified 6 test cases



as Automate/Manual with justifications, calculated automation break-even at 8 runs with



maintenance overhead analysis, explained flaky tests with 3 fix strategies.



\*\*Takeaway:\*\* learnt about 5 criterias to check for automation eligibility.automate vs manual.automation ROI calculation and flaky test.



\*\*Files:\*\* SeleniumBasics/Madhumitha/written\_exercises/automation\_strategy.md

## Day 6 — Thu Jun 25, 2026



\*\*Track:\*\* Selenium HO3, Task 2 (Framework Types) — HO3 complete ✅



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Compared all 5 automation framework types with advantages, disadvantages



and Course Management examples, recommended Hybrid for the team scenario with justification



for each requirement, described complete hybrid folder structure with design rationale.



\*\*Takeaway:\*\* learnt abt 5 different automation types



\*\*Files:\*\* SeleniumBasics/Madhumitha/written\_exercises/automation\_strategy.md



## Day 7 — Fri Jun 26, 2026



\*\*Track:\*\* Environment Setup (no submission file)



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Fixed MySQL and MongoDB PATH entries via Windows Environment Variables,

installed selenium/pytest/pytest-html/webdriver-manager, verified all tools from CMD.



\*\*Takeaway:\*\* PATH issues are silent failures — always verify with --version after install.



\*\*Files:\*\* None

## Day 8 — Sat Jun 27, 2026



\*\*Track:\*\* Database HO1 — Schema Design \& DDL ✅ Complete



\*\*Time spent:\*\* \~50 min



\*\*What I did:\*\* Created college\_db with all 5 tables and FK constraints, documented

1NF/2NF/3NF analysis as SQL comments, ran all ALTER TABLE operations, inserted all

sample data. All 17 statements executed with 0 errors in MySQL 9.7.



\*\*Takeaway:\*\* One thing to absorb today: the creation order. departments must come before students, courses, professors — and enrollments must come last because it references both students and courses. Getting FK order wrong is the most common first-day SQL mistake and MySQL will throw errno: 150 if you try to reference a table that doesn't exist yet. You'll never forget this after seeing it fail once.



\*\*Files:\*\* Module3\_DatabaseIntegration/Madhumitha/hands\_on\_1.sql

## Day 9 — Sun Jun 28, 2026



\*\*Track:\*\* Frontend HO1, Tasks 1 \& 2 — HO1 complete ✅



\*\*Time spent:\*\* \~45 min



\*\*What I did:\*\* Built Student Portal skeleton with proper semantic elements

(header/nav/main/section/article/footer), applied CSS3 reset, flex header,

hero with hover button, course cards with box-shadow and border-radius.

Validated HTML at W3C validator — zero errors.



\*\*Takeaway:\*\* The validator catches structural HTML mistakes a browser won't — browsers are too forgiving, they silently fix broken HTML and render it anyway. So visually everything looks fine, but the underlying structure is wrong. Screen readers, search engines, and automated testing tools don't fix it silently — they break. Validation is how you prove your HTML is structurally sound, not just visually okay.



\*\*Files:\*\* Module2\_FrontendDev/Madhumitha/handson\_01/index.html + styles.css


## Day 10 — Mon Jun 29, 2026



\*\*Track:\*\* Database HO2 — DML, Joins \& Aggregations ✅ Complete



\*\*Time spent:\*\* \~55 min



\*\*What I did:\*\* INSERT/UPDATE/DELETE with row count verification, 5 single-table 

queries with WHERE/ORDER BY/LIKE/GROUP BY, 5 join queries including LEFT JOIN + 

IS NULL pattern for missing relationships, 5 aggregation queries with COUNT/AVG/

ROUND and HAVING filter.



\*\*Takeaway:\*\* worked in MySQL



\*\*Files:\*\* Module3\_DatabaseIntegration/Madhumitha/hands\_on\_2.sql

