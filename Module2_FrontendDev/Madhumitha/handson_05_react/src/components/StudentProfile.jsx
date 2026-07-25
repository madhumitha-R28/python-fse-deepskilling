// src/components/StudentProfile.jsx
// HO5 Task 3, Step 74 — local state form with controlled inputs
import { useState, useEffect } from 'react';

export default function StudentProfile() {
    const [form, setForm] = useState({ name: '', email: '', semester: '' });

    function handleChange(e) {
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
    }

    // Step 75: useEffect with dependency array
    // Runs whenever form changes — demonstrates dependency array concept
    useEffect(() => {
        console.log('Profile form updated:', form);
        // WHY DEPENDENCY ARRAY MATTERS:
        // [] empty array  → runs once after mount only (componentDidMount)
        // [form]          → runs after every form state change
        // no array        → runs after EVERY render — can cause infinite loops
        //                   if the effect itself triggers a state update
    }, [form]);

    return (
        <div style={{ padding: '40px 32px', maxWidth: 500, margin: '0 auto' }}>
            <h2>Student Profile</h2>
            <form onSubmit={e => { e.preventDefault(); console.log('Submitted:', form); }}>

                <label htmlFor="name" style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>
                    Full Name
                </label>
                <input
                    id="name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder="Enter your full name"
                    style={{ display: 'block', width: '100%', padding: '10px 14px',
                             marginBottom: 16, border: '1px solid #d1dce8', borderRadius: 6 }}
                />

                <label htmlFor="email" style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>
                    Email
                </label>
                <input
                    id="email"
                    name="email"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder="Enter your email"
                    style={{ display: 'block', width: '100%', padding: '10px 14px',
                             marginBottom: 16, border: '1px solid #d1dce8', borderRadius: 6 }}
                />

                <label htmlFor="semester" style={{ display: 'block', marginBottom: 4, fontWeight: 600 }}>
                    Semester (1–8)
                </label>
                <input
                    id="semester"
                    name="semester"
                    type="number"
                    min="1"
                    max="8"
                    value={form.semester}
                    onChange={handleChange}
                    style={{ display: 'block', width: '100%', padding: '10px 14px',
                             marginBottom: 20, border: '1px solid #d1dce8', borderRadius: 6 }}
                />

                <button
                    type="submit"
                    style={{ padding: '12px 28px', background: '#0f3460', color: '#fff',
                             border: 'none', borderRadius: 6, cursor: 'pointer', fontWeight: 600 }}
                >
                    Save Profile
                </button>
            </form>
        </div>
    );
}