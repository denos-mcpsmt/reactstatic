// CourseEnrollmentPage.jsx
import { useEffect, useState } from 'react';

const CourseEnrollmentPage = ({ courseId }) => {
    const [students, setStudents] = useState([]);

    useEffect(() => {
        // Fetch students enrolled in a course
        fetch(`/api/courses/${courseId}/students`)
            .then(response => response.json())
            .then(data => setStudents(data));
    }, [courseId]);

    return (
        <div>
            <h1>Enrolled Students</h1>
            <ul>
                {students.map(student => (
                    <li key={student.id}>{student.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default CourseEnrollmentPage;
