import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import About from './components/About';
import CourseListPage from './components/Courses';
import CourseCreatePage from './components/CourseCreate';
import UserEnrollmentPage from './components/Enrollments';
import CourseEnrollmentPage from './components/CourseEnrollments';
import UserProfilePage from './components/Profile';
import CourseDetailPage from './components/CourseDetail';
import AssignTeachersPage from './components/AssignTeacher';
import LoginPage from './components/Login';
import './App.css';
import RegistrationPage from "./components/Registration"; // We'll create this file for global styles

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <main className="content">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/about" element={<About />} />
                        <Route path="/login" element={<LoginPage />} />
                        <Route path="/registration" element={<RegistrationPage />} />
                        <Route path="/courses/:courseId/edit" element={<CourseDetailPage />} />
                        <Route path="/courses" element={<CourseListPage />} />
                        <Route path="/coursecreate" element={<CourseCreatePage />} />
                        <Route path="/courses/:courseId" element={<CourseEnrollmentPage />} />
                        <Route path="/user/:userId/enrollments" element={<UserEnrollmentPage />} />
                        <Route path="/user/:userId/profile" element={<UserProfilePage />} />
                        <Route path="/courses/:courseId/assign-teacher" element={<AssignTeachersPage />} />
                        <Route path="/user/:userId/enrollments" element={<UserEnrollmentPage />} />
                        <Route path="/user/:userId/profile" element={<UserProfilePage />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App;