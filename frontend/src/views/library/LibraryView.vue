<template>
  <div class="min-h-screen bg-white">

    <!-- ── Page header ──────────────────────────────────────────────── -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 pt-8 pb-6 sm:pt-12 sm:pb-8">
      <p class="text-xs font-bold uppercase tracking-widest text-brand mb-4 flex items-center gap-2">
        <span class="w-4 h-px bg-brand inline-block"></span>
        Islamic Library
      </p>
      <h1 class="text-3xl sm:text-4xl font-black text-gray-900 tracking-tight mb-3">
        Books for the Ummah
      </h1>
      <p class="text-gray-500 text-base sm:text-lg max-w-xl">
        Scholar-reviewed Islamic books — read online, listen, or download. Free forever.
      </p>
    </div>

    <!-- ── Search + filters ─────────────────────────────────────────── -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 mb-8">
      <div class="flex flex-col sm:flex-row gap-3">

        <!-- Search -->
        <div class="relative flex-1">
          <svg
            class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Search books…"
            class="w-full bg-white border border-gray-200 text-gray-900 placeholder-gray-400 text-sm
                   rounded-xl pl-9 pr-4 py-2.5 focus:outline-none focus:border-brand/50 focus:ring-2
                   focus:ring-brand/10 transition-all duration-200"
            @input="debouncedSearch"
          />
        </div>

        <!-- Language filter -->
        <select
          v-model="langFilter"
          @change="fetchBooks"
          class="bg-white border border-gray-200 text-gray-700 text-sm rounded-xl px-4 py-2.5
                 focus:outline-none focus:border-brand/50 focus:ring-2 focus:ring-brand/10
                 transition-all duration-200 cursor-pointer"
        >
          <option value="">All Languages</option>
          <option value="en">English</option>
          <option value="ar">العربية</option>
          <option value="ur">اردو</option>
          <option value="fr">Français</option>
          <option value="id">Bahasa</option>
        </select>
      </div>

      <!-- Category chips -->
      <div v-if="categories.length" class="flex flex-wrap gap-2 mt-4">
        <button
          @click="categoryFilter = ''; fetchBooks()"
          :class="categoryFilter === ''
            ? 'bg-brand text-white border-brand'
            : 'bg-white text-gray-600 border-gray-200 hover:border-brand/40 hover:text-brand'"
          class="text-xs font-semibold px-3 py-1.5 rounded-full border transition-all duration-150"
        >
          All
        </button>
        <button
          v-for="cat in categories"
          :key="cat"
          @click="categoryFilter = cat; fetchBooks()"
          :class="categoryFilter === cat
            ? 'bg-brand text-white border-brand'
            : 'bg-white text-gray-600 border-gray-200 hover:border-brand/40 hover:text-brand'"
          class="text-xs font-semibold px-3 py-1.5 rounded-full border transition-all duration-150"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- ── Book grid ─────────────────────────────────────────────────── -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 pb-20">

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-5">
        <div
          v-for="n in 10" :key="n"
          class="animate-pulse rounded-2xl overflow-hidden bg-gray-100 border border-gray-100"
        >
          <div class="aspect-[3/4] bg-gray-200"></div>
          <div class="p-4 space-y-2">
            <div class="h-3 rounded-full bg-gray-200 w-full"></div>
            <div class="h-3 rounded-full bg-gray-100 w-2/3"></div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div
        v-else-if="error"
        class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm"
      >
        {{ error }}
      </div>

      <!-- Empty -->
      <div v-else-if="books.length === 0" class="text-center py-24">
        <div class="mb-4 flex justify-center">
          <svg
            class="w-16 h-16 text-gray-200"
            viewBox="0 0 24 24" fill="none" stroke="currentColor"
            stroke-width="1" stroke-linecap="round" stroke-linejoin="round"
          >
            <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <p class="text-gray-400 text-lg">No books found.</p>
        <button
          v-if="searchQuery || categoryFilter || langFilter"
          @click="resetFilters"
          class="mt-4 text-brand text-sm hover:underline"
        >
          Clear filters
        </button>
      </div>

      <!-- Grid -->
      <div
        v-else
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-5"
      >
        <RouterLink
          v-for="book in books"
          :key="book.id"
          :to="{ name: 'book', params: { slug: book.slug } }"
          class="group flex flex-col bg-white rounded-2xl overflow-hidden border border-gray-100
                 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-md
                 hover:border-gray-200"
        >
          <!-- Cover image -->
          <div class="aspect-[3/4] overflow-hidden relative bg-gray-50">
            <img
              v-if="book.cover_url"
              :src="book.cover_url"
              :alt="book.title"
              class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              loading="lazy"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <svg class="w-10 h-10 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                      d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
            </div>

            <!-- Audio indicator -->
            <div
              v-if="book.has_audio"
              class="absolute top-2 end-2 w-6 h-6 rounded-full flex items-center justify-center bg-brand shadow-sm"
              title="Audiobook available"
            >
              <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"/>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
              </svg>
            </div>
          </div>

          <!-- Info -->
          <div class="p-3 sm:p-4 flex flex-col flex-1">
            <!-- Category badge -->
            <span
              v-if="book.category"
              class="inline-block text-[10px] font-bold uppercase tracking-widest px-2 py-0.5
                     rounded-full mb-2 self-start bg-brand/8 text-brand border border-brand/15"
            >
              {{ book.category }}
            </span>

            <h3
              class="text-gray-900 text-xs sm:text-sm font-semibold leading-snug line-clamp-2 mb-1
                     group-hover:text-brand transition-colors duration-200"
            >
              {{ book.title }}
            </h3>
            <p class="text-gray-400 text-[11px] truncate">{{ book.author || 'Unknown' }}</p>

            <!-- Footer -->
            <div class="flex items-center gap-2 mt-auto pt-3">
              <span v-if="book.page_count" class="text-[10px] text-gray-400">
                {{ book.page_count }}p
              </span>
              <span
                v-if="book.language && book.language !== 'en'"
                class="text-[10px] font-semibold uppercase tracking-wider text-gray-400
                       border border-gray-200 rounded px-1.5 py-0.5"
              >
                {{ book.language }}
              </span>
            </div>
          </div>
        </RouterLink>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { libraryApi } from '@/api/library'
import { useSeo } from '@/composables/useSeo'

useSeo({
  title: 'Islamic Library — Tadabbur',
  description: 'Free Islamic books: read online, listen as audiobook, or download. Scholar-reviewed collection for every Muslim.',
})

const books          = ref([])
const categories     = ref([])
const loading        = ref(true)
const error          = ref('')
const searchQuery    = ref('')
const categoryFilter = ref('')
const langFilter     = ref('')

let debounceTimer = null

function debouncedSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchBooks, 350)
}

async function fetchBooks() {
  error.value   = ''
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value)    params.q        = searchQuery.value
    if (categoryFilter.value) params.category  = categoryFilter.value
    if (langFilter.value)     params.language  = langFilter.value
    books.value = await libraryApi.getBooks(params)
  } catch {
    error.value = 'Failed to load books. Please try again.'
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  searchQuery.value    = ''
  categoryFilter.value = ''
  langFilter.value     = ''
  fetchBooks()
}

onMounted(async () => {
  const [, cats] = await Promise.allSettled([
    fetchBooks(),
    libraryApi.getCategories(),
  ])
  if (cats.status === 'fulfilled') categories.value = cats.value
})
</script>
