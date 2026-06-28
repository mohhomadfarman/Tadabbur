<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Feature Flags</h1>
      <p class="text-gray-400 text-sm mt-0.5">
        Turn features on/off, or roll them out to a selected group of users for pre-testing.
      </p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="n in 5" :key="n" class="bg-gray-100 rounded-2xl h-28" />
    </div>

    <div v-else class="space-y-4">
      <div v-for="row in rows" :key="row.key"
        class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">

        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <h2 class="text-sm font-semibold text-gray-900">{{ row.label }}</h2>
              <span v-if="row.owner_section" class="text-[11px] font-medium px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">{{ row.owner_section }}</span>
              <code class="text-[11px] text-gray-400">{{ row.key }}</code>
            </div>
            <p class="text-xs text-gray-400 mt-1">{{ row.description }}</p>
          </div>

          <!-- Enabled toggle -->
          <button type="button" @click="row.enabled = !row.enabled"
            class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors shrink-0 mt-0.5"
            :class="row.enabled ? 'bg-[#234ecc]' : 'bg-gray-300'">
            <span class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
              :class="row.enabled ? 'translate-x-4' : 'translate-x-1'" />
          </button>
        </div>

        <!-- Audience -->
        <div v-if="row.enabled" class="mt-4 pt-4 border-t border-gray-100">
          <p class="text-xs font-medium text-gray-500 mb-2">Who can use it</p>
          <div class="flex gap-2">
            <button type="button" @click="row.audience = 'all'"
              class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
              :class="row.audience === 'all' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
              All users
            </button>
            <button type="button" @click="row.audience = 'selected'"
              class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
              :class="row.audience === 'selected' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
              Selected users
            </button>
          </div>

          <!-- Selected-users picker -->
          <div v-if="row.audience === 'selected'" class="mt-3">
            <div v-if="row.allowed_user_ids.length" class="flex flex-wrap gap-1.5 mb-2">
              <span v-for="uid in row.allowed_user_ids" :key="uid"
                class="inline-flex items-center gap-1.5 text-xs bg-gray-100 text-gray-700 rounded-full ps-2.5 pe-1 py-1">
                {{ userLabel(uid) }}
                <button @click="removeUser(row, uid)" class="w-4 h-4 rounded-full inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
                </button>
              </span>
            </div>
            <div class="relative">
              <input v-model="search[row.key]" @input="onSearch(row.key)" type="text"
                placeholder="Search users by email or name…"
                class="w-full border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <div v-if="results[row.key]?.length"
                class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-xl shadow-lg max-h-56 overflow-y-auto">
                <button v-for="u in results[row.key]" :key="u.id" @click="addUser(row, u)"
                  class="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 flex items-center justify-between gap-2"
                  :class="row.allowed_user_ids.includes(u.id) ? 'opacity-50 pointer-events-none' : ''">
                  <span class="truncate">
                    <span class="text-gray-800">{{ u.full_name || u.username }}</span>
                    <span class="text-gray-400 ms-1.5">{{ u.email }}</span>
                  </span>
                  <span v-if="row.allowed_user_ids.includes(u.id)" class="text-[11px] text-emerald-600">added</span>
                </button>
              </div>
            </div>
            <p class="text-[11px] text-gray-400 mt-1.5">Only these users will see the feature while it's in pre-testing.</p>
          </div>
        </div>

        <!-- Save -->
        <div class="mt-4 flex items-center justify-end gap-3">
          <span v-if="savedKey === row.key" class="text-xs text-emerald-600 font-medium">Saved ✓</span>
          <button :disabled="!isDirty(row) || savingKey === row.key" @click="saveFlag(row)"
            class="text-xs font-semibold px-4 py-2 rounded-lg transition-colors"
            :class="isDirty(row) ? 'bg-[#234ecc] hover:bg-[#1a3ba8] text-white' : 'bg-gray-100 text-gray-400 cursor-default'">
            {{ savingKey === row.key ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const rows = ref([])
const loading = ref(true)
const error = ref('')
const savingKey = ref(null)
const savedKey = ref(null)

// Snapshot of the last-saved state per key, to compute dirtiness.
const snapshots = reactive({})
// Per-flag user search state + a shared cache of id → user object for labels.
const search = reactive({})
const results = reactive({})
const userCache = reactive({})
const searchTimers = {}

function snapshotOf(row) {
  return JSON.stringify({ enabled: row.enabled, audience: row.audience, allowed_user_ids: [...row.allowed_user_ids].sort() })
}
function isDirty(row) {
  return snapshots[row.key] !== snapshotOf(row)
}
function userLabel(uid) {
  const u = userCache[uid]
  return u ? (u.email || u.username || uid) : '…'
}

async function load() {
  loading.value = true
  try {
    const data = await adminApi.listFeatureFlags()
    rows.value = data.map(r => ({ ...r, allowed_user_ids: [...(r.allowed_user_ids || [])] }))
    rows.value.forEach(r => { snapshots[r.key] = snapshotOf(r); search[r.key] = ''; results[r.key] = [] })
    // Resolve labels for all already-selected users in one call.
    const ids = [...new Set(rows.value.flatMap(r => r.allowed_user_ids))]
    if (ids.length) {
      try {
        const users = await adminApi.resolveFeatureUsers(ids)
        users.forEach(u => { userCache[u.id] = u })
      } catch { /* names just show as … */ }
    }
  } catch {
    error.value = 'Could not load feature flags. Make sure your account has Feature Flags access.'
  } finally {
    loading.value = false
  }
}

function onSearch(key) {
  clearTimeout(searchTimers[key])
  const q = (search[key] || '').trim()
  if (!q) { results[key] = []; return }
  searchTimers[key] = setTimeout(async () => {
    try {
      const users = await adminApi.searchFeatureUsers(q)
      users.forEach(u => { userCache[u.id] = u })
      results[key] = users
    } catch { results[key] = [] }
  }, 250)
}

function addUser(row, u) {
  if (!row.allowed_user_ids.includes(u.id)) row.allowed_user_ids.push(u.id)
  userCache[u.id] = u
  search[row.key] = ''
  results[row.key] = []
}
function removeUser(row, uid) {
  row.allowed_user_ids = row.allowed_user_ids.filter(id => id !== uid)
}

async function saveFlag(row) {
  savingKey.value = row.key
  try {
    const saved = await adminApi.updateFeatureFlag(row.key, {
      enabled: row.enabled,
      audience: row.audience,
      allowed_user_ids: row.allowed_user_ids,
    })
    // Server validates/filters allowed_user_ids — reflect what it stored.
    row.allowed_user_ids = [...(saved.allowed_user_ids || [])]
    snapshots[row.key] = snapshotOf(row)
    savedKey.value = row.key
    setTimeout(() => { if (savedKey.value === row.key) savedKey.value = null }, 2500)
  } catch {
    error.value = 'Could not save that flag.'
  } finally {
    savingKey.value = null
  }
}

onMounted(load)
</script>
