<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Email Campaigns</h1>
          <p class="text-gray-400 text-sm mt-0.5">Send an email to a segment of your audience.</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New campaign
        </button>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No campaigns yet</p>
        <p class="text-gray-400 text-sm">Create one to reach your learners.</p>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-x-auto shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-100 text-xs text-gray-400 uppercase tracking-wider">
              <th class="px-5 py-3 text-left font-medium">Name</th>
              <th class="px-4 py-3 text-left font-medium">Status</th>
              <th class="px-4 py-3 text-left font-medium hidden sm:table-cell">Segment</th>
              <th class="px-4 py-3 text-right font-medium">Sent</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in items" :key="c.id" class="border-b border-gray-50 last:border-0 hover:bg-gray-50/60 transition-colors cursor-pointer" @click="startEdit(c)">
              <td class="px-5 py-3 font-medium text-gray-800">{{ c.name }}</td>
              <td class="px-4 py-3"><span class="text-xs font-semibold px-2 py-0.5 rounded-full" :class="statusClass(c.status)">{{ c.status }}</span></td>
              <td class="px-4 py-3 text-gray-500 text-xs hidden sm:table-cell">{{ c.segment }}</td>
              <td class="px-4 py-3 text-right text-gray-700 font-semibold">{{ c.stats?.sent ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
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
          <!-- Pause / Resume -->
          <button v-if="form.id && form.status === 'scheduled'" :disabled="pausing" @click="doPause"
            class="bg-amber-50 border border-amber-200 hover:bg-amber-100 disabled:opacity-60 text-amber-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ pausing ? '…' : 'Pause' }}
          </button>
          <button v-if="form.id && form.status === 'paused'" :disabled="pausing" @click="doPause"
            class="bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 disabled:opacity-60 text-emerald-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ pausing ? '…' : 'Resume' }}
          </button>
          <!-- Delete -->
          <button v-if="form.id && !isActive" @click="confirmDelete = true"
            class="bg-red-50 border border-red-200 hover:bg-red-100 text-red-600 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            Delete
          </button>
          <button v-if="!isSent" :disabled="saving" @click="save"
            class="bg-white border border-gray-200 hover:bg-gray-50 disabled:opacity-60 text-gray-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : (form.id ? 'Save draft' : 'Create draft') }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Content -->
        <div class="lg:col-span-2 space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Campaign name <span class="text-red-500">*</span></label>
              <input v-model="form.name" :disabled="isSent" type="text" placeholder="Internal name"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 disabled:bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Start from template</label>
              <select :disabled="isSent" @change="applyTemplate($event.target.value)"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 disabled:bg-gray-50">
                <option value="">— None —</option>
                <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject</label>
              <input v-model="form.subject" :disabled="isSent" type="text"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 disabled:bg-gray-50" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">HTML body</label>
              <textarea v-model="form.html_body" :disabled="isSent" rows="14" spellcheck="false"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y disabled:bg-gray-50" />
            </div>
          </div>
        </div>

        <!-- Settings -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Recipients</label>
              <select v-model="form.segment" :disabled="isSent" @change="previewCount"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 disabled:bg-gray-50">
                <option v-for="s in segments" :key="s.key" :value="s.key">{{ s.label }}</option>
              </select>
              <p class="text-[11px] text-gray-400 mt-1">
                <span v-if="recipientCount !== null">{{ recipientCount }} recipient(s) after removing unsubscribes.</span>
                <span v-else>Select to preview the count.</span>
              </p>
            </div>

            <div>
              <p class="text-sm font-medium text-gray-700 mb-1.5">Status</p>
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full" :class="statusClass(form.status)">{{ form.status }}</span>
            </div>

            <div v-if="form.stats && (form.stats.total != null)" class="pt-3 border-t border-gray-100 text-xs text-gray-500 space-y-1">
              <p>Sent: <span class="font-semibold text-gray-800">{{ form.stats.sent }}</span></p>
              <p>Failed: <span class="font-semibold text-gray-800">{{ form.stats.failed }}</span></p>
              <p>Total: <span class="font-semibold text-gray-800">{{ form.stats.total }}</span></p>
            </div>
          </div>

          <!-- Test send -->
          <div v-if="form.id && !isSent" class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-3">
            <p class="text-sm font-medium text-gray-700">Send a test</p>
            <div class="flex gap-2">
              <input v-model="testEmail" type="email" placeholder="you@example.com"
                class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <button :disabled="testing || !testEmail" @click="doTest"
                class="bg-gray-100 hover:bg-gray-200 disabled:opacity-50 text-gray-700 text-sm font-medium px-3 py-2 rounded-xl transition-colors">
                {{ testing ? '…' : 'Send' }}
              </button>
            </div>
            <p v-if="testMsg" class="text-[11px] text-emerald-600">{{ testMsg }}</p>
          </div>

          <!-- Send / schedule -->
          <div v-if="form.id && !isSent" class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-3">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Schedule (optional, UTC)</label>
              <input v-model="form.scheduled_at" type="datetime-local"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <button :disabled="sending" @click="confirmSend = true"
              class="w-full bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold py-2.5 rounded-xl transition-colors">
              {{ form.scheduled_at ? 'Schedule send' : 'Send now' }}
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete confirmation -->
    <div v-if="confirmDelete" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="confirmDelete = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete this campaign?</h3>
        <p class="text-sm text-gray-500 mb-5">
          <strong>{{ form.name }}</strong> will be permanently deleted. This cannot be undone.
        </p>
        <div class="flex gap-3">
          <button @click="confirmDelete = false" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="deleting" @click="doDelete" class="flex-1 px-4 py-2.5 bg-red-600 hover:bg-red-700 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ deleting ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Send confirmation -->
    <div v-if="confirmSend" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="confirmSend = false">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">{{ form.scheduled_at ? 'Schedule this campaign?' : 'Send this campaign now?' }}</h3>
        <p class="text-sm text-gray-500 mb-5">
          It will go to <strong>{{ recipientCount ?? '…' }}</strong> recipient(s) in the
          <strong>{{ form.segment }}</strong> segment. This can't be undone.
        </p>
        <div class="flex gap-3">
          <button @click="confirmSend = false" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="sending" @click="doSend" class="flex-1 px-4 py-2.5 bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ sending ? 'Working…' : (form.scheduled_at ? 'Schedule' : 'Send now') }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { adminApi } from '@/api/admin'

const items = ref([])
const templates = ref([])
const segments = ref([{ key: 'all_users', label: 'All active users' }])
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({ id: null, name: '', subject: '', html_body: '', segment: 'all_users', status: 'draft', scheduled_at: '', stats: null })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')
const recipientCount = ref(null)

const testEmail = ref('')
const testing = ref(false)
const testMsg = ref('')

const confirmSend = ref(false)
const sending = ref(false)
const pausing = ref(false)
const confirmDelete = ref(false)
const deleting = ref(false)
let pollTimer = null

const isSent = computed(() => ['sending', 'sent'].includes(form.status))
const isActive = computed(() => ['sending', 'sent'].includes(form.status))

function statusClass(s) {
  return {
    draft: 'bg-gray-100 text-gray-500',
    scheduled: 'bg-amber-100 text-amber-700',
    paused: 'bg-orange-100 text-orange-600',
    sending: 'bg-blue-100 text-blue-700',
    sent: 'bg-emerald-100 text-emerald-700',
    failed: 'bg-red-100 text-red-700',
  }[s] || 'bg-gray-100 text-gray-500'
}

function toLocalInput(iso) { return iso ? String(iso).slice(0, 16) : '' }

async function load() {
  loading.value = true
  try {
    items.value = await adminApi.listEmailCampaigns()
  } catch {
    error.value = 'Could not load campaigns. Make sure your account has Email Marketing access.'
  } finally {
    loading.value = false
  }
}

async function loadAux() {
  try { templates.value = await adminApi.listEmailTemplates() } catch { templates.value = [] }
  try { segments.value = await adminApi.listEmailSegments() } catch { /* keep default */ }
}

function resetForm() {
  Object.assign(form, { id: null, name: '', subject: '', html_body: '', segment: 'all_users', status: 'draft', scheduled_at: '', stats: null })
  formError.value = ''; saved.value = false; recipientCount.value = null; testMsg.value = ''
}

function startNew() { resetForm(); editing.value = true; previewCount() }

async function startEdit(row) {
  resetForm()
  try {
    const c = await adminApi.getEmailCampaign(row.id)
    Object.assign(form, {
      id: c.id, name: c.name, subject: c.subject, html_body: c.html_body,
      segment: c.segment, status: c.status, scheduled_at: toLocalInput(c.scheduled_at), stats: c.stats || null,
    })
    editing.value = true
    previewCount()
    if (form.status === 'sending') startPolling()
  } catch { error.value = 'Could not open that campaign.' }
}

function applyTemplate(id) {
  const t = templates.value.find(x => x.id === id)
  if (!t) return
  // Fetch full body (list rows don't include html_body).
  adminApi.getEmailTemplate(id).then(full => {
    if (!form.subject) form.subject = full.subject || ''
    form.html_body = full.html_body || form.html_body
  }).catch(() => {})
}

async function previewCount() {
  recipientCount.value = null
  try {
    const res = await adminApi.previewEmailSegment(form.segment)
    recipientCount.value = res.count
  } catch { recipientCount.value = null }
}

async function save() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = 'A name is required.'; return }
  saving.value = true
  try {
    const payload = { name: form.name.trim(), subject: form.subject.trim(), html_body: form.html_body, segment: form.segment }
    const c = form.id
      ? await adminApi.updateEmailCampaign(form.id, payload)
      : await adminApi.createEmailCampaign(payload)
    Object.assign(form, { id: c.id, status: c.status, stats: c.stats || null })
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.detail || e?.response?.data?.name || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doTest() {
  testing.value = true; testMsg.value = ''
  try {
    await adminApi.testEmailCampaign(form.id, testEmail.value.trim())
    testMsg.value = 'Test email sent — check that inbox.'
  } catch (e) { testMsg.value = ''; formError.value = e?.response?.data?.detail || 'Test send failed.' }
  finally { testing.value = false }
}

async function doSend() {
  sending.value = true
  try {
    const payload = form.scheduled_at ? { scheduled_at: form.scheduled_at } : {}
    const res = await adminApi.sendEmailCampaign(form.id, payload)
    confirmSend.value = false
    form.status = res.scheduled ? 'scheduled' : 'sending'
    if (form.status === 'sending') startPolling()
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.detail || 'Could not send.'
    confirmSend.value = false
  } finally {
    sending.value = false
  }
}

async function doPause() {
  pausing.value = true; formError.value = ''
  try {
    const c = await adminApi.pauseEmailCampaign(form.id)
    form.status = c.status
    form.scheduled_at = toLocalInput(c.scheduled_at)
    if (c.info) formError.value = c.info
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.detail || 'Could not pause/resume.'
  } finally {
    pausing.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteEmailCampaign(form.id)
    confirmDelete.value = false
    editing.value = null
    await load()
  } catch {
    formError.value = 'Could not delete the campaign.'
    confirmDelete.value = false
  } finally {
    deleting.value = false
  }
}

function startPolling() {
  stopPolling()
  pollTimer = setInterval(async () => {
    if (!form.id) return
    try {
      const c = await adminApi.getEmailCampaign(form.id)
      form.status = c.status; form.stats = c.stats || null
      if (c.status !== 'sending') { stopPolling(); await load() }
    } catch { /* ignore */ }
  }, 3000)
}
function stopPolling() { if (pollTimer) { clearInterval(pollTimer); pollTimer = null } }

onMounted(async () => { await load(); await loadAux() })
onUnmounted(stopPolling)
</script>
