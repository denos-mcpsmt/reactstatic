import { useState } from 'react';

function RegistrationPage() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        accountType: 'CUSTOMER' // Default to CUSTOMER
    });
    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                setMessage(`Registration successful! User ID: ${data.user_id}`);
                setFormData({ name: '', email: '', password: '', accountType: 'CUSTOMER' });
            } else {
                const errorData = await response.json();
                setMessage(`Registration failed: ${errorData.message}`);
            }
        } catch (error) {
            setMessage(`An error occurred: ${error.message}`);
        }
    };

    return (
        <div style={styles.container}>
            <h2>Register New User</h2>
            <form onSubmit={handleSubmit} style={styles.form}>
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Name"
                    required
                    style={styles.input}
                />
                <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Email"
                    required
                    style={styles.input}
                />
                <input
                    type="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Password"
                    required
                    style={styles.input}
                />
                <select
                    name="accountType"
                    value={formData.accountType}
                    onChange={handleChange}
                    style={styles.input}
                >
                    <option value="CUSTOMER">Customer</option>
                    <option value="EMPLOYEE">Employee</option>
                    <option value="MANAGER">Manager</option>
                </select>
                <button type="submit" style={styles.button}>Register</button>
            </form>
            {message && <p style={styles.message}>{message}</p>}
        </div>
    );
}

const styles = {
    container: {
        maxWidth: '400px',
        margin: '0 auto',
        padding: '20px',
        textAlign: 'center',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
    input: {
        width: '100%',
        padding: '10px',
        margin: '10px 0',
        borderRadius: '5px',
        border: '1px solid #ddd',
    },
    button: {
        width: '100%',
        padding: '10px',
        margin: '10px 0',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
    },
    message: {
        marginTop: '20px',
        padding: '10px',
        backgroundColor: '#f0f0f0',
        borderRadius: '5px',
    }
};

export default RegistrationPage;