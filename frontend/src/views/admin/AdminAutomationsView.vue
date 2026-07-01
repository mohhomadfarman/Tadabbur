<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Email Automation</h1>
          <p class="text-gray-400 text-sm mt-0.5">Condition-based transactional emails triggered by learner activity — separate from marketing campaigns.</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New workflow
        </button>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No workflows yet</p>
        <p class="text-gray-400 text-sm">Create one, e.g. "remind learners who started but haven't finished a track."</p>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm divide-y divide-gray-50">
        <button v-for="w in items" :key="w.id" @click="startEdit(w)"
          class="w-full text-left px-5 py-4 hover:bg-gray-50/60 transition-colors flex items-center justify-between gap-4">
          <div class="min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <p class="font-medium text-gray-800 truncate">{{ w.name }}</p>
              <span class="text-[11px] font-medium px-2 py-0.5 rounded-full" :class="w.is_active ? 'bg-emerald-50 text-emerald-600' : 'bg-gray-100 text-gray-400'">
                {{ w.is_active ? 'Active' : 'Paused' }}
              </span>
            </div>
            <p class="text-xs text-gray-400 truncate mt-0.5">
              {{ triggerLabel(w.trigger_event) }}<template v-if="w.track_slug"> · {{ w.track_slug }}</template>
              <template v-if="w.delay_hours"> · after {{ w.delay_hours }}h</template>
              <template v-else> · immediately</template>
            </p>
          </div>
          <svg class="w-4 h-4 text-gray-300 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
        </button>
      </div>
    </template>

    <!-- ── EDIT MODE ─────────────────────────────────────────────── -->
    <template v-else>
      <div class="sticky top-0 z-10 bg-gray-50/95 backdrop-blur -mx-6 px-6 py-3 flex items-center justify-between mb-6 border-b border-gray-200">
        <button @click="editing = null" class="text-sm text-gray-500 hover:text-gray-800 inline-flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          Back
        </button>
        <div class="flex items-center gap-3">
          <span v-if="saved" class="text-sm text-emerald-600 font-medium">Saved ✓</span>
          <span v-if="formError" class="text-sm text-red-600">{{ formError }}</span>
          <button v-if="form.id" @click="deleteTarget = { id: form.id, name: form.name }"
            class="text-sm text-red-500 hover:text-red-600 px-3 py-2 transition-colors">Delete</button>
          <button :disabled="saving" @click="save"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : (form.id ? 'Save' : 'Create') }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Name <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text" placeholder="e.g. Track reminder"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Trigger</label>
                <select v-model="form.trigger_event" class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
                  <option value="track_started">Track started (not yet finished)</option>
                  <option value="track_completed">Track completed</option>
                  <option value="lesson_completed">Lesson completed</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">Send after</label>
                <div class="flex items-center gap-2">
                  <input v-model.number="form.delay_hours" type="number" min="0" step="1"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <span class="text-xs text-gray-400 shrink-0">hours</span>
                </div>
              </div>
            </div>
            <p class="text-[11px] text-gray-400 -mt-2">0 = send immediately when the trigger fires. Greater than 0 schedules a delayed check.</p>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                Track {{ trackRequired ? '' : '(optional — blank = any track)' }}
                <span v-if="trackRequired" class="text-red-500">*</span>
              </label>
              <select v-model="form.track_slug" class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
                <option value="">{{ trackRequired ? 'Select a track…' : 'Any track' }}</option>
                <option v-for="t in tracks" :key="t.slug" :value="t.slug">{{ t.title }}</option>
              </select>
            </div>

            <label v-if="form.delay_hours > 0" class="flex items-center gap-2.5 cursor-pointer">
              <button type="button" @click="form.recheck_condition = !form.recheck_condition"
                class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors shrink-0"
                :class="form.recheck_condition ? 'bg-[#234ecc]' : 'bg-gray-300'">
                <span class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                  :class="form.recheck_condition ? 'translate-x-4' : 'translate-x-1'" />
              </button>
              <span class="text-sm text-gray-700">Skip the send if the condition is no longer true</span>
            </label>

            <label class="flex items-center gap-2.5 cursor-pointer">
              <button type="button" @click="form.is_active = !form.is_active"
                class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors shrink-0"
                :class="form.is_active ? 'bg-[#234ecc]' : 'bg-gray-300'">
                <span class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                  :class="form.is_active ? 'translate-x-4' : 'translate-x-1'" />
              </button>
              <span class="text-sm text-gray-700">Active</span>
            </label>
          </div>

          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject</label>
              <input v-model="form.subject" type="text" placeholder="Email subject line"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">HTML body</label>
              <textarea v-model="form.html_body" rows="10" spellcheck="false"
                placeholder="<p>Assalamu alaikum, don't forget to finish your track…</p>"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y" />
            </div>
          </div>

          <!-- Audience -->
          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <p class="text-xs font-medium text-gray-500 mb-2">Who this applies to</p>
            <div class="flex gap-2">
              <button type="button" @click="form.audience = 'all'"
                class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
                :class="form.audience === 'all' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
                All users
              </button>
              <button type="button" @click="form.audience = 'selected'"
                class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
                :class="form.audience === 'selected' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
                Selected users
              </button>
            </div>

            <div v-if="form.audience === 'selected'" class="mt-3">
              <div v-if="form.allowed_user_ids.length" class="flex flex-wrap gap-1.5 mb-2">
                <span v-for="uid in form.allowed_user_ids" :key="uid"
                  class="inline-flex items-center gap-1.5 text-xs bg-gray-100 text-gray-700 rounded-full ps-2.5 pe-1 py-1">
                  {{ userLabel(uid) }}
                  <button @click="removeUser(uid)" class="w-4 h-4 rounded-full inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
                  </button>
                </span>
              </div>
              <div class="relative">
                <input v-model="userSearch" @input="onUserSearch" type="text"
                  placeholder="Search users by email or name…"
                  class="w-full border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                <div v-if="userResults.length"
                  class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-xl shadow-lg max-h-56 overflow-y-auto">
                  <button v-for="u in userResults" :key="u.id" @click="addUser(u)"
                    class="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 flex items-center justify-between gap-2"
                    :class="form.allowed_user_ids.includes(u.id) ? 'opacity-50 pointer-events-none' : ''">
                    <span class="truncate">
                      <span class="text-gray-800">{{ u.full_name || u.username }}</span>
                      <span class="text-gray-400 ms-1.5">{{ u.email }}</span>
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent sends (audit trail) -->
        <div class="space-y-2">
          <p class="text-sm font-medium text-gray-700">Recent sends</p>
          <div v-if="!form.id" class="bg-white border border-gray-200 rounded-2xl p-6 text-sm text-gray-400 text-center">
            Save the workflow to start tracking sends.
          </div>
          <div v-else-if="sends.length === 0" class="bg-white border border-gray-200 rounded-2xl p-6 text-sm text-gray-400 text-center">
            No sends yet.
          </div>
          <div v-else class="bg-white border border-gray-200 rounded-2xl shadow-sm divide-y divide-gray-50 max-h-[32rem] overflow-y-auto">
            <div v-for="s in sends" :key="s.id" class="px-4 py-3 text-sm flex items-center justify-between gap-3">
              <div class="min-w-0">
                <p class="text-gray-800 truncate">{{ s.user_email }}</p>
                <p class="text-[11px] text-gray-400">{{ formatDate(s.sent_at || s.scheduled_for || s.created_at) }}</p>
              </div>
              <span class="text-[11px] font-medium px-2 py-0.5 rounded-full shrink-0" :class="statusClass(s.status)">{{ s.status }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete workflow?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.name }}</strong> will be removed. Already-scheduled sends for it are cancelled.</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const items = ref([])
const tracks = ref([])
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({
  id: null, name: '', trigger_event: 'track_started', track_slug: '',
  delay_hours: 4, recheck_condition: true, subject: '', html_body: '',
  is_active: true, audience: 'all', allowed_user_ids: [],
})
const saving = ref(false)
const saved = ref(false)
const formError = ref('')

const sends = ref([])

const deleteTarget = ref(null)
const deleting = ref(false)

const userSearch = ref('')
const userResults = ref([])
const userCache = reactive({})
let userSearchTimer = null

const trackRequired = computed(() => form.trigger_event === 'track_started' || form.trigger_event === 'track_completed')

const TRIGGER_LABELS = {
  track_started: 'Track started',
  track_completed: 'Track completed',
  lesson_completed: 'Lesson completed',
}
function triggerLabel(key) { return TRIGGER_LABELS[key] || key }

function userLabel(uid) {
  const u = userCache[uid]
  return u ? (u.email || u.username || uid) : '…'
}

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString('en-GB', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
}

function statusClass(status) {
  if (status === 'sent') return 'bg-emerald-50 text-emerald-600'
  if (status === 'scheduled') return 'bg-amber-50 text-amber-600'
  if (status === 'failed') return 'bg-red-50 text-red-600'
  return 'bg-gray-100 text-gray-500'
}

async function load() {
  loading.value = true
  try {
    const [workflows, trackList] = await Promise.all([adminApi.listWorkflows(), adminApi.listTracks()])
    items.value = workflows
    tracks.value = trackList
  } catch {
    error.value = 'Could not load workflows. Make sure your account has Email Automation access.'
  } finally {
    loading.value = false
  }
}

function resetForm() {
  Object.assign(form, {
    id: null, name: '', trigger_event: 'track_started', track_slug: '',
    delay_hours: 4, recheck_condition: true, subject: '', html_body: '',
    is_active: true, audience: 'all', allowed_user_ids: [],
  })
  sends.value = []
}

function startNew() {
  resetForm()
  formError.value = ''; saved.value = false; editing.value = true
}

async function startEdit(row) {
  formError.value = ''; saved.value = false
  try {
    const w = await adminApi.getWorkflow(row.id)
    Object.assign(form, {
      id: w.id, name: w.name, trigger_event: w.trigger_event, track_slug: w.track_slug,
      delay_hours: w.delay_hours, recheck_condition: w.recheck_condition,
      subject: w.subject, html_body: w.html_body, is_active: w.is_active,
      audience: w.audience, allowed_user_ids: [...(w.allowed_user_ids || [])],
    })
    editing.value = true
    loadSends()
    if (form.allowed_user_ids.length) {
      try {
        const users = await adminApi.resolveFeatureUsers(form.allowed_user_ids)
        users.forEach(u => { userCache[u.id] = u })
      } catch { /* labels just show as … */ }
    }
  } catch { error.value = 'Could not open that workflow.' }
}

async function loadSends() {
  if (!form.id) return
  try {
    sends.value = await adminApi.getWorkflowSends(form.id)
  } catch { sends.value = [] }
}

function onUserSearch() {
  clearTimeout(userSearchTimer)
  const q = userSearch.value.trim()
  if (!q) { userResults.value = []; return }
  userSearchTimer = setTimeout(async () => {
    try {
      const users = await adminApi.searchFeatureUsers(q)
      users.forEach(u => { userCache[u.id] = u })
      userResults.value = users
    } catch { userResults.value = [] }
  }, 250)
}

function addUser(u) {
  if (!form.allowed_user_ids.includes(u.id)) form.allowed_user_ids.push(u.id)
  userCache[u.id] = u
  userSearch.value = ''
  userResults.value = []
}
function removeUser(uid) {
  form.allowed_user_ids = form.allowed_user_ids.filter(id => id !== uid)
}

async function save() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = 'A name is required.'; return }
  if (trackRequired.value && !form.track_slug) { formError.value = 'A track is required for this trigger.'; return }
  saving.value = true
  try {
    const payload = {
      name: form.name.trim(),
      trigger_event: form.trigger_event,
      track_slug: form.track_slug,
      delay_hours: form.delay_hours || 0,
      recheck_condition: form.recheck_condition,
      subject: form.subject.trim(),
      html_body: form.html_body,
      is_active: form.is_active,
      audience: form.audience,
      allowed_user_ids: form.allowed_user_ids,
    }
    const w = form.id
      ? await adminApi.updateWorkflow(form.id, payload)
      : await adminApi.createWorkflow(payload)
    form.id = w.id
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.name || e?.response?.data?.track_slug || e?.response?.data?.trigger_event || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteWorkflow(deleteTarget.value.id)
    if (form.id === deleteTarget.value.id) editing.value = null
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Could not delete this workflow.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>
