<template>
  <nav style="background:#1a1a2e; padding:16px 32px; display:flex; gap:24px;">
    <RouterLink to="/"        style="color:#c9d6e3; text-decoration:none;">Courses</RouterLink>
    <RouterLink to="/profile" style="color:#c9d6e3; text-decoration:none;">Profile</RouterLink>
  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>