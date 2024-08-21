import {useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';

function CourseCreatePage() {
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        teacherName: '',
    });
    const [teachers, setTeachers] = useState([]);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTeachers = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/users?account_type=EMPLOYEE');
                const data = await response.json();
                setTeachers(data);
            } catch (error) {
                console.error('Error fetching teachers:', error);
            }
        };

        fetchTeachers();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/api/course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                setMessage(`Course created successfully. Course ID: ${data.course_id}`);
                setFormData({ title: '', description: '', teacherName: '' });
                setTimeout(() => {
                    navigate('/courses');
                }, 2000);
            } else {
                const errorData = await response.json();
                setMessage(`Course creation failed: ${errorData.message}`);
            }
        } catch (error) {
            setMessage(`An error occurred: ${error.message}`);
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.title}>Create a New Course</h1>
            <form onSubmit={handleSubmit} style={styles.form}>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Title:</label>
                    <input
                        type="text"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                        style={styles.input}
                    />
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Description:</label>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        required
                        style={styles.textarea}
                    ></textarea>
                </div>
                <div style={styles.formGroup}>
                    <label style={styles.label}>Teacher:</label>
                    <select
                        name="teacherName"
                        value={formData.teacherName}
                        onChange={handleChange}
                        required
                        style={styles.select}
                    >
                        <option value="">Select a teacher</option>
                        {teachers.map((teacher) => (
                            <option key={teacher.id} value={teacher.name}>
                                {teacher.name}
                            </option>
                        ))}
                    </select>
                </div>
                <button type="submit" style={styles.button}>
                    Create Course
                </button>
            </form>
            {message && <p style={styles.message}>{message}</p>}
        </div>
    );
}

const styles = {
    container: {
        maxWidth: '600px',
        margin: '0 auto',
        padding: '2rem',
        backgroundColor: '#f8f8f8',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        borderRadius: '8px',
    },
    title: {
        textAlign: 'center',
        marginBottom: '2rem',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
    },
    formGroup: {
        marginBottom: '1.5rem',
    },
    label: {
        display: 'block',
        fontWeight: 'bold',
        marginBottom: '0.5rem',
    },
    input: {
        width: '100%',
        padding: '0.75rem',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
    textarea: {
        width: '100%',
        padding: '0.75rem',
        border: '1px solid #ccc',
        borderRadius: '4px',
        resize: 'vertical',
    },
    button: {
        backgroundColor: '#007bff',
        color: '#fff',
        padding: '0.75rem 1.5rem',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        '&:hover': {
            backgroundColor: '#0056b3',
        },
    },
    message: {
        marginTop: '1rem',
        padding: '0.75rem',
        backgroundColor: '#f0f0f0',
        borderRadius: '4px',
        textAlign: 'center',
    },
    select: {
        width: '100%',
        padding: '0.75rem',
        border: '1px solid #ccc',
        borderRadius: '4px',
    },
};

export default CourseCreatePage;