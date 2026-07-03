<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Email Templates</h1>
          <p class="text-gray-400 text-sm mt-0.5">Reusable subject + layout for your campaigns and system emails.</p>
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
          <div class="min-w-0 flex items-center gap-2.5">
            <div class="min-w-0">
              <p class="font-medium text-gray-800 truncate">{{ t.name }}</p>
              <p class="text-xs text-gray-400 truncate">{{ t.subject || 'No subject' }}</p>
            </div>
            <span v-if="t.slug" class="shrink-0 text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">System</span>
            <span v-if="t.slug && !t.is_active" class="shrink-0 text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">Inactive (fallback in use)</span>
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
            <div v-if="form.slug" class="flex items-center gap-2 bg-blue-50 border border-blue-100 text-blue-700 text-xs px-3 py-2 rounded-xl">
              <span class="font-semibold uppercase tracking-wide">System template</span>
              <code class="font-mono">{{ form.slug }}</code>
              <span class="text-blue-500">— used automatically for this system email. Deactivate below to fall back to the built-in copy.</span>
            </div>
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
            <div v-if="form.slug" class="flex items-center gap-2">
              <input id="is_active" v-model="form.is_active" type="checkbox" class="accent-[#234ecc]" />
              <label for="is_active" class="text-sm text-gray-600">Active (unchecking forces the hardcoded fallback copy for this email)</label>
            </div>

            <!-- Merge-tag palette — copy to clipboard, scoped to this template's slug -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Personalization tags</label>
              <div class="flex flex-wrap gap-1.5">
                <button v-for="tag in availableTags" :key="tag" type="button" @click="copyTag(tag)"
                  class="px-2 py-1 rounded-full bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] font-mono text-[11px] transition-colors">
                  {{ tagLabel(tag) }}
                </button>
              </div>
              <p v-if="copiedTag" class="text-[11px] text-emerald-600 mt-1">Copied {{ tagLabel(copiedTag) }} — paste it into a block field.</p>
              <p v-else class="text-[11px] text-gray-400 mt-1">Click a tag to copy it, then paste into a text/header/button field above.</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Content</label>
              <EmailBlockEditor v-if="features.isEnabled('email_template_editor')" v-model="form.content_blocks" @error="formError = $event" />
              <template v-else>
                <textarea v-model="form.html_body" rows="16" spellcheck="false"
                  placeholder="<h1>Hello!</h1><p>Your message…</p>"
                  class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y" />
                <p class="text-[11px] text-gray-400 mt-1">Raw HTML. An unsubscribe footer is appended automatically when sent.</p>
              </template>
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
            <p class="text-[11px] text-gray-400 mt-1">Sends the current subject + body (with sample personalization data) to one address. Configure SMTP in Email Settings first (in dev it prints to the server log).</p>
          </div>
        </div>

        <!-- Preview — rendered in a sandboxed iframe (scripts disabled, isolated
             origin) so authored HTML can never run JS in the admin's session. -->
        <div class="space-y-2">
          <p class="text-sm font-medium text-gray-700">Preview <span class="text-gray-400 font-normal">(sample data)</span></p>
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
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { useFeaturesStore } from '@/stores/features'
import EmailBlockEditor from '@/components/blocks/EmailBlockEditor.vue'
import { MERGE_TAG_CATALOGUE } from '@/components/blocks/emailBlockKit'

const features = useFeaturesStore()

const items = ref([])
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({ id: null, name: '', slug: '', subject: '', html_body: '', content_blocks: [], is_active: true })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')

const deleteTarget = ref(null)
const deleting = ref(false)

const testEmail = ref('')
const testing = ref(false)
const testMsg = ref('')
const testOk = ref(false)

const copiedTag = ref('')

const availableTags = computed(() => {
  const scope = form.slug && MERGE_TAG_CATALOGUE[form.slug] ? form.slug : 'automation'
  return [...MERGE_TAG_CATALOGUE.universal, ...(MERGE_TAG_CATALOGUE[scope] || [])]
})

// Kept as a function (not inlined in the template) — writing literal {{ }}
// characters directly inside a Vue mustache interpolation confuses the SFC
// compiler's delimiter scanner.
function tagLabel(tag) {
  return `{{${tag}}}`
}

async function copyTag(tag) {
  try {
    await navigator.clipboard.writeText(tagLabel(tag))
  } catch { /* clipboard unavailable — chip still shows the tag to copy manually */ }
  copiedTag.value = tag
  setTimeout(() => { if (copiedTag.value === tag) copiedTag.value = '' }, 2000)
}

const previewDoc = ref('<p style="color:#bbb;font-family:system-ui">Nothing to preview yet.</p>')

async function refreshPreview() {
  if (features.isEnabled('email_template_editor')) {
    if (!form.content_blocks.length) {
      previewDoc.value = '<p style="color:#bbb;font-family:system-ui">Nothing to preview yet.</p>'
      return
    }
    try {
      const { html } = await adminApi.previewEmailTemplate({ content_blocks: form.content_blocks })
      previewDoc.value = html || '<p style="color:#bbb;font-family:system-ui">Nothing to preview yet.</p>'
    } catch {
      previewDoc.value = '<p style="color:#c00;font-family:system-ui">Preview failed.</p>'
    }
  } else {
    previewDoc.value = form.html_body || '<p style="color:#bbb;font-family:system-ui">Nothing to preview yet.</p>'
  }
}

let previewTimer = null
watch(() => [form.content_blocks, form.html_body], () => {
  clearTimeout(previewTimer)
  previewTimer = setTimeout(refreshPreview, 400)
}, { deep: true })

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
  Object.assign(form, { id: null, name: '', slug: '', subject: '', html_body: '', content_blocks: [], is_active: true })
  formError.value = ''; saved.value = false; editing.value = true
  refreshPreview()
}

async function startEdit(row) {
  formError.value = ''; saved.value = false
  try {
    const t = await adminApi.getEmailTemplate(row.id)
    Object.assign(form, {
      id: t.id, name: t.name, slug: t.slug || '', subject: t.subject,
      html_body: t.html_body, content_blocks: t.content_blocks || [], is_active: t.is_active !== false,
    })
    editing.value = true
    refreshPreview()
  } catch { error.value = 'Could not open that template.' }
}

async function save() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = 'A name is required.'; return }
  saving.value = true
  try {
    const payload = {
      name: form.name.trim(), subject: form.subject.trim(), is_active: form.is_active,
      ...(features.isEnabled('email_template_editor')
        ? { content_blocks: form.content_blocks.map(b => ({ type: b.type, body: { ...b.body } })) }
        : { html_body: form.html_body }),
    }
    if (!form.id) payload.slug = form.slug.trim()
    const t = form.id
      ? await adminApi.updateEmailTemplate(form.id, payload)
      : await adminApi.createEmailTemplate(payload)
    form.id = t.id
    form.html_body = t.html_body
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.name || e?.response?.data?.content_blocks || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doTest() {
  testing.value = true; testMsg.value = ''
  try {
    let html_body = form.html_body
    if (features.isEnabled('email_template_editor') && form.content_blocks.length) {
      const preview = await adminApi.previewEmailTemplate({ content_blocks: form.content_blocks })
      html_body = preview.html
    }
    await adminApi.testSendEmail({
      email: testEmail.value.trim(),
      subject: form.subject,
      html_body,
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
