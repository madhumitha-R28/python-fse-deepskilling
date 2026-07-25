// ============================================================
// Digital Nurture 5.0 | Frontend HO3 | data.js
// ES6 Module — Course Data Export (Step 29)
//
// WHY A SEPARATE DATA MODULE:
// Separating data from logic is the first step toward the
// component architecture you'll use in React/Angular/Vue.
// In React this becomes a service or a JSON import.
// The 'export const' syntax makes this an ES6 module —
// the browser treats it as isolated scope, no global leaks.
// ============================================================

export const courses = [
    {
        id:      1,
        name:    'Data Structures & Algorithms',
        code:    'CS101',
        credits: 4,
        grade:   'A'
    },
    {
        id:      2,
        name:    'Database Management Systems',
        code:    'CS102',
        credits: 3,
        grade:   'B'
    },
    {
        id:      3,
        name:    'Object Oriented Programming',
        code:    'CS103',
        credits: 4,
        grade:   'A'
    },
    {
        id:      4,
        name:    'Web Development Fundamentals',
        code:    'CS104',
        credits: 3,
        grade:   'B'
    },
    {
        id:      5,
        name:    'Python for Data Science',
        code:    'CS105',
        credits: 4,
        grade:   'A'
    }
];
