<template>
  <div style="padding:40px 32px; max-width:600px; margin:0 auto;">
    <h2>My Profile</h2>
    <p style="margin:12px 0;">Enrolled: {{ store.enrolledCourses.length }} courses |
       Total Credits: {{ store.totalCredits }}</p>
    <h3 style="margin-top:24px;">Enrolled Courses</h3>
    <p v-if="store.enrolledCourses.length === 0">No courses enrolled yet.</p>
    <div v-for="course in store.enrolledCourses" :key="course.id"
         style="display:flex; justify-content:space-between; align-items:center;
                padding:12px; background:#fff; border:1px solid #d1dce8;
                border-radius:8px; margin-bottom:10px;">
      <span>{{ course.name }} ({{ course.code }})</span>
      <button @click="store.unenroll(course.id)"
              style="background:#c0392b; color:#fff; border:none;
                     border-radius:4px; padding:4px 12px; cursor:pointer;">
        Remove
      </button>
    </div>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from '../stores/enrollment';
const store = useEnrollmentStore();
</script>