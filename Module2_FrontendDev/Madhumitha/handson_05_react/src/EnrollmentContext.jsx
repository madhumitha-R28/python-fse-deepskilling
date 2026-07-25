import { createContext, useContext, useState } from 'react';

const EnrollmentContext = createContext(null);

export function EnrollmentProvider({ children }) {
    const [enrolledCourses, setEnrolledCourses] = useState([]);

    function enroll(course) {
        setEnrolledCourses(prev =>
            prev.find(c => c.id === course.id) ? prev : [...prev, course]
        );
    }

    function unenroll(courseId) {
        setEnrolledCourses(prev => prev.filter(c => c.id !== courseId));
    }

    return (
        <EnrollmentContext.Provider value={{ enrolledCourses, enroll, unenroll }}>
            {children}
        </EnrollmentContext.Provider>
    );
}

export const useEnrollment = () => useContext(EnrollmentContext);