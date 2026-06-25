<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">

    <RouterLink :to="{ name: 'admin-users' }" class="inline-flex items-center gap-1.5 text-sm text-[#234ecc] hover:text-[#1a3ba8] mb-6 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
      Back to users
    </RouterLink>

    <div v-if="loading" class="space-y-4 animate-pulse">
      <div class="bg-gray-100 rounded-2xl h-28" />
      <div class="bg-gray-100 rounded-2xl h-40" />
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">{{ error }}</div>

    <template v-else-if="user">
      <div v-if="actionError" class="bg-red-50 border border-red-200 text-red-700 px-5 py-3 rounded-xl text-sm mb-5 flex items-start justify-between gap-3">
        <span>{{ actionError }}</span>
        <button @click="actionError = ''" class="text-red-400 hover:text-red-600 shrink-0">✕</button>
      </div>

      <!-- Profile header -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-5">
        <div class="flex items-start gap-4">
          <span class="w-14 h-14 rounded-2xl bg-[#234ecc]/15 text-[#234ecc] text-xl font-bold flex items-center justify-center shrink-0">
            {{ (user.full_name || user.email).charAt(0).toUpperCase() }}
          </span>
          <div class="min-w-0 flex-1">
            <h1 class="text-xl font-bold text-gray-900 truncate">{{ user.full_name || user.username }}</h1>
            <p class="text-gray-400 text-sm truncate">{{ user.email }} · @{{ user.username }}</p>
            <div class="flex flex-wrap items-center gap-2 mt-2 text-xs">
              <span class="px-2 py-0.5 rounded-full bg-[#234ecc]/10 text-[#234ecc] font-semibold capitalize">{{ user.role }}</span>
              <span class="px-2 py-0.5 rounded-full font-semibold" :class="user.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-gray-100 text-gray-500'">
                {{ user.is_active ? 'Active' : 'Deactivated' }}
              </span>
              <span class="text-gray-400">Joined {{ formatDate(user.created_at) }}</span>
              <span class="text-gray-400">· Last login {{ formatDate(user.last_login) }}</span>
            </div>
          </div>
        </div>

        <!-- Quick stats -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-5">
          <div class="bg-gray-50 rounded-xl px-4 py-3">
            <p class="text-2xl font-black text-gray-900">{{ user.lessons_completed }}</p>
            <p class="text-xs text-gray-400">Lessons done</p>
          </div>
          <div class="bg-gray-50 rounded-xl px-4 py-3">
            <p class="text-2xl font-black text-gray-900">{{ user.current_streak }}</p>
            <p class="text-xs text-gray-400">Current streak</p>
          </div>
          <div class="bg-gray-50 rounded-xl px-4 py-3">
            <p class="text-2xl font-black text-gray-900">{{ user.longest_streak }}</p>
            <p class="text-xs text-gray-400">Longest streak</p>
          </div>
          <div class="bg-gray-50 rounded-xl px-4 py-3">
            <p class="text-2xl font-black text-gray-900">{{ user.enrolled_tracks.length }}</p>
            <p class="text-xs text-gray-400">Enrolled tracks</p>
          </div>
        </div>
      </div>

      <!-- Management controls -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm mb-5">
        <h2 class="font-semibold text-gray-800 mb-4">Manage</h2>
        <div class="flex flex-wrap items-center gap-3">
          <label class="text-sm text-gray-500">Role
            <select :value="user.role" @change="changeRole($event.target.value)"
              class="ms-2 border border-gray-200 rounded-lg px-3 py-2 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
              <option v-for="r in roleOptions" :key="r.name" :value="r.name">{{ r.label }}</option>
              <option v-if="!roleOptions.some(r => r.name === user.role)" :value="user.role">{{ user.role }}</option>
            </select>
          </label>
          <button @click="toggleActive"
            class="text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
            :class="user.is_active ? 'bg-gray-100 text-gray-700 hover:bg-gray-200' : 'bg-emerald-500 text-white hover:bg-emerald-600'">
            {{ user.is_active ? 'Deactivate' : 'Activate' }}
          </button>
          <button @click="showPassword = true" class="text-sm font-semibold px-4 py-2 rounded-xl bg-[#234ecc] hover:bg-[#1a3ba8] text-white transition-colors">Reset password</button>
          <button @click="showDelete = true" class="text-sm font-semibold px-4 py-2 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 transition-colors ms-auto">Delete user</button>
        </div>
      </div>

      <div class="grid lg:grid-cols-2 gap-5">
        <!-- Per-track progress -->
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
          <h2 class="font-semibold text-gray-800 mb-4">Progress by track</h2>
          <div v-if="tracks.length === 0" class="text-sm text-gray-400 py-6 text-center">No completed lessons yet.</div>
          <ul v-else class="space-y-3">
            <li v-for="t in tracks" :key="t.track_slug" class="flex items-center justify-between text-sm">
              <span class="font-mono text-xs text-gray-600 truncate">{{ t.track_slug }}</span>
              <span class="text-gray-500">{{ t.completed_lessons }} lesson{{ t.completed_lessons === 1 ? '' : 's' }}</span>
            </li>
          </ul>
        </div>

        <!-- Activity timeline -->
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
          <h2 class="font-semibold text-gray-800 mb-4">Recent activity</h2>
          <div v-if="events.length === 0" class="text-sm text-gray-400 py-6 text-center">No activity recorded.</div>
          <ol v-else class="relative border-s border-gray-100 ms-2 space-y-4">
            <li v-for="(e, i) in events" :key="i" class="ms-4">
              <span class="absolute -start-1.5 w-3 h-3 rounded-full" :class="eventColor(e.type)" />
              <p class="text-sm text-gray-800">{{ eventLabel(e) }}</p>
              <p class="text-xs text-gray-400">{{ formatDateTime(e.at) }}</p>
            </li>
          </ol>
        </div>
      </div>
    </template>

    <!-- Reset password modal -->
    <div v-if="showPassword" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showPassword = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Reset password</h3>
        <p class="text-sm text-gray-500 mb-4">Set a new password for <strong>{{ user.email }}</strong>.</p>
        <input v-model="newPassword" type="text" placeholder="New password (min 8 chars)"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        <div class="flex gap-3">
          <button @click="showPassword = false; newPassword = ''" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="newPassword.length < 8 || saving" @click="doResetPassword"
            class="flex-1 px-4 py-2.5 bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Saving…' : 'Set password' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete modal -->
    <div v-if="showDelete" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showDelete = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete user?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ user.email }}</strong> will be permanently removed. This cannot be undone.</p>
        <div class="flex gap-3">
          <button @click="showDelete = false" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="saving" @click="doDelete" class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()
const id = route.params.id

const user = ref(null)
const events = ref([])
const tracks = ref([])
const roles = ref([])
const loading = ref(true)
const error = ref('')
const actionError = ref('')
const saving = ref(false)

const showPassword = ref(false)
const newPassword = ref('')
const showDelete = ref(false)

const roleOptions = computed(() => roles.value.map(r => ({ name: r.name, label: r.label || r.name })))

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}
function formatDateTime(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleString(undefined, { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' })
}

function eventColor(type) {
  return {
    lesson_completed: 'bg-emerald-500',
    quiz_attempt: 'bg-[#234ecc]',
    login: 'bg-amber-400',
    registered: 'bg-purple-500',
  }[type] || 'bg-gray-300'
}
function eventLabel(e) {
  if (e.type === 'lesson_completed') return `Completed lesson "${e.lesson_slug}"`
  if (e.type === 'quiz_attempt') return `Answered a quiz in "${e.lesson_slug}" — ${e.is_correct ? 'correct' : 'incorrect'}`
  if (e.type === 'login') return 'Logged in'
  if (e.type === 'registered') return 'Created account'
  return e.type
}

function apiError(e, fallback) {
  return e?.response?.data?.role || e?.response?.data?.is_active || e?.response?.data?.detail || fallback
}

async function changeRole(newRole) {
  if (newRole === user.value.role) return
  const prev = user.value.role
  user.value.role = newRole
  try { await adminApi.updateUser(id, { role: newRole }) }
  catch (e) { user.value.role = prev; actionError.value = apiError(e, 'Could not change role.') }
}

async function toggleActive() {
  const prev = user.value.is_active
  user.value.is_active = !prev
  try { await adminApi.updateUser(id, { is_active: user.value.is_active }) }
  catch (e) { user.value.is_active = prev; actionError.value = apiError(e, 'Could not change status.') }
}

async function doResetPassword() {
  saving.value = true
  try {
    await adminApi.setUserPassword(id, newPassword.value)
    showPassword.value = false
    newPassword.value = ''
  } catch (e) { actionError.value = apiError(e, 'Could not set password.') }
  finally { saving.value = false }
}

async function doDelete() {
  saving.value = true
  try {
    await adminApi.deleteUser(id)
    router.push({ name: 'admin-users' })
  } catch (e) { actionError.value = apiError(e, 'Could not delete user.'); showDelete.value = false }
  finally { saving.value = false }
}

onMounted(async () => {
  try {
    user.value = await adminApi.getUser(id)
    const activity = await adminApi.getUserActivity(id)
    events.value = activity.events || []
    tracks.value = activity.tracks || []
    try { roles.value = await adminApi.listRoles() } catch { /* optional */ }
  } catch {
    error.value = 'Could not load this user.'
  } finally {
    loading.value = false
  }
})
</script>
