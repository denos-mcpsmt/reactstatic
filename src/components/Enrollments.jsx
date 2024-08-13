// UserEnrollmentPage.jsx
import { useEffect, useState } from 'react';

const UserEnrollmentPage = ({ userId }) => {
    const [enrollments, setEnrollments] = useState([]);

    useEffect(() => {
        // Fetch user enrollments from an API
        fetch(`/api/users/${userId}/enrollments`)
            .then(response => response.json())
            .then(data => setEnrollments(data));
    }, [userId]);

    return (
        <div>
            <h1>My Enrollments</h1>
            <ul>
                {enrollments.map(enrollment => (
                    <li key={enrollment.id}>{enrollment.courseName}</li>
                ))}
            </ul>
        </div>
    );
};

export default UserEnrollmentPage;
