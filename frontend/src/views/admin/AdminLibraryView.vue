<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex items-start justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Library</h1>
        <p class="text-gray-400 text-sm mt-0.5">Manage books, PDFs and audio files.</p>
      </div>
      <RouterLink
        :to="{ name: 'admin-book-new' }"
        class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shadow-sm"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Add Book
      </RouterLink>
    </div>

    <!-- Error -->
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">
      {{ error }}
    </div>

    <!-- Toolbar: search + sort + filters -->
    <div v-if="!loading && books.length > 0" class="mb-6 space-y-3">
      <div class="flex flex-col lg:flex-row gap-3">
        <!-- Search -->
        <div class="relative flex-1">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none"
               fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-width="2" d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Search by title or author…"
            class="w-full border border-gray-200 rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
          />
        </div>
        <!-- Sort -->
        <select
          v-model="sortBy"
          class="border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        >
          <option value="order">Published first</option>
          <option value="newest">Newest first</option>
          <option value="oldest">Oldest first</option>
          <option value="title-asc">Title A–Z</option>
          <option value="title-desc">Title Z–A</option>
        </select>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Status -->
        <select
          v-model="statusFilter"
          class="border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        >
          <option value="all">All status</option>
          <option value="published">Published</option>
          <option value="draft">Draft</option>
        </select>
        <!-- Category -->
        <select
          v-model="categoryFilter"
          class="border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        >
          <option value="">All categories</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
        <!-- Language -->
        <select
          v-model="languageFilter"
          class="border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        >
          <option value="">All languages</option>
          <option v-for="l in LANGUAGES" :key="l.value" :value="l.value">{{ l.label }}</option>
        </select>

        <button
          v-if="hasActiveFilters"
          @click="resetFilters"
          class="text-sm text-gray-500 hover:text-[#234ecc] transition-colors"
        >
          Clear filters
        </button>

        <span class="ml-auto text-xs text-gray-400">
          {{ sorted.length }} book{{ sorted.length === 1 ? '' : 's' }}
        </span>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-5">
      <div v-for="i in 10" :key="i" class="animate-pulse">
        <div class="aspect-[2/3] bg-gray-100 rounded-2xl mb-3" />
        <div class="h-4 bg-gray-100 rounded w-3/4 mb-2" />
        <div class="h-3 bg-gray-100 rounded w-1/2" />
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="books.length === 0"
         class="flex flex-col items-center justify-center py-32 text-center border-2 border-dashed border-gray-200 rounded-2xl">
      <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-4">
        <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
        </svg>
      </div>
      <p class="text-gray-600 font-semibold mb-1">No books yet</p>
      <p class="text-gray-400 text-sm mb-5">Add your first Islamic book to the library.</p>
      <RouterLink
        :to="{ name: 'admin-book-new' }"
        class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Add First Book
      </RouterLink>
    </div>

    <!-- No results for current filters -->
    <div v-else-if="sorted.length === 0"
         class="flex flex-col items-center justify-center py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
      <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mb-4">
        <svg class="w-7 h-7 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" stroke-width="1.5"/><path stroke-linecap="round" stroke-width="1.5" d="m21 21-4.35-4.35"/>
        </svg>
      </div>
      <p class="text-gray-600 font-semibold mb-1">No books match your filters</p>
      <p class="text-gray-400 text-sm mb-5">Try a different search or clear the filters.</p>
      <button
        @click="resetFilters"
        class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors"
      >
        Clear filters
      </button>
    </div>

    <!-- Book grid -->
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-5">
      <div
        v-for="book in paged"
        :key="book.slug"
        class="group"
      >
        <!-- Cover -->
        <div class="relative aspect-[2/3] rounded-2xl overflow-hidden mb-3 shadow-sm group-hover:shadow-lg transition-shadow duration-200">

          <img
            v-if="book.cover_url"
            :src="book.cover_url"
            :alt="book.title"
            class="w-full h-full object-cover"
          />
          <!-- Placeholder cover -->
          <div
            v-else
            class="w-full h-full flex flex-col items-center justify-center"
            :style="placeholderStyle(book.title)"
          >
            <svg class="w-10 h-10 text-white/40 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            <span class="text-white/60 text-xs font-medium px-3 text-center line-clamp-2 leading-tight">{{ book.title }}</span>
          </div>

          <!-- Status badge -->
          <span
            class="absolute top-2 left-2 text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full"
            :class="book.is_published
              ? 'bg-emerald-500/90 text-white'
              : 'bg-black/40 text-white/80'"
          >
            {{ book.is_published ? 'Live' : 'Draft' }}
          </span>

          <!-- File type badges -->
          <div class="absolute bottom-2 left-2 flex gap-1">
            <span v-if="book.has_pdf"
                  class="text-[9px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded bg-[#234ecc]/80 text-white">
              PDF
            </span>
            <span v-if="book.has_audio"
                  class="text-[9px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded bg-purple-500/80 text-white">
              Audio
            </span>
          </div>

          <!-- Hover overlay with actions -->
          <div class="absolute inset-0 bg-black/0 group-hover:bg-black/50 transition-all duration-200 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100">
            <RouterLink
              :to="{ name: 'admin-book-edit', params: { slug: book.slug } }"
              class="w-9 h-9 bg-white rounded-xl flex items-center justify-center text-gray-700 hover:text-[#234ecc] transition-colors shadow-sm"
              title="Edit"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </RouterLink>
            <button
              @click="togglePublish(book)"
              :title="book.is_published ? 'Unpublish' : 'Publish'"
              class="w-9 h-9 bg-white rounded-xl flex items-center justify-center transition-colors shadow-sm"
              :class="book.is_published ? 'text-emerald-600 hover:text-gray-600' : 'text-gray-400 hover:text-emerald-600'"
            >
              <svg v-if="book.is_published" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
              </svg>
            </button>
            <button
              @click="confirmDelete(book)"
              title="Delete"
              class="w-9 h-9 bg-white rounded-xl flex items-center justify-center text-gray-400 hover:text-red-500 transition-colors shadow-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Info below card -->
        <p class="font-semibold text-gray-900 text-sm truncate leading-tight">{{ book.title }}</p>
        <p v-if="book.author" class="text-xs text-gray-400 mt-0.5 truncate">{{ book.author }}</p>
        <div v-if="book.category" class="mt-1.5">
          <span class="text-[10px] text-[#234ecc] bg-[#234ecc]/8 font-semibold px-2 py-0.5 rounded-full">
            {{ book.category }}
          </span>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && totalPages > 1" class="flex items-center justify-center gap-1.5 mt-8">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        Prev
      </button>
      <template v-for="(p, i) in pageNumbers" :key="i">
        <span v-if="p === '…'" class="px-2 text-gray-400 select-none">…</span>
        <button
          v-else
          @click="goToPage(p)"
          class="min-w-[2.25rem] px-3 py-2 text-sm rounded-lg border transition-colors"
          :class="p === currentPage
            ? 'bg-[#234ecc] border-[#234ecc] text-white font-semibold'
            : 'border-gray-200 text-gray-600 hover:border-[#234ecc]/40 hover:text-[#234ecc]'"
        >
          {{ p }}
        </button>
      </template>
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="px-3 py-2 text-sm rounded-lg border border-gray-200 text-gray-600 hover:border-[#234ecc]/40 hover:text-[#234ecc] disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        Next
      </button>
    </div>

    <!-- Delete modal -->
    <div
      v-if="deleteTarget"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
      @click.self="deleteTarget = null"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <div class="w-12 h-12 bg-red-50 rounded-xl flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
        </div>
        <h3 class="font-bold text-gray-900 mb-1">Delete Book?</h3>
        <p class="text-sm text-gray-500 mb-5">
          "<strong>{{ deleteTarget.title }}</strong>" will be permanently removed. This cannot be undone.
        </p>
        <div class="flex gap-3">
          <button
            @click="deleteTarget = null"
            class="flex-1 px-4 py-2.5 text-sm text-gray-600 hover:text-gray-900 border border-gray-200 rounded-xl transition-colors"
          >
            Cancel
          </button>
          <button
            :disabled="deleting"
            @click="doDelete"
            class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors"
          >
            {{ deleting ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const books = ref([])
const loading = ref(true)
const error = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)

// ── Search / filters / sort / pagination (all client-side) ──────────────────
const searchQuery    = ref('')
const statusFilter   = ref('all')     // all | published | draft
const categoryFilter = ref('')
const languageFilter = ref('')
const sortBy         = ref('order')   // order | newest | oldest | title-asc | title-desc
const currentPage    = ref(1)
const pageSize       = 12

const LANGUAGES = [
  { value: 'en', label: 'English' },
  { value: 'ar', label: 'Arabic' },
  { value: 'ur', label: 'Urdu' },
  { value: 'fr', label: 'French' },
  { value: 'id', label: 'Indonesian' },
  { value: 'other', label: 'Other' },
]

const categories = computed(() =>
  [...new Set(books.value.map(b => b.category).filter(Boolean))].sort((a, b) => a.localeCompare(b))
)

const hasActiveFilters = computed(() =>
  !!searchQuery.value || statusFilter.value !== 'all' || !!categoryFilter.value || !!languageFilter.value
)

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return books.value.filter(b => {
    if (q && !`${b.title} ${b.author || ''}`.toLowerCase().includes(q)) return false
    if (statusFilter.value === 'published' && !b.is_published) return false
    if (statusFilter.value === 'draft' && b.is_published) return false
    if (categoryFilter.value && b.category !== categoryFilter.value) return false
    if (languageFilter.value && b.language !== languageFilter.value) return false
    return true
  })
})

const sorted = computed(() => {
  const arr = [...filtered.value]
  switch (sortBy.value) {
    case 'title-asc':  return arr.sort((a, b) => (a.title || '').localeCompare(b.title || ''))
    case 'title-desc': return arr.sort((a, b) => (b.title || '').localeCompare(a.title || ''))
    case 'newest':     return arr.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    case 'oldest':     return arr.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    default:           return arr.sort((a, b) =>
      (Number(b.is_published) - Number(a.is_published)) ||
      ((a.order ?? 0) - (b.order ?? 0)) ||
      (a.title || '').localeCompare(b.title || ''))
  }
})

const totalPages = computed(() => Math.max(1, Math.ceil(sorted.value.length / pageSize)))

const paged = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return sorted.value.slice(start, start + pageSize)
})

const pageNumbers = computed(() => {
  const tp = totalPages.value
  const cur = currentPage.value
  const out = []
  for (let i = 1; i <= tp; i++) {
    if (i === 1 || i === tp || (i >= cur - 1 && i <= cur + 1)) out.push(i)
    else if (out[out.length - 1] !== '…') out.push('…')
  }
  return out
})

// Reset to first page when the result set changes.
watch([searchQuery, statusFilter, categoryFilter, languageFilter, sortBy], () => {
  currentPage.value = 1
})
// Clamp the page if results shrink (e.g. after a delete).
watch(totalPages, (tp) => {
  if (currentPage.value > tp) currentPage.value = tp
})

function resetFilters() {
  searchQuery.value = ''
  statusFilter.value = 'all'
  categoryFilter.value = ''
  languageFilter.value = ''
}

function goToPage(p) {
  currentPage.value = Math.min(Math.max(1, p), totalPages.value)
}

const COVER_GRADIENTS = [
  'linear-gradient(135deg, #1e3a5f, #234ecc)',
  'linear-gradient(135deg, #2d1b69, #7c3aed)',
  'linear-gradient(135deg, #1a3a2a, #16a34a)',
  'linear-gradient(135deg, #3d1515, #dc2626)',
  'linear-gradient(135deg, #1a2a3d, #0891b2)',
  'linear-gradient(135deg, #3d2a00, #d97706)',
  'linear-gradient(135deg, #1a1a2e, #e11d48)',
  'linear-gradient(135deg, #0f2027, #203a43)',
]

function placeholderStyle(title) {
  const index = (title?.charCodeAt(0) || 0) % COVER_GRADIENTS.length
  return { background: COVER_GRADIENTS[index] }
}

async function togglePublish(book) {
  const prev = book.is_published
  book.is_published = !prev
  try {
    await adminApi.updateBook(book.slug, { is_published: book.is_published })
  } catch {
    book.is_published = prev
  }
}

function confirmDelete(book) {
  deleteTarget.value = book
}

async function doDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await adminApi.deleteBook(deleteTarget.value.slug)
    books.value = books.value.filter(b => b.slug !== deleteTarget.value.slug)
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  try {
    books.value = await adminApi.listBooks()
  } catch {
    error.value = 'Could not load books. Make sure your account has author access.'
  } finally {
    loading.value = false
  }
})
</script>
