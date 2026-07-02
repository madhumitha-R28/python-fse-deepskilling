// ============================================================
// Digital Nurture 5.0 | Database Integration | Hands-On 5
// MongoDB — Document Modelling, CRUD & Aggregation Pipeline
// Author: Madhumitha R
//
// HOW TO USE:
// Open MongoDB Compass → Connect to localhost
// → click "Mongosh" tab at the bottom → paste each section
// OR open CMD → type: mongosh → paste sections below
// ============================================================

// ============================================================
// TASK 1: CREATE DATABASE, COLLECTION & INSERT (Steps 60–64)
// ============================================================

use college_nosql

db.feedback.insertMany([
    {
        student_id:   1,
        course_code:  "CS101",
        semester:     "2022-ODD",
        rating:       5,
        comments:     "Excellent teaching. Concepts explained with real-world examples.",
        tags:         ["challenging", "well-structured", "good-examples"],
        submitted_at: new Date("2022-11-30T10:15:00Z"),
        attachments:  [{ filename: "notes.pdf", size_kb: 240 }]
    },
    {
        student_id:   2,
        course_code:  "CS101",
        semester:     "2022-ODD",
        rating:       4,
        comments:     "Good content. Assignments were tough but worthwhile.",
        tags:         ["challenging", "practical"],
        submitted_at: new Date("2022-11-28T09:00:00Z"),
        attachments:  [{ filename: "assignment1.pdf", size_kb: 150 }]
    },
    {
        student_id:   5,
        course_code:  "CS101",
        semester:     "2022-ODD",
        rating:       3,
        comments:     "Average pace. Could use more examples.",
        tags:         ["average-pace", "needs-improvement"],
        submitted_at: new Date("2022-11-29T14:30:00Z"),
        attachments:  []
    },
    {
        student_id:   1,
        course_code:  "CS102",
        semester:     "2022-ODD",
        rating:       5,
        comments:     "Best database course. SQL theory was crystal clear.",
        tags:         ["well-structured", "practical", "good-examples"],
        submitted_at: new Date("2022-11-30T11:00:00Z"),
        attachments:  [{ filename: "er_diagram.pdf", size_kb: 320 }]
    },
    {
        student_id:   2,
        course_code:  "CS102",
        semester:     "2022-ODD",
        rating:       4,
        comments:     "Enjoyed the normalization section the most.",
        tags:         ["well-structured", "theoretical"],
        submitted_at: new Date("2022-11-27T16:45:00Z")
        // Step 63: No 'attachments' field intentionally —
        // demonstrates MongoDB's schema-less flexibility.
        // In MySQL this column would exist as NULL on every row.
        // Here the field simply doesn't exist in this document.
    },
    {
        student_id:   3,
        course_code:  "CS103",
        semester:     "2022-ODD",
        rating:       4,
        comments:     "OOP concepts well illustrated with Python examples.",
        tags:         ["practical", "well-structured"],
        submitted_at: new Date("2022-11-26T10:00:00Z"),
        attachments:  [{ filename: "oop_notes.pdf", size_kb: 180 }]
    },
    {
        student_id:   6,
        course_code:  "CS101",
        semester:     "2021-EVEN",
        rating:       2,
        comments:     "Too fast-paced. Needed more time on each topic.",
        tags:         ["challenging", "fast-paced", "needs-improvement"],
        submitted_at: new Date("2022-05-20T08:30:00Z"),
        attachments:  []
    },
    {
        student_id:   8,
        course_code:  "CS102",
        semester:     "2021-EVEN",
        rating:       1,
        comments:     "Lab sessions were poorly organised.",
        tags:         ["disorganised", "needs-improvement"],
        submitted_at: new Date("2022-05-22T09:15:00Z"),
        attachments:  [{ filename: "complaint.pdf", size_kb: 45 }]
    },
    {
        student_id:   4,
        course_code:  "EC101",
        semester:     "2022-ODD",
        rating:       5,
        comments:     "Circuit theory fundamentals were very well taught.",
        tags:         ["well-structured", "good-examples", "recommended"],
        submitted_at: new Date("2022-11-25T13:00:00Z"),
        attachments:  [{ filename: "circuit_notes.pdf", size_kb: 410 }]
    },
    {
        student_id:   7,
        course_code:  "ME101",
        semester:     "2022-ODD",
        rating:       3,
        comments:     "Thermodynamics is inherently tough. Decent coverage.",
        tags:         ["challenging", "theoretical"],
        submitted_at: new Date("2022-11-24T15:30:00Z"),
        attachments:  []
    }
])

// Step 64: Verify — must return 10
db.feedback.countDocuments()


// ============================================================
// TASK 2: CRUD OPERATIONS (Steps 65–70)
// ============================================================

// Step 65: READ — rating = 5
// Simple equality filter. PyMongo equivalent:
// collection.find({"rating": 5})
db.feedback.find({ rating: 5 }).pretty()


// Step 66: READ — CS101 with tag 'challenging'
// MongoDB lets you query inside arrays by value directly.
// No $elemMatch needed for a simple "array contains X" check.
// $elemMatch is only needed when matching MULTIPLE conditions
// on the SAME array sub-document simultaneously.
db.feedback.find({
    course_code: "CS101",
    tags:        "challenging"
}).pretty()


// Step 67: READ — projection (only 3 fields, exclude _id)
// 1 = include, 0 = exclude. _id:0 must be explicit.
// This shapes the response — don't send fields you don't need.
db.feedback.find(
    {},
    { student_id: 1, course_code: 1, rating: 1, _id: 0 }
)


// Step 68: UPDATE — add needs_review:true where rating < 3
// $set adds/updates a field without touching the rest.
// $lt = less than. No ALTER TABLE needed — new field,
// only on matching documents.
db.feedback.updateMany(
    { rating: { $lt: 3 } },
    { $set: { needs_review: true } }
)
// Verify
db.feedback.find({ needs_review: true }, { student_id: 1, course_code: 1, rating: 1, needs_review: 1, _id: 0 })


// Step 69: UPDATE — push 'reviewed' into tags array
// $push appends to array without replacing it.
db.feedback.updateMany(
    { needs_review: true },
    { $push: { tags: "reviewed" } }
)
// Verify
db.feedback.find({ needs_review: true }, { tags: 1, _id: 0 })


// Step 70: DELETE — remove 2021-EVEN semester documents
// Always preview with find() before deleteMany()
db.feedback.find({ semester: "2021-EVEN" })
db.feedback.deleteMany({ semester: "2021-EVEN" })
// Verify: should now be 8
db.feedback.countDocuments()


// ============================================================
// TASK 3: AGGREGATION PIPELINE (Steps 71–74)
//
// Pipeline = series of stages, each transforms the documents.
// $match = WHERE (filter early, reduce documents downstream)
// $group = GROUP BY + aggregate functions
// $sort  = ORDER BY
// $project = SELECT with aliases and expressions
// $unwind = explode array into individual documents
// ============================================================

// Step 71–72: Average rating per course for 2022-ODD semester
db.feedback.aggregate([
    {
        $match: { semester: "2022-ODD" }  // filter first — cheaper
    },
    {
        $group: {
            _id:            "$course_code",
            avg_rating:     { $avg: "$rating" },
            feedback_count: { $sum: 1 }
        }
    },
    {
        $sort: { avg_rating: -1 }
    },
    {
        $project: {
            _id:             0,
            course_code:     "$_id",
            average_rating:  { $round: ["$avg_rating", 1] },
            feedback_count:  1
        }
    }
])


// Step 73: Tag frequency leaderboard using $unwind
// Before $unwind: { tags: ["challenging", "practical"] } = 1 doc
// After  $unwind: { tags: "challenging" } + { tags: "practical" } = 2 docs
// Then $group counts each individual tag.
// Equivalent SQL would need a separate tags table + JOIN.
db.feedback.aggregate([
    { $unwind: "$tags" },
    {
        $group: {
            _id:   "$tags",
            count: { $sum: 1 }
        }
    },
    { $sort: { count: -1 } },
    {
        $project: {
            _id:   0,
            tag:   "$_id",
            count: 1
        }
    }
])


// Step 74: Index on course_code + verify with explain()
// Without index: COLLSCAN (reads every document)
// With index:    IXSCAN  (jumps directly to matches)
db.feedback.createIndex({ course_code: 1 })

db.feedback.find({ course_code: "CS101" }).explain("executionStats")
// In the output look for:
// winningPlan.inputStage.stage = "IXSCAN"  ← index used ✅
// If it shows "COLLSCAN" the index wasn't used
