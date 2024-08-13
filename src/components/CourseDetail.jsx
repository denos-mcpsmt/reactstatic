// CourseDetailPage.jsx
import { useState, useEffect } from 'react';

const CourseDetailPage = ({ courseId }) => {
    const [course, setCourse] = useState({});

    useEffect(() => {
        // Fetch course details
        fetch(`/api/courses/${courseId}`)
            .then(response => response.json())
            .then(data => setCourse(data));
    }, [courseId]);

    const handleChange = (e) => {
        setCourse({
            ...course,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Update course details via API
        fetch(`/api/courses/${courseId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(course),
        });
    };

    return (
        <div>
            <h1>Update Course</h1>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" value={course.name || ''} onChange={handleChange} placeholder="Course Name" />
                <textarea name="description" value={course.description || ''} onChange={handleChange} placeholder="Course Description" />
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default CourseDetailPage;
