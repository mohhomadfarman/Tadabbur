<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Announcements</h1>
          <p class="text-gray-400 text-sm mt-0.5">Pop-up modals shown to logged-in users (once each).</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New announcement
        </button>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 4" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No announcements yet</p>
        <p class="text-gray-400 text-sm">Create one to greet users when they open the app.</p>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-x-auto shadow-sm">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-100 text-xs text-gray-400 uppercase tracking-wider">
              <th class="px-5 py-3 text-left font-medium">Title</th>
              <th class="px-4 py-3 text-left font-medium">Status</th>
              <th class="px-4 py-3 text-left font-medium hidden sm:table-cell">Schedule</th>
              <th class="px-4 py-3 text-right font-medium">Views</th>
              <th class="px-4 py-3 text-right font-medium hidden sm:table-cell">Dismissed</th>
              <th class="px-4 py-3 text-right font-medium w-px"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in items" :key="a.id" class="border-b border-gray-50 last:border-0 hover:bg-gray-50/60 transition-colors cursor-pointer" @click="startEdit(a)">
              <td class="px-5 py-3 font-medium text-gray-800">
                {{ a.title }}
                <span class="text-gray-300 ms-1">· {{ a.block_count }} block{{ a.block_count === 1 ? '' : 's' }}</span>
              </td>
              <td class="px-4 py-3">
                <span v-if="a.is_active" class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700">Active</span>
                <span v-else class="text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">Off</span>
              </td>
              <td class="px-4 py-3 text-gray-500 text-xs hidden sm:table-cell">{{ scheduleLabel(a) }}</td>
              <td class="px-4 py-3 text-right font-semibold text-gray-700">{{ a.views }}</td>
              <td class="px-4 py-3 text-right text-gray-500 hidden sm:table-cell">{{ a.dismissed }}</td>
              <td class="px-4 py-3 text-right">
                <button @click.stop="deleteTarget = a" title="Delete" class="w-8 h-8 rounded-lg inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </td>
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
          <button :disabled="saving" @click="save"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : (form.id ? 'Save' : 'Create') }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Content -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
            <input v-model="form.title" type="text" placeholder="e.g. We've gone live! 🎉"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <BlockEditor v-model="form.content_blocks" @error="formError = $event" />
        </div>

        <!-- Settings -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Active</p>
                <p class="text-xs text-gray-400 mt-0.5">Show to users when on.</p>
              </div>
              <button type="button" @click="form.is_active = !form.is_active"
                class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
                :class="form.is_active ? 'bg-[#234ecc]' : 'bg-gray-300'">
                <span class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                  :class="form.is_active ? 'translate-x-4' : 'translate-x-1'" />
              </button>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Priority</label>
              <input v-model.number="form.priority" type="number"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <p class="text-[11px] text-gray-400 mt-1">Higher shows first when several are queued.</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Show from</label>
              <input v-model="form.starts_at" type="datetime-local"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Show until</label>
              <input v-model="form.ends_at" type="datetime-local"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <p class="text-[11px] text-gray-400 mt-1">Leave both blank to show indefinitely. Times are UTC.</p>
            </div>

            <div v-if="form.id" class="pt-3 border-t border-gray-100 text-xs text-gray-400 space-y-1">
              <p>Views: <span class="text-gray-700 font-semibold">{{ form.views }}</span></p>
              <p>Dismissed: <span class="text-gray-700 font-semibold">{{ form.dismissed }}</span></p>
            </div>

            <button v-if="form.id" @click="deleteTarget = { id: form.id, title: form.title }"
              class="w-full text-sm text-red-500 hover:text-red-600 border border-red-200 hover:bg-red-50 rounded-xl py-2 transition-colors">
              Delete announcement
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete announcement?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.title }}</strong> will be removed. Its view records go too.</p>
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
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import BlockEditor from '@/components/blocks/BlockEditor.vue'

const items = ref([])
const loading = ref(true)
const error = ref('')

const editing = ref(null)   // null = list; truthy = editor open
const form = reactive({ id: null, title: '', is_active: false, priority: 0, starts_at: '', ends_at: '', content_blocks: [], views: 0, dismissed: 0 })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')

const deleteTarget = ref(null)
const deleting = ref(false)

function toLocalInput(iso) {
  return iso ? String(iso).slice(0, 16) : ''
}

function scheduleLabel(a) {
  if (!a.starts_at && !a.ends_at) return 'Always'
  const fmt = (iso) => iso ? String(iso).slice(0, 16).replace('T', ' ') : '…'
  return `${fmt(a.starts_at)} → ${fmt(a.ends_at)}`
}

async function load() {
  loading.value = true
  try {
    items.value = await adminApi.listAnnouncements()
  } catch {
    error.value = 'Could not load announcements. Make sure your account has Announcements access.'
  } finally {
    loading.value = false
  }
}

function startNew() {
  Object.assign(form, { id: null, title: '', is_active: false, priority: 0, starts_at: '', ends_at: '', content_blocks: [], views: 0, dismissed: 0 })
  formError.value = ''
  saved.value = false
  editing.value = true
}

async function startEdit(row) {
  formError.value = ''
  saved.value = false
  try {
    const a = await adminApi.getAnnouncement(row.id)
    Object.assign(form, {
      id: a.id,
      title: a.title,
      is_active: a.is_active,
      priority: a.priority || 0,
      starts_at: toLocalInput(a.starts_at),
      ends_at: toLocalInput(a.ends_at),
      content_blocks: (a.content_blocks || []).map(b => ({ type: b.type, body: { ...b.body } })),
      views: a.views || 0,
      dismissed: a.dismissed || 0,
    })
    editing.value = true
  } catch {
    error.value = 'Could not open that announcement.'
  }
}

async function save() {
  formError.value = ''
  if (!form.title.trim()) { formError.value = 'A title is required.'; return }
  saving.value = true
  try {
    const payload = {
      title: form.title.trim(),
      is_active: form.is_active,
      priority: form.priority || 0,
      starts_at: form.starts_at || '',
      ends_at: form.ends_at || '',
      content_blocks: form.content_blocks.map(b => ({ type: b.type, body: b.body })),
    }
    const saved_a = form.id
      ? await adminApi.updateAnnouncement(form.id, payload)
      : await adminApi.createAnnouncement(payload)
    form.id = saved_a.id
    form.views = saved_a.views || 0
    form.dismissed = saved_a.dismissed || 0
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.content_blocks || e?.response?.data?.title || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteAnnouncement(deleteTarget.value.id)
    if (form.id === deleteTarget.value.id) editing.value = null
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Could not delete this announcement.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>
