import { createRouter, createWebHistory } from 'vue-router';
import CoursesView from '../views/CoursesView.vue';
import ProfileView from '../views/ProfileView.vue';

const routes = [
  { path: '/',        component: CoursesView },
  { path: '/profile', component: ProfileView },
];

export default createRouter({ history: createWebHistory(), routes });