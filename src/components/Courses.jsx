import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function CourseListPage() {
    const [courses, setCourses] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/courses');
                const data = await response.json();
                setCourses(data);
            } catch (error) {
                console.error('Error fetching courses:', error);
            }
        };

        fetchCourses();
    }, []);

    const handleCreateCourse = () => {
        navigate('/coursecreate');
    };

    return (
        <div>
            <h1>Course List</h1>
            <ul>
                {courses.map((course) => (
                    <li key={course.id}>
                        <h3>{course.title}</h3>
                        <p>{course.description}</p>
                        <p>Teacher: {course.teacherName}</p>
                    </li>
                ))}
            </ul>
            <button onClick={handleCreateCourse}>Create Course</button>
        </div>
    );
}

export default CourseListPage;