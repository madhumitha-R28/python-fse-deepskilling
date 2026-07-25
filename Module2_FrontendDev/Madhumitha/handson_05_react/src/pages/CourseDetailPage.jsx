import { useParams, useNavigate } from 'react-router-dom';
import { COURSES_DATA } from '../data/courses';
import { useEnrollment } from '../EnrollmentContext';

export default function CourseDetailPage() {
    const { courseId } = useParams();
    const navigate = useNavigate();

    const { enroll } = useEnrollment();

    const course = COURSES_DATA.find(
        c => c.id === parseInt(courseId)
    );

    if (!course)
        return (
            <div style={{ padding: 40 }}>
                Course not found
            </div>
        );

    function handleEnroll() {
        enroll(course);
        navigate('/profile');
    }

    return (
        <div
            style={{
                padding: '60px 32px',
                maxWidth: 600,
                margin: '0 auto'
            }}
        >
            <h2>{course.name}</h2>

            <p>Code: {course.code}</p>
            <p>Credits: {course.credits}</p>
            <p>Grade: {course.grade}</p>

            <button
                onClick={handleEnroll}
                style={{
                    marginTop: 20,
                    padding: '12px 28px',
                    background: '#0f3460',
                    color: '#fff',
                    border: 'none',
                    borderRadius: 6,
                    cursor: 'pointer'
                }}
            >
                Enroll in this Course
            </button>
        </div>
    );
}