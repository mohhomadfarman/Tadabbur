<template>
  <div class="flex h-screen overflow-hidden bg-gray-50">

    <!-- Mobile top bar -->
    <div class="fixed top-0 left-0 right-0 z-30 flex items-center h-14 px-4 bg-[#0c0c0e] md:hidden">
      <button @click="sidebarOpen = true" class="p-2 rounded-lg text-white/60 hover:text-white hover:bg-white/10 transition-colors">
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 12h18M3 6h18M3 18h18"/>
        </svg>
      </button>
      <RouterLink to="/admin" class="ms-3 text-white font-bold text-sm tracking-wide">تدبّر <span class="text-white/40 font-normal">Admin</span></RouterLink>
    </div>

    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div v-if="sidebarOpen" class="fixed inset-0 z-40 bg-black/60 md:hidden" @click="sidebarOpen = false" />
    </Transition>

    <!-- Sidebar -->
    <Transition name="slide">
      <aside
        v-show="sidebarOpen || !isMobile"
        class="fixed md:static z-50 flex flex-col h-full w-60 shrink-0 bg-[#0c0c0e]"
        :class="{ 'hidden md:flex': !sidebarOpen && isMobile }"
      >
        <!-- Logo -->
        <div class="flex items-center h-16 px-5 border-b border-white/5 shrink-0">
          <RouterLink to="/admin" class="flex items-center gap-2" @click="sidebarOpen = false">
            <span class="text-white font-bold text-lg tracking-tight">تدبّر</span>
            <span class="text-white/30 text-sm font-normal">Admin</span>
          </RouterLink>
        </div>

        <!-- Nav -->
        <nav class="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
          <!-- Overview -->
          <RouterLink
            to="/admin"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('overview') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            Overview
          </RouterLink>

          <!-- Curriculum -->
          <RouterLink
            v-if="auth.can('curriculum')"
            :to="{ name: 'admin-curriculum' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('curriculum') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
            Curriculum
          </RouterLink>

          <!-- Library -->
          <RouterLink
            v-if="auth.can('library')"
            :to="{ name: 'admin-library' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('library') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
            </svg>
            Library
          </RouterLink>

          <!-- Users -->
          <RouterLink
            v-if="auth.can('users')"
            :to="{ name: 'admin-users' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('users') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            Users
          </RouterLink>

          <!-- Registrations -->
          <RouterLink
            v-if="auth.can('registrations')"
            :to="{ name: 'admin-registrations' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('registrations') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 7v10a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7M3 7l9 6 9-6M3 7l2-3h14l2 3"/>
            </svg>
            Registrations
          </RouterLink>

          <!-- Analytics -->
          <RouterLink
            v-if="auth.can('analytics')"
            :to="{ name: 'admin-analytics' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('analytics') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 20V10M12 20V4M6 20v-6"/>
            </svg>
            Analytics
          </RouterLink>

          <!-- Languages (AI translation) -->
          <RouterLink
            v-if="auth.can('translations')"
            :to="{ name: 'admin-translations' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('translations') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>
            </svg>
            Languages
          </RouterLink>

          <!-- Announcements (pop-up modals) -->
          <RouterLink
            v-if="auth.can('announcements')"
            :to="{ name: 'admin-announcements' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('announcements') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.1 2.18a9.93 9.93 0 0 1 3.8 0"/><path d="M5.6 4.6a10 10 0 0 1 12.8 0"/><path d="M3 9a14 14 0 0 1 18 0"/><path d="M12 18h.01"/><path d="M8.5 13.5a5 5 0 0 1 7 0"/>
            </svg>
            Announcements
          </RouterLink>

          <!-- Track Feedback -->
          <RouterLink
            v-if="auth.can('feedback')"
            :to="{ name: 'admin-feedback' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('feedback') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            Feedback
          </RouterLink>

          <!-- Badges & Rewards -->
          <RouterLink
            v-if="auth.can('badges')"
            :to="{ name: 'admin-badges' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('badges') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>
            </svg>
            Badges
          </RouterLink>

          <!-- Email Marketing (dark-launched behind its own flag) -->
          <RouterLink
            v-if="auth.can('email') && features.isEnabled('email_marketing')"
            :to="{ name: 'admin-email-campaigns' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('email-campaigns') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
            </svg>
            Email Campaigns
          </RouterLink>
          <RouterLink
            v-if="auth.can('email') && features.isEnabled('email_marketing')"
            :to="{ name: 'admin-email-templates' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('email-templates') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16v16H4z"/><path d="M4 9h16M9 9v11"/>
            </svg>
            Email Templates
          </RouterLink>
          <RouterLink
            v-if="auth.can('email') && features.isEnabled('email_marketing')"
            :to="{ name: 'admin-email-settings' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('email-settings') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
            </svg>
            Email Settings
          </RouterLink>

          <!-- Email Automation (dark-launched behind its own flag) -->
          <RouterLink
            v-if="auth.can('automations') && features.isEnabled('email_automation')"
            :to="{ name: 'admin-automations' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('automations') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
            Automation
          </RouterLink>

          <!-- Feature Flags -->
          <RouterLink
            v-if="auth.can('features')"
            :to="{ name: 'admin-features' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('features') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/>
            </svg>
            Feature Flags
          </RouterLink>

          <!-- Roles & Permissions -->
          <RouterLink
            v-if="auth.can('roles')"
            :to="{ name: 'admin-roles' }"
            class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors"
            :class="isActive('roles') ? 'bg-[#234ecc] text-white font-medium' : 'text-white/50 hover:text-white hover:bg-white/5'"
            @click="sidebarOpen = false"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>
            </svg>
            Roles
          </RouterLink>
        </nav>

        <!-- Divider -->
        <div class="mx-3 border-t border-white/5" />

        <!-- Bottom -->
        <div class="p-4 space-y-3 shrink-0">
          <RouterLink to="/" class="flex items-center gap-2 text-xs text-white/30 hover:text-white/60 transition-colors">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Back to site
          </RouterLink>
          <div v-if="auth.user" class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-full bg-[#234ecc]/30 flex items-center justify-center text-[#234ecc] text-xs font-bold shrink-0">
              {{ auth.user.full_name?.charAt(0)?.toUpperCase() || auth.user.email?.charAt(0)?.toUpperCase() }}
            </div>
            <div class="min-w-0">
              <p class="text-white/50 text-xs truncate">{{ auth.user.email }}</p>
              <p class="text-white/25 text-[11px] capitalize">{{ auth.user.role }}</p>
            </div>
          </div>
          <button @click="handleLogout" class="flex items-center gap-2 text-xs text-white/25 hover:text-red-400 transition-colors w-full">
            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            Sign out
          </button>
        </div>
      </aside>
    </Transition>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto bg-gray-50 pt-14 md:pt-0">
      <RouterView />
    </main>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFeaturesStore } from '@/stores/features'

const route    = useRoute()
const router   = useRouter()
const auth     = useAuthStore()
const features = useFeaturesStore()

const sidebarOpen = ref(false)
const isMobile    = ref(false)

function checkMobile() {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})
onUnmounted(() => window.removeEventListener('resize', checkMobile))

function isActive(section) {
  const p = route.path
  if (section === 'overview')   return p === '/admin'
  if (section === 'curriculum') return p.startsWith('/admin/curriculum') || p.startsWith('/admin/tracks') || p.startsWith('/admin/subjects') || p.startsWith('/admin/lessons')
  if (section === 'library')    return p.startsWith('/admin/library')
  if (section === 'users')      return p.startsWith('/admin/users')
  if (section === 'registrations') return p.startsWith('/admin/registrations')
  if (section === 'analytics')  return p.startsWith('/admin/analytics')
  if (section === 'roles')      return p.startsWith('/admin/roles')
  if (section === 'translations') return p.startsWith('/admin/languages')
  if (section === 'announcements') return p.startsWith('/admin/announcements')
  if (section === 'features')   return p.startsWith('/admin/features')
  if (section === 'feedback')   return p.startsWith('/admin/feedback')
  if (section === 'badges')     return p.startsWith('/admin/badges')
  if (section === 'email-campaigns') return p.startsWith('/admin/email/campaigns')
  if (section === 'email-templates') return p.startsWith('/admin/email/templates')
  if (section === 'email-settings')  return p.startsWith('/admin/email/settings')
  if (section === 'automations') return p.startsWith('/admin/automations')
  return false
}

function handleLogout() {
  auth.logout()
  router.push({ name: 'home' })
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-enter-active, .slide-leave-active { transition: transform 0.25s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>
