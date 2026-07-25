// ============================================================
// Digital Nurture 5.0 | Frontend HO3 | app.js
// JavaScript ES6+ & DOM Manipulation
// Author: Madhumitha R
//
// WHAT THIS FILE DOES:
// 1. Imports course data from data.js (ES6 module)
// 2. Demonstrates ES6+ syntax: destructuring, map, filter, reduce
// 3. Dynamically renders course cards into the DOM
// 4. Adds search filtering and sort-by-credits interactivity
// 5. Uses event delegation for card click handling
// ============================================================


// Step 30: ES6 named import — pulls 'courses' from data.js
// This only works because index.html loads app.js as type="module"
import { courses } from './data.js';


// ============================================================
// TASK 1: ES6+ SYNTAX PRACTICE (Steps 30–34)
// ============================================================

// Step 30: Destructuring in a loop
// Instead of course.name and course.credits separately,
// destructure directly in the for...of parameter
console.log('--- Step 30: Destructuring ---');
for (const { name, credits, code } of courses) {
    console.log(`${code}: ${name} — ${credits} credits`);
}

// Step 31: Array.map() — transform array into formatted strings
// map() returns a NEW array, never mutates the original.
// Arrow function syntax: (param) => expression
const formattedCourses = courses.map(
    ({ code, name, credits }) => `${code} — ${name} (${credits} credits)`
);
console.log('\n--- Step 31: map() formatted strings ---');
console.log(formattedCourses);

// Step 32: Array.filter() — get only courses with credits >= 4
// filter() returns a new array of elements where callback returns true
const heavyCourses = courses.filter(course => course.credits >= 4);
console.log('\n--- Step 32: filter() courses with 4+ credits ---');
console.log(`Count: ${heavyCourses.length}`);
console.log(heavyCourses.map(c => c.name));

// Step 33: Array.reduce() — sum all credits
// reduce(callback, initialValue)
// accumulator starts at 0, adds each course's credits
const totalCredits = courses.reduce((acc, course) => acc + course.credits, 0);
console.log('\n--- Step 33: reduce() total credits ---');
console.log(`Total credits enrolled: ${totalCredits}`);

// Step 34: Arrow function + template literal
// Before (traditional for loop):
// for (let i = 0; i < courses.length; i++) {
//     console.log('Course: ' + courses[i].name);
// }
//
// After (arrow function + template literal):
console.log('\n--- Step 34: Arrow function + template literal ---');
courses.forEach(course => {
    console.log(`Course: ${course.name} | Grade: ${course.grade}`);
});


// ============================================================
// TASK 2: DOM RENDERING (Steps 35–39)
// ============================================================

// Working copy of courses — we'll sort/filter this, not 'courses'
// Spread operator creates a shallow copy so original stays intact
let displayCourses = [...courses];

// Step 36: Select the grid container
const courseGrid     = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const selectedCourseEl = document.getElementById('selected-course');

// Step 37–38: Create and append course cards
// WHY DocumentFragment (mentioned in hint):
// Appending directly to the DOM N times triggers N reflows.
// A DocumentFragment is an in-memory DOM node — you build the
// entire card list in memory, then append once → 1 reflow.
function renderCourses(courseList) {
    // Step 44 prep: clear existing cards before re-rendering
    // Always clear before re-render to prevent duplicate cards
    courseGrid.innerHTML = '';

    const fragment = document.createDocumentFragment();

    courseList.forEach(course => {
        // Step 37: createElement — same as what React does under the hood
        const article = document.createElement('article');
        article.className = 'course-card';
        article.dataset.id = course.id;  // store id for event delegation

        // Template literal builds the inner HTML in one readable block
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Course Code: <strong>${course.code}</strong></p>
            <div class="card-footer">
                <span class="credits">Credits: ${course.credits}</span>
                <span class="grade grade-${course.grade}">Grade: ${course.grade}</span>
            </div>
        `;

        fragment.appendChild(article);
    });

    // Step 38: Single DOM append — all cards inserted in one operation
    courseGrid.appendChild(fragment);

    // Step 39: Update total credits dynamically
    const currentTotal = courseList.reduce((acc, c) => acc + c.credits, 0);
    totalCreditsEl.textContent = `Total Credits: ${currentTotal} of ${totalCredits} enrolled`;
}

// Initial render on page load
renderCourses(displayCourses);


// ============================================================
// TASK 3: EVENT LISTENERS & INTERACTIVITY (Steps 40–44)
// ============================================================

// Step 40–41: Search input — live filtering
// 'input' event fires on every keystroke, not just on blur/submit.
// This is what makes search feel instant.
const searchInput = document.getElementById('search-courses');

searchInput.addEventListener('input', (event) => {
    const query = event.target.value.toLowerCase().trim();

    // filter() the original courses array (not displayCourses)
    // so searching after sorting still works correctly
    displayCourses = courses.filter(course =>
        course.name.toLowerCase().includes(query) ||
        course.code.toLowerCase().includes(query)
    );

    renderCourses(displayCourses);
});


// Step 42: Sort by credits button
// Descending sort: if b.credits > a.credits, b comes first (returns positive)
const sortBtn = document.getElementById('sort-credits');

sortBtn.addEventListener('click', () => {
    displayCourses = [...displayCourses].sort((a, b) => b.credits - a.credits);
    renderCourses(displayCourses);
});


// Step 43–44: Event delegation on the grid container
// WHY event delegation:
// If we attached a click listener to each card individually,
// dynamically added cards (after search/sort re-render) wouldn't
// have listeners — they didn't exist when the listeners were attached.
// Instead, attach ONE listener to the parent container.
// event.target is whatever was actually clicked (could be h3, p, span).
// closest('.course-card') walks UP the DOM tree to find the card ancestor.
courseGrid.addEventListener('click', (event) => {
    // closest() returns null if no matching ancestor found
    const card = event.target.closest('.course-card');
    if (!card) return;  // clicked outside a card (gap between cards)

    const courseId = parseInt(card.dataset.id);
    const course   = courses.find(c => c.id === courseId);

    if (course) {
        selectedCourseEl.textContent =
            `Selected: ${course.name} (${course.code}) — Grade: ${course.grade} — Credits: ${course.credits}`;
        selectedCourseEl.classList.add('active');
    }
});
