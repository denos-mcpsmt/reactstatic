// AssignTeachersPage.jsx
import { useState, useEffect } from 'react';

const AssignTeachersPage = ({ courseId }) => {
    const [teachers, setTeachers] = useState([]);
    const [selectedTeacher, setSelectedTeacher] = useState('');

    useEffect(() => {
        // Fetch available teachers
        fetch('/api/teachers')
            .then(response => response.json())
            .then(data => setTeachers(data));
    }, []);

    const handleAssign = () => {
        // Assign teacher to course via API
        fetch(`/api/courses/${courseId}/assign-teacher`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ teacherId: selectedTeacher }),
        });
    };

    return (
        <div>
            <h1>Assign Teacher to Course</h1>
            <select value={selectedTeacher} onChange={(e) => setSelectedTeacher(e.target.value)}>
                <option value="">Select a Teacher</option>
                {teachers.map(teacher => (
                    <option key={teacher.id} value={teacher.id}>{teacher.name}</option>
                ))}
            </select>
            <button onClick={handleAssign}>Assign</button>
        </div>
    );
};

export default AssignTeachersPage;
