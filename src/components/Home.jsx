function Home() {
    return (
        <div style={styles.container}>
            <h1>Welcome to My Website</h1>
            <p>This is the landing page of my awesome website!</p>
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

export default Home;