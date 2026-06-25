<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex items-start justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Users</h1>
        <p class="text-gray-400 text-sm mt-0.5">Manage accounts, roles and access.</p>
      </div>
    </div>

    <!-- Action error banner -->
    <div v-if="actionError" class="bg-red-50 border border-red-200 text-red-700 px-5 py-3 rounded-xl text-sm mb-6 flex items-start justify-between gap-3">
      <span>{{ actionError }}</span>
      <button @click="actionError = ''" class="text-red-400 hover:text-red-600 shrink-0">✕</button>
    </div>

    <!-- Load error -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">
      {{ error }}
    </div>

    <!-- Toolbar -->
    <div v-if="!loading && users.length > 0" class="mb-6 flex flex-col lg:flex-row gap-3">
      <div class="relative flex-1">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-width="2" d="m21 21-4.35-4.35"/>
        </svg>
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Search by name, email or username…"
          class="w-full border border-gray-200 rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        />
      </div>
      <select v-model="roleFilter" class="border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
        <option value="">All roles</option>
        <option v-for="r in roleOptions" :key="r.name" :value="r.name">{{ r.label }}</option>
      </select>
      <select v-model="statusFilter" class="border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
        <option value="all">All status</option>
        <option value="active">Active</option>
        <option value="inactive">Deactivated</option>
      </select>
      <select v-model="sortBy" class="border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
        <option value="newest">Newest first</option>
        <option value="name">Name A–Z</option>
        <option value="lessons">Most lessons</option>
        <option value="streak">Longest streak</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-2 animate-pulse">
      <div v-for="n in 8" :key="n" class="bg-gray-100 rounded-xl h-14" />
    </div>

    <!-- Empty -->
    <div v-else-if="users.length === 0" class="py-24 text-center text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-2xl">
      No users found.
    </div>
    <div v-else-if="sorted.length === 0" class="py-20 text-center text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-2xl">
      No users match your filters.
    </div>

    <!-- Table -->
    <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 text-xs text-gray-400 uppercase tracking-wider">
            <th class="px-5 py-3 text-left font-medium">User</th>
            <th class="px-4 py-3 text-left font-medium">Role</th>
            <th class="px-4 py-3 text-center font-medium">Status</th>
            <th class="px-4 py-3 text-right font-medium hidden md:table-cell">Lessons</th>
            <th class="px-4 py-3 text-right font-medium hidden lg:table-cell">Streak</th>
            <th class="px-4 py-3 text-right font-medium hidden lg:table-cell">Last active</th>
            <th class="px-4 py-3 text-right font-medium w-px">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in paged" :key="u.id" class="border-b border-gray-50 last:border-0 hover:bg-gray-50/60 transition-colors">
            <!-- User -->
            <td class="px-5 py-3">
              <RouterLink :to="{ name: 'admin-user-detail', params: { id: u.id } }" class="flex items-center gap-3 group">
                <span class="w-8 h-8 rounded-full bg-[#234ecc]/15 text-[#234ecc] text-xs font-bold flex items-center justify-center shrink-0">
                  {{ (u.full_name || u.email).charAt(0).toUpperCase() }}
                </span>
                <span class="min-w-0">
                  <span class="block font-medium text-gray-800 truncate group-hover:text-[#234ecc] transition-colors">{{ u.full_name || u.username }}</span>
                  <span class="block text-xs text-gray-400 truncate">{{ u.email }}</span>
                </span>
              </RouterLink>
            </td>
            <!-- Role -->
            <td class="px-4 py-3">
              <select
                :value="u.role"
                @change="changeRole(u, $event.target.value)"
                class="border border-gray-200 rounded-lg px-2 py-1.5 text-xs bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 max-w-[10rem]"
              >
                <option v-for="r in roleOptions" :key="r.name" :value="r.name">{{ r.label }}</option>
                <option v-if="!roleOptions.some(r => r.name === u.role)" :value="u.role">{{ u.role }}</option>
              </select>
            </td>
            <!-- Status -->
            <td class="px-4 py-3 text-center">
              <button
                @click="toggleActive(u)"
                class="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full transition-colors"
                :class="u.is_active ? 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'"
                :title="u.is_active ? 'Click to deactivate' : 'Click to activate'"
              >
                <span class="w-1.5 h-1.5 rounded-full" :class="u.is_active ? 'bg-emerald-500' : 'bg-gray-400'" />
                {{ u.is_active ? 'Active' : 'Off' }}
              </button>
            </td>
            <td class="px-4 py-3 text-right text-gray-600 hidden md:table-cell">{{ u.lessons_completed }}</td>
            <td class="px-4 py-3 text-right text-gray-600 hidden lg:table-cell">{{ u.current_streak }}🔥</td>
            <td class="px-4 py-3 text-right text-gray-400 text-xs hidden lg:table-cell">{{ formatDate(u.last_activity || u.last_login) }}</td>
            <!-- Actions -->
            <td class="px-4 py-3">
              <div class="flex items-center justify-end gap-1">
                <button @click="passwordTarget = u" title="Reset password" class="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-[#234ecc] hover:bg-[#234ecc]/8 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                </button>
                <button @click="deleteTarget = u" title="Delete user" class="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && totalPages > 1" class="flex items-center justify-center gap-1.5 mt-6">
      <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"
        class="px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-40 disabled:cursor-not-allowed transition-colors">Prev</button>
      <span class="text-sm text-gray-500 px-2">Page {{ currentPage }} / {{ totalPages }}</span>
      <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"
        class="px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-40 disabled:cursor-not-allowed transition-colors">Next</button>
    </div>

    <!-- Reset password modal -->
    <div v-if="passwordTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="passwordTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Reset password</h3>
        <p class="text-sm text-gray-500 mb-4">Set a new password for <strong>{{ passwordTarget.email }}</strong>.</p>
        <input v-model="newPassword" type="text" placeholder="New password (min 8 chars)"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        <div class="flex gap-3">
          <button @click="passwordTarget = null; newPassword = ''" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="newPassword.length < 8 || saving" @click="doResetPassword"
            class="flex-1 px-4 py-2.5 bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Saving…' : 'Set password' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete user?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.email }}</strong> will be permanently removed. This cannot be undone.</p>
        <div class="flex gap-3">
          <button @click="deleteTarget = null" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="saving" @click="doDelete" class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const users = ref([])
const roles = ref([])
const loading = ref(true)
const error = ref('')
const actionError = ref('')
const saving = ref(false)

const passwordTarget = ref(null)
const newPassword = ref('')
const deleteTarget = ref(null)

const searchQuery  = ref('')
const roleFilter   = ref('')
const statusFilter = ref('all')
const sortBy       = ref('newest')
const currentPage  = ref(1)
const pageSize     = 15

const roleOptions = computed(() =>
  roles.value.length
    ? roles.value.map(r => ({ name: r.name, label: r.label || r.name }))
    : [...new Set(users.value.map(u => u.role))].map(n => ({ name: n, label: n }))
)

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return users.value.filter(u => {
    if (q && !`${u.full_name || ''} ${u.email} ${u.username}`.toLowerCase().includes(q)) return false
    if (roleFilter.value && u.role !== roleFilter.value) return false
    if (statusFilter.value === 'active' && !u.is_active) return false
    if (statusFilter.value === 'inactive' && u.is_active) return false
    return true
  })
})

const sorted = computed(() => {
  const arr = [...filtered.value]
  switch (sortBy.value) {
    case 'name':    return arr.sort((a, b) => (a.full_name || a.email).localeCompare(b.full_name || b.email))
    case 'lessons': return arr.sort((a, b) => b.lessons_completed - a.lessons_completed)
    case 'streak':  return arr.sort((a, b) => b.current_streak - a.current_streak)
    default:        return arr.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
  }
})

const totalPages = computed(() => Math.max(1, Math.ceil(sorted.value.length / pageSize)))
const paged = computed(() => sorted.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

watch([searchQuery, roleFilter, statusFilter, sortBy], () => { currentPage.value = 1 })
watch(totalPages, (tp) => { if (currentPage.value > tp) currentPage.value = tp })
function goToPage(p) { currentPage.value = Math.min(Math.max(1, p), totalPages.value) }

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return '—'
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

function apiError(e, fallback) {
  return e?.response?.data?.role || e?.response?.data?.is_active || e?.response?.data?.detail || fallback
}

async function changeRole(u, newRole) {
  if (newRole === u.role) return
  const prev = u.role
  u.role = newRole
  try {
    await adminApi.updateUser(u.id, { role: newRole })
  } catch (e) {
    u.role = prev
    actionError.value = apiError(e, 'Could not change role.')
  }
}

async function toggleActive(u) {
  const prev = u.is_active
  u.is_active = !prev
  try {
    await adminApi.updateUser(u.id, { is_active: u.is_active })
  } catch (e) {
    u.is_active = prev
    actionError.value = apiError(e, 'Could not change status.')
  }
}

async function doResetPassword() {
  saving.value = true
  try {
    await adminApi.setUserPassword(passwordTarget.value.id, newPassword.value)
    passwordTarget.value = null
    newPassword.value = ''
  } catch (e) {
    actionError.value = apiError(e, 'Could not set password.')
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  saving.value = true
  try {
    await adminApi.deleteUser(deleteTarget.value.id)
    users.value = users.value.filter(u => u.id !== deleteTarget.value.id)
    deleteTarget.value = null
  } catch (e) {
    actionError.value = apiError(e, 'Could not delete user.')
    deleteTarget.value = null
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    users.value = await adminApi.listUsers()
    try { roles.value = await adminApi.listRoles() } catch { /* role list optional */ }
  } catch {
    error.value = 'Could not load users. Make sure your account has Users access.'
  } finally {
    loading.value = false
  }
})
</script>
