function About() {
    return (
        <div style={styles.container}>
            <h1>About Me</h1>
            <p>Hi, Im a web developer passionate about creating awesome websites!</p>
        </div>
    );
}
const styles = {
    container: {
        padding: '2rem',
        textAlign: 'center',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
    },
};

export default About;