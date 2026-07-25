import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// HO10: async thunk for fetching courses (Step 143)
export const fetchAllCourses = createAsyncThunk(
    'courses/fetchAll',
    async () => {
        const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
        const data = await res.json();
        return data.map((p, i) => ({
            id: p.id,
            name: p.title.slice(0, 40),
            code: `CS10${i + 1}`,
            credits: [3, 4, 3, 4, 4][i],
            grade: ['A', 'B', 'A', 'B', 'A'][i]
        }));
    }
);

const enrollmentSlice = createSlice({
    name: 'enrollment',
    initialState: {
        enrolledCourses: [],
        courses: [],
        loading: false,
        error: null
    },
    reducers: {
        enroll(state, action) {
            const exists = state.enrolledCourses.find(c => c.id === action.payload.id);
            if (!exists) state.enrolledCourses.push(action.payload);
        },
        unenroll(state, action) {
            state.enrolledCourses =
                state.enrolledCourses.filter(c => c.id !== action.payload);
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchAllCourses.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllCourses.fulfilled, (state, action) => {
                state.loading = false;
                state.courses = action.payload;
            })
            .addCase(fetchAllCourses.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message;
            });
    }
});

export const { enroll, unenroll } = enrollmentSlice.actions;

// Selectors (Step 146)
export const selectCourses = state => state.enrollment.courses;
export const selectEnrolled = state => state.enrollment.enrolledCourses;
export const selectCoursesLoading = state => state.enrollment.loading;
export const selectCoursesError = state => state.enrollment.error;

export default enrollmentSlice.reducer;