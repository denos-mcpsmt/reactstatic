import { Link } from 'react-router-dom';

function Navbar() {
    return (
        <nav style={styles.nav}>
            <ul style={styles.navList}>
                <li><Link to="/" style={styles.navItem}>Home</Link></li>
                <li><Link to="/about" style={styles.navItem}>About</Link></li>
                <li><Link to="/login" style={styles.navItem}>Login</Link></li>
                <li><Link to="/courses" style={styles.navItem}>Courses</Link></li>

            </ul>
        </nav>
    );
}

const styles = {
    nav: {
        backgroundColor: '#333',
        padding: '1rem',
        width: '100%',
    },
    navList: {
        listStyle: 'none',
        display: 'flex',
        justifyContent: 'center',
        margin: 0,
        padding: 0,
    },
    navItem: {
        color: 'white',
        textDecoration: 'none',
        padding: '0 1rem',
    },
};

export default Navbar;