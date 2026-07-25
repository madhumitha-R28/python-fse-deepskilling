import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CourseCard from '../components/CourseCard';
import { COURSES_DATA } from '../data/courses';
import { enroll, selectEnrolled } from '../enrollmentSlice';
import { useEnrollment } from '../EnrollmentContext';

export default function CoursesPage() {
    const [courses, setCourses] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const { enroll: contextEnroll } = useEnrollment();
    const dispatch = useDispatch();

    // HO5 Task 3, Step 71: useEffect to fetch on mount
    useEffect(() => {
        setLoading(true);

        // Using local data with simulated delay
        setTimeout(() => {
            setCourses(COURSES_DATA);
            setLoading(false);
        }, 800);
    }, []);

    // HO5 Task 3, Step 75: log on courses change
    useEffect(() => {
        console.log('Courses updated:', courses.length);

        // Empty array [] = run once (mount)
        // [courses] = run when courses changes.
        // Missing array = run every render.
    }, [courses]);

    const filteredCourses = courses.filter(course =>
        course.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    function handleEnroll(course) {
        contextEnroll(course);
        dispatch(enroll(course));
    }

    if (loading)
        return (
            <div style={{ padding: 40, textAlign: 'center' }}>
                ⏳ Loading courses...
            </div>
        );

    if (error)
        return (
            <div style={{ padding: 40, color: 'red' }}>
                Error: {error}
            </div>
        );

    return (
        <div
            style={{
                padding: '40px 32px',
                maxWidth: 1100,
                margin: '0 auto'
            }}
        >
            <h2 style={{ marginBottom: 20 }}>Enrolled Courses</h2>

            <input
                type="text"
                placeholder="Search courses..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                style={{
                    width: '100%',
                    maxWidth: 400,
                    padding: '10px 14px',
                    marginBottom: 20,
                    border: '1px solid #d1dce8',
                    borderRadius: 6,
                    fontSize: '1rem'
                }}
            />

            <p
                role="status"
                aria-live="polite"
                style={{
                    marginBottom: 12,
                    fontSize: '0.9rem',
                    color: '#4a5568'
                }}
            >
                {filteredCourses.length} course
                {filteredCourses.length !== 1 ? 's' : ''} found
            </p>

            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns:
                        'repeat(auto-fit, minmax(280px, 1fr))',
                    gap: 20
                }}
            >
                {filteredCourses.map(course => (
                    <CourseCard
                        key={course.id}
                        {...course}
                        onEnroll={handleEnroll}
                    />
                ))}
            </div>
        </div>
    );
}