import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CoursesPage from './pages/CoursesPage';
import CourseDetailPage from './pages/CourseDetailPage';
import ProfilePage from './pages/ProfilePage';
import { useEnrollment } from './EnrollmentContext';

export default function App() {
    const { enrolledCourses } = useEnrollment();

    return (
        <>
            <Header
                siteName="Student Portal"
                enrolledCount={enrolledCourses.length}
            />

            <main>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/courses" element={<CoursesPage />} />
                    <Route
                        path="/courses/:courseId"
                        element={<CourseDetailPage />}
                    />
                    <Route
                        path="/profile"
                        element={<ProfilePage />}
                    />
                </Routes>
            </main>

            <Footer />
        </>
    );
}
