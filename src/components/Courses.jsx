// CourseListPage.jsx
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const CourseListPage = () => {
    const [courses, setCourses] = useState([]);

    useEffect(() => {
        // Fetch courses from an API
        fetch('/api/courses')
            .then(response => response.json())
            .then(data => setCourses(data));
    }, []);

    return (
        <div>
            <h1>Courses</h1>
            <ul>
                {courses.map(course => (
                    <li key={course.id}>
                        <Link to={`/courses/${course.id}`}>{course.name}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CourseListPage;
