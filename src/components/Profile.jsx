// UserProfilePage.jsx
import { useState, useEffect } from 'react';

const UserProfilePage = ({ userId }) => {
    const [user, setUser] = useState({});

    useEffect(() => {
        // Fetch user profile data
        fetch(`/api/users/${userId}`)
            .then(response => response.json())
            .then(data => setUser(data));
    }, [userId]);

    const handleChange = (e) => {
        setUser({
            ...user,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Update user profile via API
        fetch(`/api/users/${userId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user),
        });
    };

    return (
        <div>
            <h1>Update Profile</h1>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" value={user.name || ''} onChange={handleChange} placeholder="Name" />
                <input type="email" name="email" value={user.email || ''} onChange={handleChange} placeholder="Email" />
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default UserProfilePage;
