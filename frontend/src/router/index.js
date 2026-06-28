import { useAuthStore } from '@/stores/auth'

// vite-ssg creates the router (and chooses history mode) itself, so this module
// only exports the route table + a guard installer. See main.js.
export const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guestOnly: true, noindex: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { guestOnly: true, noindex: true },
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
    meta: { requiresAuth: true, noindex: true },
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

  // Videos — restricted to roles with the 'videos' section (admins/content
  // roles). Students and the public are redirected away; kept out of indexes.
  {
    path: '/videos',
    name: 'videos',
    component: () => import('@/views/videos/VideosView.vue'),
    meta: { requiresSection: 'videos', noindex: true },
  },
  {
    path: '/videos/:id',
    name: 'video',
    component: () => import('@/views/videos/VideoView.vue'),
    meta: { requiresSection: 'videos', noindex: true },
  },

  // Live launch registration — standalone full-bleed page (own chrome), indexable
  {
    path: '/launch',
    name: 'launch',
    component: () => import('@/views/launch/LaunchView.vue'),
    meta: { fullScreen: true },
  },

  // Legal (public, indexable)
  {
    path: '/privacy',
    name: 'privacy',
    component: () => import('@/views/legal/PrivacyView.vue'),
  },
  {
    path: '/terms',
    name: 'terms',
    component: () => import('@/views/legal/TermsView.vue'),
  },

  // Admin panel (all wrapped in AdminLayout). Parent requires *some* admin
  // access; each child names the section it needs (meta.section) so the guard
  // can gate per-role. Overview has no section — any admin user can see it.
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { requiresAdminAccess: true, fullScreen: true, noindex: true },
    children: [
      { path: '',                     name: 'admin',              component: () => import('@/views/admin/AdminDashboardView.vue') },
      { path: 'tracks/new',          name: 'admin-track-new',    meta: { section: 'curriculum' }, component: () => import('@/views/admin/TrackEditorView.vue') },
      { path: 'tracks/:slug/edit',   name: 'admin-track-edit',   meta: { section: 'curriculum' }, component: () => import('@/views/admin/TrackEditorView.vue') },
      { path: 'tracks/:slug',        name: 'admin-track-detail', meta: { section: 'curriculum' }, component: () => import('@/views/admin/AdminTrackDetailView.vue') },
      { path: 'subjects/new',    name: 'admin-subject-new',  meta: { section: 'curriculum' }, component: () => import('@/views/admin/SubjectEditorView.vue') },
      { path: 'subjects/:slug',  name: 'admin-subject-edit', meta: { section: 'curriculum' }, component: () => import('@/views/admin/SubjectEditorView.vue') },
      { path: 'lessons/new',   name: 'admin-lesson-new',  meta: { section: 'curriculum' }, component: () => import('@/views/admin/LessonEditorView.vue') },
      { path: 'lessons/:slug', name: 'admin-lesson-edit', meta: { section: 'curriculum' }, component: () => import('@/views/admin/LessonEditorView.vue') },
      { path: 'library',       name: 'admin-library',     meta: { section: 'library' },    component: () => import('@/views/admin/AdminLibraryView.vue') },
      { path: 'library/new',   name: 'admin-book-new',    meta: { section: 'library' },    component: () => import('@/views/admin/AdminBookEditorView.vue') },
      { path: 'library/:slug', name: 'admin-book-edit',   meta: { section: 'library' },    component: () => import('@/views/admin/AdminBookEditorView.vue') },
      { path: 'analytics',     name: 'admin-analytics',   meta: { section: 'analytics' },  component: () => import('@/views/admin/AdminAnalyticsView.vue') },
      { path: 'users',         name: 'admin-users',       meta: { section: 'users' },      component: () => import('@/views/admin/AdminUsersView.vue') },
      { path: 'users/:id',     name: 'admin-user-detail', meta: { section: 'users' },      component: () => import('@/views/admin/AdminUserDetailView.vue') },
      { path: 'roles',         name: 'admin-roles',       meta: { section: 'roles' },      component: () => import('@/views/admin/AdminRolesView.vue') },
      { path: 'registrations', name: 'admin-registrations', meta: { section: 'registrations' }, component: () => import('@/views/admin/AdminRegistrationsView.vue') },
      { path: 'languages',     name: 'admin-translations', meta: { section: 'translations' }, component: () => import('@/views/admin/AdminTranslationsView.vue') },
      { path: 'announcements', name: 'admin-announcements', meta: { section: 'announcements' }, component: () => import('@/views/admin/AdminAnnouncementsView.vue') },
      { path: 'features',      name: 'admin-features',      meta: { section: 'features' },      component: () => import('@/views/admin/AdminFeatureFlagsView.vue') },
      { path: 'feedback',      name: 'admin-feedback',      meta: { section: 'feedback' },      component: () => import('@/views/admin/AdminFeedbackView.vue') },
      { path: 'badges',        name: 'admin-badges',        meta: { section: 'badges' },        component: () => import('@/views/admin/AdminBadgesView.vue') },
      { path: 'email/campaigns', name: 'admin-email-campaigns', meta: { section: 'email' }, component: () => import('@/views/admin/AdminEmailCampaignsView.vue') },
      { path: 'email/templates', name: 'admin-email-templates', meta: { section: 'email' }, component: () => import('@/views/admin/AdminEmailTemplatesView.vue') },
      { path: 'email/settings',  name: 'admin-email-settings',  meta: { section: 'email' }, component: () => import('@/views/admin/AdminEmailSettingsView.vue') },
    ],
  },
]

export const scrollBehavior = () => ({ top: 0 })

// Auth guards. Installed by main.js after Pinia is registered. During SSG
// prerender there is no auth state and we never want build-time redirects, so
// the guard is a no-op on the server.
export function setupRouterGuards(router) {
  router.beforeEach(async (to, _from, next) => {
    if (import.meta.env.SSR) return next()
    const auth = useAuthStore()

    // On a hard load/refresh of a gated route the token exists but the profile
    // (and its sections) isn't fetched yet — load it before deciding, so admin
    // refreshes resolve correctly instead of bouncing to home.
    if (auth.isLoggedIn && !auth.user &&
        (to.meta.requiresAdminAccess || to.meta.requiresAuth || to.meta.requiresSection)) {
      try { await auth.fetchUser() } catch { /* invalid token falls through to checks */ }
    }

    // Section-gated public routes (e.g. Videos is admin/content-roles only).
    // Students and logged-out visitors are sent home.
    if (to.meta.requiresSection && !auth.can(to.meta.requiresSection)) {
      return next({ name: 'home' })
    }

    if (to.meta.requiresAdminAccess) {
      if (!auth.isLoggedIn) return next({ name: 'login', query: { redirect: to.fullPath } })
      if (!auth.hasAdminAccess) return next({ name: 'home' })
      // Lacks the specific section for this child → send to the admin overview.
      if (to.meta.section && !auth.can(to.meta.section)) return next({ name: 'admin' })
    } else if (to.meta.requiresAuth && !auth.isLoggedIn) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    } else if (to.meta.guestOnly && auth.isLoggedIn) {
      return next({ name: 'dashboard' })
    }
    next()
  })
}
