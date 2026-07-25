export default function CourseCard({
    id,
    name,
    code,
    credits,
    grade,
    onEnroll
}) {
    return (
        <article
            style={{
                background: '#fff',
                border: '1px solid #d1dce8',
                borderRadius: 10,
                padding: 20,
                boxShadow: '0 2px 8px rgba(0,0,0,.08)'
            }}
        >
            <h3 style={{ color: '#0f3460', marginBottom: 8 }}>
                {name}
            </h3>

            <p style={{ color: '#4a5568', marginBottom: 12 }}>
                Code: {code}
            </p>

            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <span
                    style={{
                        background: '#e8f0fe',
                        color: '#0f3460',
                        padding: '3px 10px',
                        borderRadius: 12,
                        fontSize: '0.8rem',
                        fontWeight: 600
                    }}
                >
                    Credits: {credits}
                </span>

                <span
                    style={{
                        fontWeight: 700,
                        color: grade === 'A' ? '#155724' : '#004085'
                    }}
                >
                    Grade: {grade}
                </span>
            </div>

            {onEnroll && (
                <button
                    onClick={() =>
                        onEnroll({
                            id,
                            name,
                            code,
                            credits,
                            grade
                        })
                    }
                    style={{
                        marginTop: 12,
                        padding: '8px 16px',
                        background: '#0f3460',
                        color: '#fff',
                        border: 'none',
                        borderRadius: 6,
                        cursor: 'pointer',
                        width: '100%'
                    }}
                >
                    + Enroll
                </button>
            )}
        </article>
    );
}