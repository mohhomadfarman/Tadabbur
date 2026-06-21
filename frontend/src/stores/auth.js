import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import { useProgressStore } from '@/stores/progress'

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

  async function login(email, password) {
    const response = await authApi.login(email, password)
    token.value = response.access
    refreshToken.value = response.refresh
    user.value = response.user
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
  }

  async function register(email, username, password, fullName) {
    const response = await authApi.register(email, username, password, fullName)
    token.value = response.access
    refreshToken.value = response.refresh
    user.value = response.user
    localStorage.setItem('access_token', response.access)
    localStorage.setItem('refresh_token', response.refresh)
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
  }

  return {
    user, token, isLoggedIn, isAdmin, isAuthor,
    login, register, logout, fetchUser,
  }
})
