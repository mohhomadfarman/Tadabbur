import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { useProgressStore } from '@/stores/progress'
import { useFeaturesStore } from '@/stores/features'
import { useBadgesStore } from '@/stores/badges'

// No localStorage during SSG prerender — the store starts logged-out on the
// server and rehydrates from localStorage on the client.
const isClient = typeof window !== 'undefined'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(isClient ? localStorage.getItem('access_token') : null)
  const refreshToken = ref(isClient ? localStorage.getItem('refresh_token') : null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isAuthor = computed(() => ['author', 'scholar', 'admin'].includes(user.value?.role))

  // Per-section access, resolved server-side from the user's role. `can()` gates
  // admin nav items and route access; `hasAdminAccess` = holds at least one section.
  const sections = computed(() => user.value?.sections || [])
  const can = (section) => sections.value.includes(section)
  const hasAdminAccess = computed(() => sections.value.length > 0)

  async function login(email, password) {
    const response = await authApi.login(email, password)
    token.value = response.access
    refreshToken.value = response.refresh
    user.value = response.user
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    // Re-resolve feature flags for the now-authenticated user (beta cohorts).
    useFeaturesStore().loadFlags()
  }

  async function register(email, username, password, fullName) {
    const response = await authApi.register(email, username, password, fullName)
    token.value = response.access
    refreshToken.value = response.refresh
    user.value = response.user
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
    useFeaturesStore().loadFlags()
  }

  async function fetchUser() {
    const data = await authApi.getProfile()
    user.value = data
  }

  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    useProgressStore().reset()
    useBadgesStore().reset()
    // Drop personalized flags, then reload anonymous defaults.
    const features = useFeaturesStore()
    features.reset()
    features.loadFlags()
  }

  return {
    user, token, isLoggedIn, isAdmin, isAuthor,
    sections, can, hasAdminAccess,
    login, register, logout, fetchUser,
  }
})
