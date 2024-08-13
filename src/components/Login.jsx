// LoginPage.jsx
import { useState } from 'react';

const LoginPage = () => {
    const [credentials, setCredentials] = useState({ email: '', password: '' });

    const handleChange = (e) => {
        setCredentials({
            ...credentials,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle login via API
        fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(credentials),
        })
            .then(response => {
                if (response.ok) {
                    // Redirect or set authentication state
                }
            });
    };

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" value={credentials.email} onChange={handleChange} placeholder="Email" />
                <input type="password" name="password" value={credentials.password} onChange={handleChange} placeholder="Password" />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;
