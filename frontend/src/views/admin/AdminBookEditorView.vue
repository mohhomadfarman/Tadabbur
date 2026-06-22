<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Sticky top bar -->
    <div class="sticky top-0 z-10 bg-white/95 backdrop-blur border-b border-gray-200 -mx-6 px-6 py-3 flex items-center justify-between mb-8">
      <nav class="text-sm text-gray-400 flex items-center gap-2">
        <RouterLink :to="{ name: 'admin-library' }" class="hover:text-gray-600 transition-colors">Library</RouterLink>
        <span>/</span>
        <span class="text-gray-600">{{ isEdit ? 'Edit Book' : 'New Book' }}</span>
      </nav>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-500">{{ form.is_published ? 'Published' : 'Draft' }}</span>
          <button
            type="button"
            @click="form.is_published = !form.is_published"
            class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
            :class="form.is_published ? 'bg-[#234ecc]' : 'bg-gray-300'"
          >
            <span
              class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
              :class="form.is_published ? 'translate-x-4' : 'translate-x-1'"
            />
          </button>
        </div>
        <button
          type="button"
          :disabled="saving"
          @click="save"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Add Book') }}
        </button>
        <RouterLink :to="{ name: 'admin-library' }" class="text-sm text-gray-500 hover:text-gray-700 transition-colors">
          Cancel
        </RouterLink>
      </div>
    </div>

    <div v-if="loadingBook" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 bg-gray-100 rounded-2xl h-96" />
      <div class="bg-gray-100 rounded-2xl h-80" />
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left: book details -->
      <div class="lg:col-span-2 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">

        <div v-if="apiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
          {{ apiError }}
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
          <input
            v-model="form.title"
            @input="autofillSlug"
            type="text"
            required
            placeholder="e.g. Riyad as-Salihin"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug <span class="text-red-500">*</span></label>
          <div class="flex gap-2">
            <input
              v-model="form.slug"
              @input="slugWasEdited = true"
              type="text"
              required
              placeholder="e.g. riyad-as-salihin"
              class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
            <button
              type="button"
              @click="regenerateSlug"
              class="px-3 py-2.5 text-xs text-gray-500 border border-gray-200 rounded-xl hover:border-[#234ecc]/40 hover:text-[#234ecc] transition-colors"
            >
              Regenerate
            </button>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Author</label>
          <input
            v-model="form.author"
            type="text"
            placeholder="e.g. Imam al-Nawawi"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Description</label>
          <textarea
            v-model="form.description"
            rows="4"
            placeholder="Brief description of this book…"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Category</label>
            <input
              v-model="form.category"
              list="category-options"
              type="text"
              placeholder="e.g. Hadith"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
            <datalist id="category-options">
              <option v-for="c in CATEGORIES" :key="c" :value="c" />
            </datalist>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Language</label>
            <select
              v-model="form.language"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 bg-white"
            >
              <option value="en">English</option>
              <option value="ar">Arabic</option>
              <option value="ur">Urdu</option>
              <option value="fr">French</option>
              <option value="id">Indonesian</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Tags</label>
          <input
            v-model="tagsInput"
            type="text"
            placeholder="fiqh, sunnah, worship (comma-separated)"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
          />
          <p class="text-xs text-gray-400 mt-1">Comma-separated list of tags.</p>
        </div>

        <!-- Multi-volume books -->
        <div class="pt-2 border-t border-gray-100">
          <div class="flex items-start justify-between gap-4 mb-1">
            <div>
              <label class="block text-sm font-medium text-gray-700">Multi-volume book</label>
              <p class="text-xs text-gray-400 mt-0.5">Combine several PDF volumes (e.g. a tafsir) into one book.</p>
            </div>
            <button
              type="button"
              @click="toggleMultiVolume"
              class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors shrink-0 mt-1"
              :class="multiVolume ? 'bg-[#234ecc]' : 'bg-gray-300'"
            >
              <span
                class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                :class="multiVolume ? 'translate-x-4' : 'translate-x-1'"
              />
            </button>
          </div>

          <div v-if="multiVolume" class="space-y-3 mt-4">
            <div
              v-for="(vol, i) in form.volumes"
              :key="i"
              class="border border-gray-200 rounded-xl p-4 space-y-3 bg-gray-50/60"
            >
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold uppercase tracking-wider text-gray-400">Volume {{ i + 1 }}</span>
                <button
                  type="button"
                  @click="removeVolume(i)"
                  class="text-xs text-red-500 hover:text-red-600 hover:underline"
                >
                  Remove
                </button>
              </div>

              <div class="grid grid-cols-3 gap-3">
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">No.</label>
                  <input
                    v-model.number="vol.number"
                    type="number" min="1"
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                  />
                </div>
                <div class="col-span-2">
                  <label class="block text-xs font-medium text-gray-600 mb-1">Title</label>
                  <input
                    v-model="vol.title"
                    type="text"
                    placeholder="e.g. Al-Fatiha – Al-Baqarah"
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                  />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">Pages</label>
                  <input
                    v-model.number="vol.page_count"
                    type="number" min="0"
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                  />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-1">Size (MB)</label>
                  <input
                    v-model.number="vol.file_size_mb"
                    type="number" min="0" step="0.1"
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                  />
                </div>
              </div>

              <!-- Volume PDF upload -->
              <div class="border border-dashed border-gray-200 rounded-lg p-3 space-y-2 bg-white">
                <p v-if="vol.pdf_key" class="text-xs text-gray-500 truncate">{{ fileBasename(vol.pdf_key) }}</p>
                <p v-if="volUploading[i]" class="text-xs text-[#234ecc] animate-pulse">Uploading…</p>
                <p v-if="volUploaded[i]" class="text-xs text-emerald-600 flex items-center gap-1">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                  Uploaded
                </p>
                <input
                  :ref="el => (volInputs[i] = el)"
                  type="file" accept="application/pdf" class="hidden"
                  @change="handleVolumeUpload(i, $event)"
                />
                <button
                  type="button"
                  @click="volInputs[i]?.click()"
                  :disabled="volUploading[i]"
                  class="text-xs text-gray-500 border border-gray-200 px-3 py-1.5 rounded-lg hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-50 transition-colors"
                >
                  {{ vol.pdf_key ? 'Replace PDF' : 'Upload PDF' }}
                </button>
              </div>
            </div>

            <button
              type="button"
              @click="addVolume"
              class="w-full border border-dashed border-gray-300 rounded-xl py-2.5 text-sm font-medium text-gray-500 hover:border-[#234ecc]/40 hover:text-[#234ecc] transition-colors"
            >
              + Add volume
            </button>
          </div>
        </div>

      </div>

      <!-- Right: publish + files -->
      <div class="lg:col-span-1 lg:sticky lg:top-24 space-y-4">
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-5">

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Order</label>
              <input
                v-model.number="form.order"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Size (MB)</label>
              <input
                v-model.number="form.file_size_mb"
                type="number" min="0" step="0.1"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Pages</label>
            <input
              v-model.number="form.page_count"
              type="number" min="0"
              class="w-32 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
          </div>

          <!-- Cover upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Cover Image</label>
            <div class="border border-dashed border-gray-200 rounded-xl p-4 space-y-2">
              <p v-if="form.cover_key" class="text-xs text-gray-500 truncate">{{ fileBasename(form.cover_key) }}</p>
              <p v-if="uploading.cover" class="text-xs text-[#234ecc] animate-pulse">Uploading…</p>
              <p v-if="uploaded.cover" class="text-xs text-emerald-600 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Uploaded
              </p>
              <input ref="coverInput" type="file" accept="image/*" class="hidden" @change="handleUpload('cover', 'book_cover', $event)" />
              <button type="button" @click="coverInput.click()" :disabled="uploading.cover"
                class="text-xs text-gray-500 border border-gray-200 px-3 py-1.5 rounded-lg hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-50 transition-colors">
                Choose File
              </button>
            </div>
          </div>

          <!-- PDF upload (single-volume books only) -->
          <div v-if="!multiVolume">
            <label class="block text-sm font-medium text-gray-700 mb-2">PDF File</label>
            <div class="border border-dashed border-gray-200 rounded-xl p-4 space-y-2">
              <p v-if="form.pdf_key" class="text-xs text-gray-500 truncate">{{ fileBasename(form.pdf_key) }}</p>
              <p v-if="uploading.pdf" class="text-xs text-[#234ecc] animate-pulse">Uploading…</p>
              <p v-if="uploaded.pdf" class="text-xs text-emerald-600 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Uploaded
              </p>
              <input ref="pdfInput" type="file" accept="application/pdf" class="hidden" @change="handleUpload('pdf', 'book_pdf', $event)" />
              <button type="button" @click="pdfInput.click()" :disabled="uploading.pdf"
                class="text-xs text-gray-500 border border-gray-200 px-3 py-1.5 rounded-lg hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-50 transition-colors">
                Choose File
              </button>
            </div>
          </div>

          <!-- Audio upload (optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Audio File
              <span class="text-gray-400 font-normal ml-1">(optional)</span>
            </label>
            <div class="border border-dashed border-gray-200 rounded-xl p-4 space-y-2">
              <p v-if="form.audio_key" class="text-xs text-gray-500 truncate">{{ fileBasename(form.audio_key) }}</p>
              <p v-if="uploading.audio" class="text-xs text-[#234ecc] animate-pulse">Uploading…</p>
              <p v-if="uploaded.audio" class="text-xs text-emerald-600 flex items-center gap-1">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Uploaded
              </p>
              <input ref="audioInput" type="file" accept="audio/*" class="hidden" @change="handleUpload('audio', 'book_audio', $event)" />
              <button type="button" @click="audioInput.click()" :disabled="uploading.audio"
                class="text-xs text-gray-500 border border-gray-200 px-3 py-1.5 rounded-lg hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-50 transition-colors">
                Choose File
              </button>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const CATEGORIES = ['Fiqh', 'Aqeedah', 'Seerah', 'Hadith', 'Quran', 'Arabic', 'Other']

const form = ref({
  title: '',
  slug: '',
  author: '',
  description: '',
  category: '',
  language: 'en',
  order: 0,
  file_size_mb: null,
  page_count: null,
  is_published: false,
  cover_key: '',
  pdf_key: '',
  audio_key: '',
  volumes: [],
})
const tagsInput = ref('')

const loadingBook = ref(false)
const saving = ref(false)
const apiError = ref('')
let slugWasEdited = false

const uploading = reactive({ cover: false, pdf: false, audio: false })
const uploaded = reactive({ cover: false, pdf: false, audio: false })

const coverInput = ref(null)
const pdfInput = ref(null)
const audioInput = ref(null)

// ── Multi-volume ───────────────────────────────────────────────────────────
const multiVolume = ref(false)
const volInputs = {}                      // per-row <input type=file> element refs
const volUploading = reactive({})         // per-row upload-in-progress flags
const volUploaded = reactive({})          // per-row upload-done flags

function toggleMultiVolume() {
  multiVolume.value = !multiVolume.value
  if (multiVolume.value && form.value.volumes.length === 0) addVolume()
}

function addVolume() {
  form.value.volumes.push({
    number: form.value.volumes.length + 1,
    title: '',
    pdf_key: '',
    page_count: null,
    file_size_mb: null,
  })
}

function removeVolume(index) {
  form.value.volumes.splice(index, 1)
  // Transient upload flags are index-keyed; reset them after a reorder.
  Object.keys(volUploading).forEach(k => delete volUploading[k])
  Object.keys(volUploaded).forEach(k => delete volUploaded[k])
}

async function handleVolumeUpload(index, event) {
  const file = event.target.files?.[0]
  if (!file) return
  volUploading[index] = true
  volUploaded[index] = false
  try {
    const { upload_url, key } = await adminApi.getUploadUrl(file.name, file.type, 'book_pdf')
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    form.value.volumes[index].pdf_key = key
    form.value.volumes[index].file_size_mb = Math.round((file.size / (1024 * 1024)) * 10) / 10
    volUploaded[index] = true
  } catch {
    apiError.value = `Failed to upload volume ${index + 1} PDF.`
  } finally {
    volUploading[index] = false
  }
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (!slugWasEdited) form.value.slug = slugify(form.value.title)
}

function regenerateSlug() {
  form.value.slug = slugify(form.value.title)
  slugWasEdited = false
}

function fileBasename(key) {
  if (!key) return ''
  return key.split('/').pop()
}

async function handleUpload(field, folder, event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploading[field] = true
  uploaded[field] = false
  try {
    const { upload_url, key } = await adminApi.getUploadUrl(file.name, file.type, folder)
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    form.value[`${field}_key`] = key
    uploaded[field] = true
  } catch {
    apiError.value = `Failed to upload ${field} file.`
  } finally {
    uploading[field] = false
  }
}

async function save() {
  apiError.value = ''
  saving.value = true
  try {
    const payload = {
      ...form.value,
      tags: tagsInput.value.split(',').map(t => t.trim()).filter(Boolean),
      // Only persist volumes that actually have a PDF; clear them when the
      // multi-volume toggle is off so single-PDF books fall back to pdf_key.
      volumes: multiVolume.value
        ? form.value.volumes
            .filter(v => v.pdf_key)
            .map((v, i) => ({
              number: v.number || i + 1,
              title: (v.title || '').trim(),
              pdf_key: v.pdf_key,
              page_count: v.page_count || 0,
              file_size_mb: v.file_size_mb || 0,
            }))
        : [],
    }
    if (isEdit.value) {
      await adminApi.updateBook(route.params.slug, payload)
    } else {
      await adminApi.createBook(payload)
    }
    router.push({ name: 'admin-library' })
  } catch (e) {
    const data = e.response?.data
    apiError.value = typeof data === 'object'
      ? Object.values(data).flat().join(' ')
      : 'Could not save book.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (!isEdit.value) return
  loadingBook.value = true
  try {
    const data = await adminApi.getBook(route.params.slug)
    form.value = {
      title: data.title,
      slug: data.slug,
      author: data.author || '',
      description: data.description || '',
      category: data.category || '',
      language: data.language || 'en',
      order: data.order ?? 0,
      file_size_mb: data.file_size_mb ?? null,
      page_count: data.page_count ?? null,
      is_published: data.is_published,
      cover_key: data.cover_key || '',
      pdf_key: data.pdf_key || '',
      audio_key: data.audio_key || '',
      volumes: (data.volumes || []).map(v => ({
        number: v.number,
        title: v.title || '',
        pdf_key: v.pdf_key || '',
        page_count: v.page_count ?? null,
        file_size_mb: v.file_size_mb ?? null,
      })),
    }
    multiVolume.value = (data.volumes?.length || 0) > 0
    tagsInput.value = (data.tags || []).join(', ')
    slugWasEdited = true
  } finally {
    loadingBook.value = false
  }
})
</script>
