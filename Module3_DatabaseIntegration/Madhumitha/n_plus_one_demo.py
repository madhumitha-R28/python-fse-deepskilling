# ============================================================
# Digital Nurture 5.0 | Database Integration | Hands-On 4
# Task 3: The N+1 Problem — Demonstration and Fix
# Author: Madhumitha R
#
# WHY THIS MATTERS:
# The N+1 problem is the most common performance bug introduced
# by developers using ORMs (Django ORM, SQLAlchemy, etc.).
# It happens when you fetch N rows, then issue one extra query
# PER ROW to get related data — N+1 total queries instead of 1.
#
# In development with 10 rows: invisible (milliseconds).
# In production with 10,000 rows: catastrophic (30+ seconds,
# database CPU spikes, API timeouts, angry users).
#
# Django ORM equivalent of N+1 (what NOT to do):
#   enrollments = Enrollment.objects.all()        # 1 query
#   for e in enrollments:
#       print(e.student.first_name)               # N queries — lazy load!
#
# Django ORM fix (eager loading):
#   enrollments = Enrollment.objects.select_related('student', 'course').all()
#   # ↑ generates ONE JOIN query, not N+1
# ============================================================

import mysql.connector
import time

# ---- Database connection config ----
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'madhu@mysql',   # replace with your MySQL root password
    'database': 'college_db'
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# VERSION 1: N+1 PROBLEM
# 1 query to get all enrollments
# + 1 query PER enrollment to get the student's name
# = N+1 total queries
# ============================================================
def demo_n_plus_one():
    print("\n" + "="*60)
    print("VERSION 1: N+1 Problem")
    print("="*60)

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    query_count = 0
    start_time  = time.time()

    # Query 1: fetch all enrollments (1 query)
    cursor.execute("SELECT enrollment_id, student_id, course_id, grade FROM enrollments")
    enrollments = cursor.fetchall()
    query_count += 1

    results = []
    for enrollment in enrollments:
        # Query N: one extra query PER enrollment row to get student name
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s",
            (enrollment['student_id'],)
        )
        student = cursor.fetchone()
        query_count += 1

        results.append({
            'enrollment_id': enrollment['enrollment_id'],
            'student_name':  f"{student['first_name']} {student['last_name']}",
            'course_id':     enrollment['course_id'],
            'grade':         enrollment['grade']
        })

    elapsed = time.time() - start_time

    for row in results:
        print(f"  Enrollment {row['enrollment_id']}: {row['student_name']} | "
              f"Course {row['course_id']} | Grade: {row['grade']}")

    print(f"\n  Total queries executed : {query_count}")
    print(f"  Time elapsed           : {elapsed:.4f} seconds")
    print(f"\n  With 10,000 enrollments: {10000 + 1} queries instead of 1")
    print(f"  At 1ms per query      : {(10000 + 1) / 1000:.1f} seconds wasted")

    cursor.close()
    conn.close()
    return results


# ============================================================
# VERSION 2: THE FIX — Single JOIN Query
# 1 query with a JOIN fetches ALL data in one round-trip
# ============================================================
def demo_optimised():
    print("\n" + "="*60)
    print("VERSION 2: Optimised — Single JOIN Query")
    print("="*60)

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    query_count = 0
    start_time  = time.time()

    # Single query: JOIN brings student name alongside enrollment data
    cursor.execute("""
        SELECT
            e.enrollment_id,
            CONCAT(s.first_name, ' ', s.last_name) AS student_name,
            c.course_name,
            e.grade
        FROM   enrollments e
        JOIN   students s ON e.student_id = s.student_id
        JOIN   courses  c ON e.course_id  = c.course_id
        ORDER BY e.enrollment_id
    """)
    results = cursor.fetchall()
    query_count += 1

    elapsed = time.time() - start_time

    for row in results:
        print(f"  Enrollment {row['enrollment_id']}: {row['student_name']} | "
              f"{row['course_name']} | Grade: {row['grade']}")

    print(f"\n  Total queries executed : {query_count}")
    print(f"  Time elapsed           : {elapsed:.4f} seconds")
    print(f"\n  With 10,000 enrollments: still just 1 query")

    cursor.close()
    conn.close()
    return results


# ============================================================
# COMPARISON SUMMARY
# ============================================================
def compare():
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)

    conn   = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Count actual enrollments in DB
    cursor.execute("SELECT COUNT(*) AS total FROM enrollments")
    n = cursor.fetchone()['total']

    print(f"\n  Current enrollments in DB : {n}")
    print(f"\n  N+1 approach queries      : {n + 1}")
    print(f"  Optimised approach queries: 1")
    print(f"  Queries saved             : {n}")
    print(f"\n  Scaled to 10,000 rows     :")
    print(f"    N+1 → 10,001 queries    ≈ 10+ seconds")
    print(f"    JOIN →     1 query      ≈ 50ms")

    print("""
  Django ORM translation:
  ─────────────────────────────────────────────────────
  BAD  (N+1):
    enrollments = Enrollment.objects.all()
    for e in enrollments:
        print(e.student.first_name)  # lazy loads each student

  GOOD (eager loading):
    enrollments = Enrollment.objects.select_related(
        'student', 'course'
    ).all()
    for e in enrollments:
        print(e.student.first_name)  # already loaded, no extra query

  SQLAlchemy equivalent:
    session.query(Enrollment).options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    ).all()
    """)

    cursor.close()
    conn.close()


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("N+1 Problem Demonstration — college_db")
    print("Make sure college_db is running and populated first.")

    n_plus_one_results = demo_n_plus_one()
    optimised_results  = demo_optimised()
    compare()

    # Verify both approaches return the same data
    n1_names  = [r['student_name'] for r in n_plus_one_results]
    opt_names = [r['student_name'] for r in optimised_results]
    print("\n  Data consistency check:", "PASS ✅" if n1_names == opt_names else "MISMATCH ❌")
