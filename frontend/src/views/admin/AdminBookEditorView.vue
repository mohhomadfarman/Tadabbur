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

          <!-- PDF upload / GDrive -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">PDF File</label>

            <!-- Source toggle -->
            <div class="flex rounded-lg border border-gray-200 overflow-hidden mb-3 text-xs font-medium">
              <button type="button"
                @click="pdfSource = 'upload'"
                class="flex-1 py-1.5 transition-colors"
                :class="pdfSource === 'upload' ? 'bg-[#234ecc] text-white' : 'text-gray-500 hover:bg-gray-50'">
                Upload file
              </button>
              <button type="button"
                @click="pdfSource = 'gdrive'"
                class="flex-1 py-1.5 transition-colors"
                :class="pdfSource === 'gdrive' ? 'bg-[#234ecc] text-white' : 'text-gray-500 hover:bg-gray-50'">
                Google Drive
              </button>
            </div>

            <!-- Upload panel -->
            <div v-if="pdfSource === 'upload'" class="border border-dashed border-gray-200 rounded-xl p-4 space-y-2">
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

            <!-- GDrive panel -->
            <div v-else class="space-y-2">
              <input
                v-model="form.gdrive_pdf_id"
                type="text"
                placeholder="Paste Google Drive file ID…"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <p class="text-xs text-gray-400">
                From your Drive share link:
                <code class="bg-gray-100 px-1 rounded">drive.google.com/file/d/<strong>FILE_ID</strong>/view</code>.
                The file must be shared as "Anyone with the link can view".
              </p>
              <a v-if="form.gdrive_pdf_id"
                :href="`https://drive.google.com/file/d/${form.gdrive_pdf_id}/preview`"
                target="_blank" rel="noopener noreferrer"
                class="inline-flex items-center gap-1 text-xs text-[#234ecc] hover:underline">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
                Preview in Drive
              </a>
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
import { ref, reactive, computed, watch, onMounted } from 'vue'
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
  gdrive_pdf_id: '',
})
const tagsInput = ref('')

const loadingBook = ref(false)
const saving = ref(false)
const apiError = ref('')
let slugWasEdited = false

const pdfSource = ref('upload')

watch(pdfSource, (src) => {
  if (src === 'upload') form.value.gdrive_pdf_id = ''
  else form.value.pdf_key = ''
})

const uploading = reactive({ cover: false, pdf: false, audio: false })
const uploaded = reactive({ cover: false, pdf: false, audio: false })

const coverInput = ref(null)
const pdfInput = ref(null)
const audioInput = ref(null)

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
      gdrive_pdf_id: data.gdrive_pdf_id || '',
    }
    tagsInput.value = (data.tags || []).join(', ')
    slugWasEdited = true
    if (!data.pdf_key && data.gdrive_pdf_id) pdfSource.value = 'gdrive'
  } finally {
    loadingBook.value = false
  }
})
</script>
