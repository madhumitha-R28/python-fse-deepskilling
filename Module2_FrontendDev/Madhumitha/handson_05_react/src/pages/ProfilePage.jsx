import { useState } from 'react';
import { useEnrollment } from '../EnrollmentContext';
import StudentProfile from '../components/StudentProfile';
export default function ProfilePage() {
    const { enrolledCourses, unenroll } = useEnrollment();

    const [form, setForm] = useState({
        name: '',
        email: '',
        semester: ''
    });

    function handleChange(e) {
        setForm(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    }

    return (
        <div
            style={{
                padding: '40px 32px',
                maxWidth: 700,
                margin: '0 auto'
            }}
        >
            <h2>Student Profile</h2>

            {/* HO5 Step 74: form with controlled inputs */}

            <form style={{ marginBottom: 40 }}>

                <label htmlFor="name">Full Name</label>

                <input
                    id="name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    style={{
                        display: 'block',
                        width: '100%',
                        padding: 10,
                        margin: '6px 0 16px',
                        border: '1px solid #d1dce8',
                        borderRadius: 6
                    }}
                />

                <label htmlFor="email">Email</label>

                <input
                    id="email"
                    name="email"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    style={{
                        display: 'block',
                        width: '100%',
                        padding: 10,
                        margin: '6px 0 16px',
                        border: '1px solid #d1dce8',
                        borderRadius: 6
                    }}
                />

                <label htmlFor="semester">Semester</label>

                <input
                    id="semester"
                    name="semester"
                    type="number"
                    value={form.semester}
                    onChange={handleChange}
                    style={{
                        display: 'block',
                        width: '100%',
                        padding: 10,
                        margin: '6px 0 16px',
                        border: '1px solid #d1dce8',
                        borderRadius: 6
                    }}
                />
            </form>

            <h3>
                Enrolled Courses ({enrolledCourses.length})
            </h3>

            {enrolledCourses.length === 0 && (
                <p>No courses enrolled yet.</p>
            )}

            {enrolledCourses.map(course => (
                <div
                    key={course.id}
                    style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: 12,
                        background: '#fff',
                        border: '1px solid #d1dce8',
                        borderRadius: 8,
                        marginBottom: 10
                    }}
                >
                    <span>
                        {course.name} ({course.code})
                    </span>

                    <button
                        onClick={() => unenroll(course.id)}
                        style={{
                            background: '#c0392b',
                            color: '#fff',
                            border: 'none',
                            borderRadius: 4,
                            padding: '4px 12px',
                            cursor: 'pointer'
                        }}
                    >
                        Remove
                    </button>
                </div>
            ))}
        </div>
    );
}