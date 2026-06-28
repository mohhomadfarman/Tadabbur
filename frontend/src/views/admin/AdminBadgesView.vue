<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Badges &amp; Rewards</h1>
          <p class="text-gray-400 text-sm mt-0.5">Achievements awarded to learners, with a celebration popup.</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New badge
        </button>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 4" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No badges yet</p>
        <p class="text-gray-400 text-sm">Create one to reward learners for milestones.</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <button v-for="b in items" :key="b.id" @click="startEdit(b)"
          class="text-left bg-white border border-gray-200 rounded-2xl p-4 shadow-sm hover:border-[#234ecc]/40 transition-colors flex items-center gap-4">
          <div class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden shrink-0">
            <img v-if="b.icon_url" :src="b.icon_url" class="w-full h-full object-cover" />
            <svg v-else class="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 15a5 5 0 1 0 0-10 5 5 0 0 0 0 10z"/><path d="m8.5 13.5-1.8 7.5L12 18l5.3 3-1.8-7.5"/></svg>
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
              <p class="font-semibold text-gray-800 truncate">{{ b.name }}</p>
              <span v-if="!b.is_active" class="text-[11px] font-semibold px-1.5 py-0.5 rounded-full bg-gray-100 text-gray-500">Off</span>
            </div>
            <p class="text-xs text-gray-400 mt-0.5">{{ criteriaLabel(b) }} · {{ b.awarded_count }} earned</p>
          </div>
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
          <button :disabled="saving" @click="save"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : (form.id ? 'Save' : 'Create') }}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Name <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text" placeholder="e.g. First Steps"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Description</label>
              <textarea v-model="form.description" rows="2" placeholder="What this badge celebrates."
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Reward text</label>
              <input v-model="form.reward" type="text" placeholder="e.g. You earned a gold star!"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
          </div>
        </div>

        <!-- Settings -->
        <div class="lg:col-span-1 space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
            <!-- Icon -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Icon</label>
              <div class="flex items-center gap-3">
                <div class="w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden shrink-0">
                  <img v-if="form.icon_url" :src="form.icon_url" class="w-full h-full object-cover" />
                  <svg v-else class="w-7 h-7 text-amber-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 15a5 5 0 1 0 0-10 5 5 0 0 0 0 10z"/><path d="m8.5 13.5-1.8 7.5L12 18l5.3 3-1.8-7.5"/></svg>
                </div>
                <label class="text-xs font-medium text-[#234ecc] hover:underline cursor-pointer">
                  {{ uploading ? 'Uploading…' : 'Upload image' }}
                  <input type="file" accept="image/*" class="hidden" @change="onIconUpload" :disabled="uploading" />
                </label>
              </div>
            </div>

            <!-- Active -->
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-700">Active</p>
                <p class="text-xs text-gray-400 mt-0.5">Eligible to be awarded.</p>
              </div>
              <button type="button" @click="form.is_active = !form.is_active"
                class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
                :class="form.is_active ? 'bg-[#234ecc]' : 'bg-gray-300'">
                <span class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                  :class="form.is_active ? 'translate-x-4' : 'translate-x-1'" />
              </button>
            </div>

            <!-- Criteria -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Awarded when</label>
              <select v-model="form.criteria_type"
                class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
                <option value="manual">Granted manually</option>
                <option value="track_complete">A track is completed</option>
                <option value="lessons_count">N lessons completed</option>
                <option value="streak">N-day streak reached</option>
              </select>
            </div>

            <div v-if="form.criteria_type === 'track_complete'">
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Track slug</label>
              <input v-model="form.criteria_value" type="text" placeholder="e.g. seerah-foundations"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div v-else-if="form.criteria_type === 'lessons_count' || form.criteria_type === 'streak'">
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                {{ form.criteria_type === 'streak' ? 'Streak days' : 'Lessons' }}
              </label>
              <input v-model="form.criteria_value" type="number" min="1"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>

            <div v-if="form.id" class="pt-3 border-t border-gray-100 text-xs text-gray-400">
              <p>Earned by: <span class="text-gray-700 font-semibold">{{ form.awarded_count }}</span> learners</p>
            </div>

            <button v-if="form.id" @click="deleteTarget = { id: form.id, name: form.name }"
              class="w-full text-sm text-red-500 hover:text-red-600 border border-red-200 hover:bg-red-50 rounded-xl py-2 transition-colors">
              Delete badge
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete badge?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.name }}</strong> will be removed, along with every learner's award of it.</p>
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

const items = ref([])
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({ id: null, name: '', description: '', icon_url: '', criteria_type: 'manual', criteria_value: '', reward: '', is_active: true, awarded_count: 0 })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')
const uploading = ref(false)

const deleteTarget = ref(null)
const deleting = ref(false)

const CRITERIA_LABELS = {
  manual: 'Manual',
  track_complete: 'Track completed',
  lessons_count: 'Lessons completed',
  streak: 'Streak reached',
}
function criteriaLabel(b) {
  const base = CRITERIA_LABELS[b.criteria_type] || b.criteria_type
  return b.criteria_value ? `${base} (${b.criteria_value})` : base
}

async function load() {
  loading.value = true
  try {
    items.value = await adminApi.listBadges()
  } catch {
    error.value = 'Could not load badges. Make sure your account has Badges access.'
  } finally {
    loading.value = false
  }
}

function reset() {
  Object.assign(form, { id: null, name: '', description: '', icon_url: '', criteria_type: 'manual', criteria_value: '', reward: '', is_active: true, awarded_count: 0 })
  formError.value = ''
  saved.value = false
}

function startNew() {
  reset()
  editing.value = true
}

async function startEdit(row) {
  reset()
  try {
    const b = await adminApi.getBadge(row.id)
    Object.assign(form, {
      id: b.id, name: b.name, description: b.description, icon_url: b.icon_url,
      criteria_type: b.criteria_type, criteria_value: b.criteria_value, reward: b.reward,
      is_active: b.is_active, awarded_count: b.awarded_count || 0,
    })
    editing.value = true
  } catch {
    error.value = 'Could not open that badge.'
  }
}

async function onIconUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const { upload_url, public_url } = await adminApi.getUploadUrl(file.name, file.type, 'image')
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error('upload failed')
    form.icon_url = public_url
  } catch {
    formError.value = 'Image upload failed.'
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}

async function save() {
  formError.value = ''
  if (!form.name.trim()) { formError.value = 'A name is required.'; return }
  saving.value = true
  try {
    const payload = {
      name: form.name.trim(),
      description: form.description.trim(),
      icon_url: form.icon_url,
      criteria_type: form.criteria_type,
      criteria_value: String(form.criteria_value || '').trim(),
      reward: form.reward.trim(),
      is_active: form.is_active,
    }
    const b = form.id
      ? await adminApi.updateBadge(form.id, payload)
      : await adminApi.createBadge(payload)
    form.id = b.id
    form.awarded_count = b.awarded_count || 0
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    formError.value = e?.response?.data?.key || e?.response?.data?.name || e?.response?.data?.criteria_type || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteBadge(deleteTarget.value.id)
    if (form.id === deleteTarget.value.id) editing.value = null
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Could not delete this badge.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(load)
</script>
