import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/learn',
    name: 'curriculum',
    component: () => import('@/views/curriculum/CurriculumView.vue'),
  },
  {
    path: '/learn/:trackSlug',
    name: 'track',
    component: () => import('@/views/curriculum/TrackView.vue'),
  },
  {
    path: '/learn/:trackSlug/:subjectSlug',
    name: 'subject',
    component: () => import('@/views/curriculum/SubjectView.vue'),
  },
  {
    path: '/lesson/:lessonSlug',
    name: 'lesson',
    component: () => import('@/views/lessons/LessonView.vue'),
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/dashboard/DashboardView.vue'),
    meta: { requiresAuth: true },
  },

  // Library
  {
    path: '/library',
    name: 'library',
    component: () => import('@/views/library/LibraryView.vue'),
  },
  {
    path: '/library/:slug',
    name: 'book',
    component: () => import('@/views/library/BookView.vue'),
  },

  // Videos
  {
    path: '/videos',
    name: 'videos',
    component: () => import('@/views/videos/VideosView.vue'),
  },
  {
    path: '/videos/:id',
    name: 'video',
    component: () => import('@/views/videos/VideoView.vue'),
  },

  // Admin panel — authors/scholars/admins only (all wrapped in AdminLayout)
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAuthor: true, fullScreen: true },
    children: [
      { path: '',                     name: 'admin',              component: () => import('@/views/admin/AdminDashboardView.vue') },
      { path: 'tracks/new',          name: 'admin-track-new',    component: () => import('@/views/admin/TrackEditorView.vue') },
      { path: 'tracks/:slug/edit',   name: 'admin-track-edit',   component: () => import('@/views/admin/TrackEditorView.vue') },
      { path: 'tracks/:slug',        name: 'admin-track-detail', component: () => import('@/views/admin/AdminTrackDetailView.vue') },
      { path: 'subjects/new',    name: 'admin-subject-new',  component: () => import('@/views/admin/SubjectEditorView.vue') },
      { path: 'subjects/:slug',  name: 'admin-subject-edit', component: () => import('@/views/admin/SubjectEditorView.vue') },
      { path: 'lessons/new',   name: 'admin-lesson-new',  component: () => import('@/views/admin/LessonEditorView.vue') },
      { path: 'lessons/:slug', name: 'admin-lesson-edit', component: () => import('@/views/admin/LessonEditorView.vue') },
      { path: 'library',       name: 'admin-library',     component: () => import('@/views/admin/AdminLibraryView.vue') },
      { path: 'library/new',   name: 'admin-book-new',    component: () => import('@/views/admin/AdminBookEditorView.vue') },
      { path: 'library/:slug', name: 'admin-book-edit',   component: () => import('@/views/admin/AdminBookEditorView.vue') },
      { path: 'analytics',     name: 'admin-analytics',   component: () => import('@/views/admin/AdminAnalyticsView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuthor) {
    if (!auth.isLoggedIn) return next({ name: 'login', query: { redirect: to.fullPath } })
    if (!auth.isAuthor) return next({ name: 'home' })
  } else if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guestOnly && auth.isLoggedIn) {
    return next({ name: 'dashboard' })
  }
  next()
})

export default router
