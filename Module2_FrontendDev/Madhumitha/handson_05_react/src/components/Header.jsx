import { Link } from 'react-router-dom';

export default function Header({ siteName, enrolledCount }) {
    return (
        <header
            style={{
                background: '#1a1a2e',
                color: '#fff',
                padding: '16px 32px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}
        >
            <div style={{ fontWeight: 'bold', fontSize: '1.4rem' }}>
                🎓 {siteName}
            </div>

            <nav>
                <Link
                    to="/"
                    style={{
                        color: '#c9d6e3',
                        marginRight: 20,
                        textDecoration: 'none'
                    }}
                >
                    Home
                </Link>

                <Link
                    to="/courses"
                    style={{
                        color: '#c9d6e3',
                        marginRight: 20,
                        textDecoration: 'none'
                    }}
                >
                    Courses
                </Link>

                <Link
                    to="/profile"
                    style={{
                        color: '#c9d6e3',
                        textDecoration: 'none'
                    }}
                >
                    Profile ({enrolledCount} enrolled)
                </Link>
            </nav>
        </header>
    );
}