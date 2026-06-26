<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex items-start justify-between mb-8 gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Registrations</h1>
        <p class="text-gray-400 text-sm mt-0.5">People signed up for the live launch.</p>
      </div>
      <button
        v-if="registrations.length"
        @click="exportCsv"
        class="inline-flex items-center gap-2 bg-white border border-gray-200 hover:border-[#234ecc]/40 hover:text-[#234ecc] text-gray-700 text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shadow-sm shrink-0"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
        Export CSV
      </button>
    </div>

    <div v-if="actionError" class="bg-red-50 border border-red-200 text-red-700 px-5 py-3 rounded-xl text-sm mb-6 flex items-start justify-between gap-3">
      <span>{{ actionError }}</span>
      <button @click="actionError = ''" class="text-red-400 hover:text-red-600 shrink-0">✕</button>
    </div>
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <!-- Event settings (powers the public /launch page) -->
    <details class="bg-white border border-gray-200 rounded-2xl shadow-sm mb-8" open>
      <summary class="flex items-center justify-between gap-3 px-5 py-4 cursor-pointer select-none">
        <div>
          <h2 class="font-semibold text-gray-800">Event settings</h2>
          <p class="text-xs text-gray-400 mt-0.5">Date, headline and intro shown on the <span class="font-mono">/launch</span> page.</p>
        </div>
        <span v-if="settingsSaved" class="text-xs text-emerald-600 font-semibold shrink-0">Saved ✓</span>
      </summary>
      <div class="px-5 pb-5 grid sm:grid-cols-2 gap-4 border-t border-gray-100 pt-5">
        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1">Date &amp; time</label>
          <input v-model="settingsForm.datetime" type="datetime-local"
            class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1">Timezone</label>
          <select v-model="settingsForm.offset"
            class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
            <option v-for="o in offsetOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
          </select>
        </div>
        <div class="sm:col-span-2">
          <label class="block text-xs font-medium text-gray-500 mb-1">Headline</label>
          <input v-model="settingsForm.headline" type="text" maxlength="120"
            class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        </div>
        <div class="sm:col-span-2">
          <label class="block text-xs font-medium text-gray-500 mb-1">Intro paragraph</label>
          <textarea v-model="settingsForm.intro" rows="3"
            class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"></textarea>
        </div>
        <div class="sm:col-span-2 flex flex-wrap items-center gap-3">
          <button @click="saveSettings" :disabled="savingSettings"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors">
            {{ savingSettings ? 'Saving…' : 'Save event settings' }}
          </button>
          <span class="text-xs text-gray-400">Preview: <span class="text-gray-600">{{ previewLabel }}</span></span>
          <span v-if="settingsError" class="text-xs text-red-600">{{ settingsError }}</span>
        </div>
      </div>
    </details>

    <!-- Toolbar -->
    <div v-if="!loading && registrations.length > 0" class="mb-6 flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-width="2" d="m21 21-4.35-4.35"/>
        </svg>
        <input v-model="searchQuery" type="search" placeholder="Search name, email, phone, country…"
          class="w-full border border-gray-200 rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
      </div>
      <span class="text-sm text-gray-400 self-center whitespace-nowrap">
        {{ filtered.length }} registration{{ filtered.length === 1 ? '' : 's' }}
      </span>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-2 animate-pulse">
      <div v-for="n in 8" :key="n" class="bg-gray-100 rounded-xl h-14" />
    </div>

    <!-- Empty -->
    <div v-else-if="registrations.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
      <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4 mx-auto">
        <svg class="w-7 h-7 text-gray-300" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/></svg>
      </div>
      <p class="text-gray-600 font-semibold mb-1">No registrations yet</p>
      <p class="text-gray-400 text-sm">They'll appear here as people sign up at <span class="font-mono">/launch</span>.</p>
    </div>
    <div v-else-if="filtered.length === 0" class="py-20 text-center text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-2xl">
      No registrations match your search.
    </div>

    <!-- Table -->
    <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-x-auto shadow-sm">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 text-xs text-gray-400 uppercase tracking-wider">
            <th class="px-5 py-3 text-left font-medium">Name</th>
            <th class="px-4 py-3 text-left font-medium">Email</th>
            <th class="px-4 py-3 text-left font-medium hidden sm:table-cell">WhatsApp</th>
            <th class="px-4 py-3 text-left font-medium hidden md:table-cell">Country / City</th>
            <th class="px-4 py-3 text-right font-medium hidden lg:table-cell">Registered</th>
            <th class="px-4 py-3 text-right font-medium w-px"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in paged" :key="r.id" class="border-b border-gray-50 last:border-0 hover:bg-gray-50/60 transition-colors">
            <td class="px-5 py-3 font-medium text-gray-800">{{ r.full_name }}</td>
            <td class="px-4 py-3 text-gray-600"><a :href="`mailto:${r.email}`" class="hover:text-[#234ecc]">{{ r.email }}</a></td>
            <td class="px-4 py-3 text-gray-600 hidden sm:table-cell">{{ r.phone || '—' }}</td>
            <td class="px-4 py-3 text-gray-600 hidden md:table-cell">{{ r.country || '—' }}</td>
            <td class="px-4 py-3 text-right text-gray-400 text-xs hidden lg:table-cell">{{ formatDate(r.created_at) }}</td>
            <td class="px-4 py-3 text-right">
              <button @click="deleteTarget = r" title="Delete" class="w-8 h-8 rounded-lg inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
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

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete registration?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.email }}</strong> will be removed from the list.</p>
        <div class="flex gap-3">
          <button @click="deleteTarget = null" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="deleting" @click="doDelete" class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ deleting ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const registrations = ref([])
const loading = ref(true)
const error = ref('')
const actionError = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)

// ── Event settings (powers the /launch page) ─────────────────────────
const COMMON_OFFSETS = [
  { value: '+05:30', label: 'GMT+5:30 — India / Sri Lanka' },
  { value: '+05:00', label: 'GMT+5:00 — Pakistan' },
  { value: '+04:00', label: 'GMT+4:00 — UAE / Gulf' },
  { value: '+03:00', label: 'GMT+3:00 — Makkah / Türkiye' },
  { value: '+01:00', label: 'GMT+1:00 — Central Europe' },
  { value: '+00:00', label: 'GMT — UK / UTC' },
  { value: '+07:00', label: 'GMT+7:00 — Indonesia (WIB)' },
  { value: '+08:00', label: 'GMT+8:00 — Malaysia / Singapore' },
  { value: '-05:00', label: 'GMT-5:00 — US Eastern' },
  { value: '-08:00', label: 'GMT-8:00 — US Pacific' },
]
const settings = ref(null)
const settingsForm = reactive({ datetime: '', offset: '+05:30', headline: '', intro: '' })
const savingSettings = ref(false)
const settingsSaved = ref(false)
const settingsError = ref('')

const offsetOptions = computed(() =>
  settingsForm.offset && !COMMON_OFFSETS.some(o => o.value === settingsForm.offset)
    ? [{ value: settingsForm.offset, label: `GMT ${settingsForm.offset}` }, ...COMMON_OFFSETS]
    : COMMON_OFFSETS
)

function loadSettingsForm(s) {
  const m = String(s.event_at || '').match(/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})(?::\d{2})?(Z|[+-]\d{2}:\d{2})?$/)
  settingsForm.datetime = m ? m[1] : ''
  settingsForm.offset = m ? (m[2] === 'Z' ? '+00:00' : (m[2] || '+05:30')) : '+05:30'
  settingsForm.headline = s.headline || ''
  settingsForm.intro = s.intro || ''
}

function eventIso() {
  return settingsForm.datetime ? `${settingsForm.datetime}:00${settingsForm.offset}` : ''
}

const previewLabel = computed(() => {
  const iso = eventIso()
  const d = iso ? new Date(iso) : null
  if (!d || Number.isNaN(d.getTime())) return '—'
  const sign = settingsForm.offset[0] === '-' ? -1 : 1
  const oh = parseInt(settingsForm.offset.slice(1, 3), 10)
  const om = parseInt(settingsForm.offset.slice(4, 6), 10)
  const label = 'GMT' + (sign < 0 ? '-' : '+') + oh + (om ? ':' + String(om).padStart(2, '0') : '')
  const wall = new Date(d.getTime() + sign * (oh * 60 + om) * 60000).toLocaleString('en-US', {
    timeZone: 'UTC', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    hour: 'numeric', minute: '2-digit',
  })
  return `${wall} ${label}`
})

async function saveSettings() {
  settingsError.value = ''
  if (!settingsForm.datetime) { settingsError.value = 'Pick a date and time.'; return }
  savingSettings.value = true
  try {
    settings.value = await adminApi.updateLaunchSettings({
      event_at: eventIso(),
      headline: settingsForm.headline,
      intro: settingsForm.intro,
    })
    settingsSaved.value = true
    setTimeout(() => { settingsSaved.value = false }, 2500)
  } catch {
    settingsError.value = 'Could not save event settings.'
  } finally {
    savingSettings.value = false
  }
}

const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 20

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return registrations.value
  return registrations.value.filter(r =>
    `${r.full_name} ${r.email} ${r.phone} ${r.country}`.toLowerCase().includes(q)
  )
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)))
const paged = computed(() => filtered.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

watch(searchQuery, () => { currentPage.value = 1 })
watch(totalPages, (tp) => { if (currentPage.value > tp) currentPage.value = tp })
function goToPage(p) { currentPage.value = Math.min(Math.max(1, p), totalPages.value) }

function formatDate(iso) {
  if (!iso) return '—'
  const d = new Date(iso)
  return Number.isNaN(d.getTime()) ? '—' : d.toLocaleString(undefined, { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' })
}

function exportCsv() {
  const headers = ['Name', 'Email', 'WhatsApp', 'Country/City', 'Registered']
  const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`
  const rows = filtered.value.map(r => [r.full_name, r.email, r.phone, r.country, r.created_at].map(esc).join(','))
  const csv = [headers.map(esc).join(','), ...rows].join('\r\n')
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `launch-registrations-${new Date().toISOString().slice(0, 10)}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteRegistration(deleteTarget.value.id)
    registrations.value = registrations.value.filter(r => r.id !== deleteTarget.value.id)
    deleteTarget.value = null
  } catch {
    actionError.value = 'Could not delete this registration.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  try {
    registrations.value = await adminApi.listRegistrations()
  } catch {
    error.value = 'Could not load registrations. Make sure your account has Registrations access.'
  } finally {
    loading.value = false
  }
  try {
    const s = await adminApi.getLaunchSettings()
    settings.value = s
    loadSettingsForm(s)
  } catch { /* settings optional */ }
})
</script>
