<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Email Templates</h1>
          <p class="text-gray-400 text-sm mt-0.5">Reusable subject + HTML layouts for your campaigns.</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New template
        </button>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No templates yet</p>
        <p class="text-gray-400 text-sm">Create one to reuse across campaigns.</p>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm divide-y divide-gray-50">
        <button v-for="t in items" :key="t.id" @click="startEdit(t)"
          class="w-full text-left px-5 py-4 hover:bg-gray-50/60 transition-colors flex items-center justify-between gap-4">
          <div class="min-w-0">
            <p class="font-medium text-gray-800 truncate">{{ t.name }}</p>
            <p class="text-xs text-gray-400 truncate">{{ t.subject || 'No subject' }}</p>
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
              <input v-model="form.name" type="text" placeholder="e.g. Monthly newsletter"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject</label>
              <input v-model="form.subject" type="text" placeholder="Email subject line"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">HTML body</label>
              <textarea v-model="form.html_body" rows="16" spellcheck="false"
                placeholder="<h1>Hello!</h1><p>Your message…</p>"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y" />
              <p class="text-[11px] text-gray-400 mt-1">Raw HTML. An unsubscribe footer is appended automatically when sent.</p>
            </div>
          </div>

          <!-- Send a single test email of the current content -->
          <div class="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm">
            <p class="text-sm font-medium text-gray-700 mb-2">Send a test</p>
            <div class="flex gap-2">
              <input v-model="testEmail" type="email" placeholder="you@example.com"
                class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <button :disabled="testing || !testEmail" @click="doTest"
                class="bg-gray-100 hover:bg-gray-200 disabled:opacity-50 text-gray-700 text-sm font-medium px-3 py-2 rounded-xl transition-colors whitespace-nowrap">
                {{ testing ? 'Sending…' : 'Send test' }}
              </button>
            </div>
            <p v-if="testMsg" class="text-[11px] mt-1.5" :class="testOk ? 'text-emerald-600' : 'text-red-600'">{{ testMsg }}</p>
            <p class="text-[11px] text-gray-400 mt-1">Sends the current subject + body to one address. Configure SMTP in Email Settings first (in dev it prints to the server log).</p>
          </div>
        </div>

        <!-- Preview — rendered in a sandboxed iframe (scripts disabled, isolated
             origin) so authored HTML can never run JS in the admin's session. -->
        <div class="space-y-2">
          <p class="text-sm font-medium text-gray-700">Preview</p>
          <div class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
            <iframe :srcdoc="previewDoc" sandbox="" title="Email preview"
              class="w-full h-[28rem] border-0 bg-white" />
          </div>
        </div>
      </div>
    </template>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete template?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.name }}</strong> will be removed.</p>
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
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({ id: null, name: '', subject: '', html_body: '' })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')

const deleteTarget = ref(null)
const deleting = ref(false)

const testEmail = ref('')
const testing = ref(false)
const testMsg = ref('')
const testOk = ref(false)

const previewDoc = computed(() =>
  form.html_body || '<p style="color:#bbb;font-family:system-ui">Nothing to preview yet.</p>'
)

async function load() {
  loading.value = true
  try {
    items.value = await adminApi.listEmailTemplates()
  } catch {
    error.value = 'Could not load templates. Make sure your account has Email Marketing access.'
  } finally {
    loading.value = false
  }
}

function startNew() {
  Object.assign(form, { id: null, name: '', subject: '', html_body: '' })
  formError.value = ''; saved.value = false; editing.value = true
}

async function startEdit(row) {
  formError.value = ''; saved.value = false
  try {
    const t = await adminApi.getEmailTemplate(row.id)
    Object.assign(form, { id: t.id, name: t.name, subject: t.subject, html_body: t.html_body })
    editing.value = true
  } catch { error.value = 'Could not open that template.' }
}

async function save() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = 'A name is required.'; return }
  saving.value = true
  try {
    const payload = { name: form.name.trim(), subject: form.subject.trim(), html_body: form.html_body }
    const t = form.id
      ? await adminApi.updateEmailTemplate(form.id, payload)
      : await adminApi.createEmailTemplate(payload)
    form.id = t.id
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.name || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doTest() {
  testing.value = true; testMsg.value = ''
  try {
    await adminApi.testSendEmail({
      email: testEmail.value.trim(),
      subject: form.subject,
      html_body: form.html_body,
    })
    testOk.value = true
    testMsg.value = 'Sent — check that inbox (or the server log in dev).'
  } catch (e) {
    testOk.value = false
    testMsg.value = e?.response?.data?.detail || e?.response?.data?.email || 'Could not send the test.'
  } finally {
    testing.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteEmailTemplate(deleteTarget.value.id)
    if (form.id === deleteTarget.value.id) editing.value = null
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Could not delete this template.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>
