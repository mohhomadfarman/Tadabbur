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
            to="/admin"
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

const route  = useRoute()
const router = useRouter()
const auth   = useAuthStore()

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
  if (section === 'curriculum') return p.startsWith('/admin/tracks') || p.startsWith('/admin/subjects') || p.startsWith('/admin/lessons')
  if (section === 'library')    return p.startsWith('/admin/library')
  if (section === 'users')      return p.startsWith('/admin/users')
  if (section === 'analytics')  return p.startsWith('/admin/analytics')
  if (section === 'roles')      return p.startsWith('/admin/roles')
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
