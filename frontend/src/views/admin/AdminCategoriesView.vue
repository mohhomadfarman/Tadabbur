<template>
  <div class="px-6 py-8 max-w-3xl mx-auto">

    <!-- ── LIST MODE ─────────────────────────────────────────────── -->
    <template v-if="!editing">
      <div class="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Categories</h1>
          <p class="text-gray-400 text-sm mt-0.5">Group tracks into categories, each with its own levels (e.g. Beginner/Intermediate/Advanced).</p>
        </div>
        <button @click="startNew"
          class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
          New category
        </button>
      </div>

      <!-- Learn page banner (powers the public /learn page hero) -->
      <details v-if="features.isEnabled('learn_page_media')" class="bg-white border border-gray-200 rounded-2xl shadow-sm mb-8" open>
        <summary class="flex items-center justify-between gap-3 px-5 py-4 cursor-pointer select-none">
          <div>
            <h2 class="font-semibold text-gray-800">Learn page banner</h2>
            <p class="text-xs text-gray-400 mt-0.5">Background image shown behind the header on the <span class="font-mono">/learn</span> page.</p>
          </div>
          <span v-if="bannerSaved" class="text-xs text-emerald-600 font-semibold shrink-0">Saved ✓</span>
        </summary>
        <div class="px-5 pb-5 border-t border-gray-100 pt-5">

          <!-- Live preview — mirrors the actual /learn hero styling -->
          <div
            class="rounded-xl overflow-hidden relative px-6 py-10 mb-4 bg-gray-100 bg-cover bg-center"
            :style="bannerForm.banner_image ? { backgroundImage: `url(${bannerForm.banner_image})` } : {}"
          >
            <p v-if="!bannerForm.banner_image" class="text-xs text-gray-400">No banner image — upload one below to preview.</p>
            <template v-else>
              <h3
                class="font-bold mb-1"
                :style="{
                  color: bannerForm.banner_text_color,
                  fontSize: bannerForm.banner_font_size + 'px',
                  textShadow: bannerForm.banner_text_shadow ? '0 1px 6px rgba(0,0,0,.55)' : 'none',
                }"
              >{{ bannerForm.banner_title || 'Learning Tracks' }}</h3>
              <p
                :style="{
                  color: bannerForm.banner_text_color,
                  opacity: 0.9,
                  fontSize: Math.max(14, Math.round(bannerForm.banner_font_size * 0.45)) + 'px',
                  textShadow: bannerForm.banner_text_shadow ? '0 1px 6px rgba(0,0,0,.55)' : 'none',
                }"
              >{{ bannerForm.banner_subtitle || 'Choose a field of Islamic knowledge to begin your journey.' }}</p>
            </template>
          </div>

          <div class="flex items-center gap-4">
            <div class="w-32 h-20 rounded-xl overflow-hidden bg-gray-100 border border-gray-100 flex items-center justify-center shrink-0">
              <img v-if="bannerForm.banner_image" :src="bannerForm.banner_image" class="w-full h-full object-cover" />
              <span v-else class="text-xs text-gray-300">No banner</span>
            </div>
            <div class="flex flex-col gap-2">
              <label class="text-xs font-medium text-[#234ecc] hover:underline cursor-pointer">
                {{ bannerUploading ? 'Uploading…' : 'Upload image' }}
                <input type="file" accept="image/*" class="hidden" @change="onBannerUpload" :disabled="bannerUploading" />
              </label>
              <button v-if="bannerForm.banner_image" type="button" @click="bannerForm.banner_image = ''"
                class="text-xs text-gray-400 hover:text-red-500 text-left transition-colors">Remove banner</button>
            </div>
          </div>
          <div class="mt-4 grid sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Title</label>
              <input v-model="bannerForm.banner_title" type="text" maxlength="200"
                placeholder="Defaults to &quot;Learning Tracks&quot;"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Subtitle</label>
              <input v-model="bannerForm.banner_subtitle" type="text" maxlength="300"
                placeholder="Defaults to the standard subtitle"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
          </div>

          <!-- Text styling -->
          <div class="mt-4 grid sm:grid-cols-3 gap-4 items-end">
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Text color</label>
              <div class="flex items-center gap-2">
                <input v-model="bannerForm.banner_text_color" type="color"
                  class="w-10 h-10 rounded-lg border border-gray-200 cursor-pointer p-0.5 shrink-0" />
                <input v-model="bannerForm.banner_text_color" type="text" maxlength="20"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              </div>
            </div>
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Title font size ({{ bannerForm.banner_font_size }}px)</label>
              <input v-model.number="bannerForm.banner_font_size" type="range" min="16" max="56" step="1"
                class="w-full cursor-pointer" />
            </div>
            <div>
              <label class="inline-flex items-center gap-2 text-sm text-gray-700 cursor-pointer select-none py-2">
                <input v-model="bannerForm.banner_text_shadow" type="checkbox"
                  class="w-4 h-4 rounded border-gray-300 text-[#234ecc] focus:ring-[#234ecc]/40" />
                Text shadow
              </label>
            </div>
          </div>

          <div class="mt-4 flex flex-wrap items-center gap-3">
            <button @click="saveBannerSettings" :disabled="bannerSaving"
              class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors">
              {{ bannerSaving ? 'Saving…' : 'Save banner' }}
            </button>
            <span v-if="bannerError" class="text-xs text-red-600">{{ bannerError }}</span>
          </div>
        </div>
      </details>

      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

      <div v-if="loading" class="space-y-2 animate-pulse">
        <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-xl h-16" />
      </div>

      <div v-else-if="items.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
        <p class="text-gray-600 font-semibold mb-1">No categories yet</p>
        <p class="text-gray-400 text-sm">Create one to organize tracks on the Curriculum page and /learn.</p>
      </div>

      <div v-else class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm divide-y divide-gray-50">
        <button v-for="c in items" :key="c.id" @click="startEdit(c)"
          class="w-full text-left px-5 py-4 hover:bg-gray-50/60 transition-colors flex items-center justify-between gap-4">
          <div class="min-w-0">
            <p class="font-medium text-gray-800 truncate">{{ c.title }}</p>
            <p class="text-xs text-gray-400 truncate mt-0.5">
              {{ c.levels.length ? c.levels.map(l => l.name).join(', ') : 'No levels yet' }}
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
          <button v-if="form.id" @click="deleteTarget = { id: form.id, title: form.title }"
            class="text-sm text-red-500 hover:text-red-600 px-3 py-2 transition-colors">Delete</button>
          <button :disabled="saving" @click="save"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : (form.id ? 'Save' : 'Create') }}
          </button>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
          <input v-model="form.title" type="text" placeholder="e.g. Quran Studies"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        </div>

        <div v-if="features.isEnabled('learn_page_media')">
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Icon</label>
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center overflow-hidden shrink-0">
              <img v-if="form.icon_url" :src="form.icon_url" class="w-full h-full object-cover" />
              <svg v-else class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14M4 8h16M4 4h16v16H4V4z"/></svg>
            </div>
            <label class="text-xs font-medium text-[#234ecc] hover:underline cursor-pointer">
              {{ iconUploading ? 'Uploading…' : 'Upload image' }}
              <input type="file" accept="image/*" class="hidden" @change="onIconUpload" :disabled="iconUploading" />
            </label>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Display order</label>
          <input v-model.number="form.order" type="number" min="0"
            class="w-32 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        </div>

        <div>
          <div class="flex items-center justify-between mb-1.5">
            <label class="block text-sm font-medium text-gray-700">Levels</label>
            <button type="button" @click="addLevel" class="text-xs font-semibold text-[#234ecc] hover:text-[#1a3ba8]">+ Add level</button>
          </div>
          <p class="text-xs text-gray-400 mb-2">e.g. Beginner, Intermediate, Advanced — assigned to tracks from the track editor.</p>

          <div v-if="form.levels.length === 0" class="text-sm text-gray-400 border border-dashed border-gray-200 rounded-xl py-4 text-center">
            No levels yet — add one above.
          </div>
          <div v-for="(lvl, i) in form.levels" :key="i" class="flex items-center gap-2 mb-2">
            <input v-model="lvl.name" type="text" placeholder="Level name"
              class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            <button type="button" @click="form.levels.splice(i, 1)"
              class="w-9 h-9 shrink-0 rounded-lg text-gray-400 hover:text-red-500 hover:bg-red-50 flex items-center justify-center transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete category?</h3>
        <p class="text-sm text-gray-500 mb-5"><strong>{{ deleteTarget.title }}</strong> will be removed. Tracks still assigned to it will block the delete.</p>
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
import { useFeaturesStore } from '@/stores/features'

const features = useFeaturesStore()

const items = ref([])
const loading = ref(true)
const error = ref('')

const editing = ref(null)
const form = reactive({ id: null, title: '', order: 0, levels: [], icon_url: '' })
const saving = ref(false)
const saved = ref(false)
const formError = ref('')
const iconUploading = ref(false)

const deleteTarget = ref(null)
const deleting = ref(false)

const bannerForm = reactive({
  banner_image: '', banner_title: '', banner_subtitle: '',
  banner_text_color: '#ffffff', banner_font_size: 30, banner_text_shadow: false,
})
const bannerUploading = ref(false)
const bannerSaving = ref(false)
const bannerSaved = ref(false)
const bannerError = ref('')

let originalSlug = ''

async function load() {
  loading.value = true
  try {
    items.value = await adminApi.listCategories()
  } catch {
    error.value = 'Could not load categories. Make sure your account has Curriculum access.'
  } finally {
    loading.value = false
  }
}

function startNew() {
  Object.assign(form, { id: null, title: '', order: 0, levels: [], icon_url: '' })
  originalSlug = ''
  formError.value = ''; saved.value = false; editing.value = true
}

function addLevel() {
  form.levels.push({ name: '', slug: '' })
}

async function onIconUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  iconUploading.value = true
  try {
    const { upload_url, public_url } = await adminApi.getUploadUrl(file.name, file.type, 'category_icon')
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error('upload failed')
    form.icon_url = public_url
  } catch {
    formError.value = 'Image upload failed.'
  } finally {
    iconUploading.value = false
    e.target.value = ''
  }
}

async function loadBannerSettings() {
  try {
    const s = await adminApi.getLearnPageSettings()
    bannerForm.banner_image = s.banner_image || ''
    bannerForm.banner_title = s.banner_title || ''
    bannerForm.banner_subtitle = s.banner_subtitle || ''
    bannerForm.banner_text_color = s.banner_text_color || '#ffffff'
    bannerForm.banner_font_size = s.banner_font_size || 30
    bannerForm.banner_text_shadow = !!s.banner_text_shadow
  } catch { /* banner panel just shows empty — not worth surfacing an error here */ }
}

async function onBannerUpload(e) {
  const file = e.target.files?.[0]
  if (!file) return
  bannerUploading.value = true
  try {
    const { upload_url, public_url } = await adminApi.getUploadUrl(file.name, file.type, 'banner')
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error('upload failed')
    bannerForm.banner_image = public_url
  } catch {
    bannerError.value = 'Image upload failed.'
  } finally {
    bannerUploading.value = false
    e.target.value = ''
  }
}

async function saveBannerSettings() {
  bannerError.value = ''
  bannerSaving.value = true
  try {
    await adminApi.updateLearnPageSettings({
      banner_image: bannerForm.banner_image,
      banner_title: bannerForm.banner_title,
      banner_subtitle: bannerForm.banner_subtitle,
      banner_text_color: bannerForm.banner_text_color,
      banner_font_size: bannerForm.banner_font_size,
      banner_text_shadow: bannerForm.banner_text_shadow,
    })
    bannerSaved.value = true
    setTimeout(() => { bannerSaved.value = false }, 2500)
  } catch {
    bannerError.value = 'Could not save banner.'
  } finally {
    bannerSaving.value = false
  }
}

async function startEdit(row) {
  formError.value = ''; saved.value = false
  try {
    const c = await adminApi.getCategory(row.slug)
    Object.assign(form, {
      id: c.id, title: c.title, order: c.order,
      // Keep each level's existing slug (stable identity) — renaming `name`
      // shouldn't change which tracks it's assigned to. Only brand-new rows
      // (added via "+ Add level") get slug: '' so the backend generates one.
      levels: c.levels.map(l => ({ name: l.name, slug: l.slug })),
      icon_url: c.icon_url || '',
    })
    originalSlug = c.slug
    editing.value = true
  } catch { error.value = 'Could not open that category.' }
}

async function save() {
  formError.value = ''
  if (!form.title.trim()) { formError.value = 'A title is required.'; return }
  const levels = form.levels.filter(l => l.name.trim()).map(l => ({ name: l.name.trim(), slug: l.slug || undefined }))
  saving.value = true
  try {
    const payload = { title: form.title.trim(), order: form.order || 0, levels, icon_url: form.icon_url }
    const c = form.id
      ? await adminApi.updateCategory(originalSlug, payload)
      : await adminApi.createCategory(payload)
    form.id = c.id
    form.levels = c.levels.map(l => ({ name: l.name, slug: l.slug }))
    form.icon_url = c.icon_url || ''
    originalSlug = c.slug
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
    await load()
  } catch (e) {
    const data = e?.response?.data
    formError.value = (data && (data.title || data.levels || data.slug)) || 'Could not save.'
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  deleting.value = true
  try {
    await adminApi.deleteCategory(originalSlug)
    if (form.id === deleteTarget.value.id) editing.value = null
    deleteTarget.value = null
    await load()
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Could not delete this category.'
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  load()
  loadBannerSettings()
})
</script>
