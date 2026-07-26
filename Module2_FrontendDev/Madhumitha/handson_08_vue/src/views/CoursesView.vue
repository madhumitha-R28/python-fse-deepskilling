<template>
  <div style="padding:40px 32px; max-width:1100px; margin:0 auto;">
    <h2>Enrolled Courses</h2>
    <input v-model="searchTerm" placeholder="Search courses..."
           style="width:100%; max-width:400px; padding:10px; margin:16px 0;
                  border:1px solid #d1dce8; border-radius:6px; font-size:1rem;" />
    <p role="status" aria-live="polite">{{ filteredCourses.length }} courses found</p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; margin-top:16px;">
      <div v-for="course in filteredCourses" :key="course.id"
           style="background:#fff; border:1px solid #d1dce8; border-radius:10px; padding:20px;">
        <h3 style="color:#0f3460; margin-bottom:8px;">{{ course.name }}</h3>
        <p style="color:#4a5568; margin-bottom:12px;">Code: {{ course.code }}</p>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="background:#e8f0fe; color:#0f3460; padding:3px 10px; border-radius:12px; font-size:0.8rem;">
            Credits: {{ course.credits }}
          </span>
          <span style="font-weight:700; color:#0f3460;">Grade: {{ course.grade }}</span>
        </div>
        <button @click="store.enroll(course)"
                style="width:100%; margin-top:12px; padding:8px; background:#0f3460;
                       color:#fff; border:none; border-radius:6px; cursor:pointer;">
          + Enroll
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useEnrollmentStore } from '../stores/enrollment';

const store      = useEnrollmentStore();
const searchTerm = ref('');
const courses    = ref([]);

const filteredCourses = computed(() =>
  courses.value.filter(c => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
);

onMounted(() => {
  courses.value = [
    { id:1, name:'Data Structures & Algorithms', code:'CS101', credits:4, grade:'A' },
    { id:2, name:'Database Management Systems',  code:'CS102', credits:3, grade:'B' },
    { id:3, name:'Object Oriented Programming',  code:'CS103', credits:4, grade:'A' },
    { id:4, name:'Web Development Fundamentals', code:'CS104', credits:3, grade:'B' },
    { id:5, name:'Python for Data Science',      code:'CS105', credits:4, grade:'A' },
  ];
});
</script>