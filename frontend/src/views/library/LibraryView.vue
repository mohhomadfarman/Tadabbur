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
      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5 sm:gap-7">
        <div
          v-for="n in 8" :key="n"
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
        class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-5 sm:gap-7"
      >
        <RouterLink
          v-for="book in books"
          :key="book.id"
          :to="{ name: 'book', params: { slug: book.slug } }"
          class="group flex flex-col"
        >
          <!-- Cover -->
          <div
            class="relative aspect-[3/4] rounded-xl overflow-hidden ring-1 ring-black/5
                   shadow-[0_8px_24px_-12px_rgba(0,0,0,0.45)] transition-all duration-300
                   group-hover:-translate-y-1.5 group-hover:shadow-[0_22px_40px_-18px_rgba(35,78,204,0.5)]"
          >
            <!-- Real cover -->
            <img
              v-if="book.cover_url"
              :src="book.cover_url"
              :alt="book.title"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.04]"
              loading="lazy"
            />

            <!-- Generated fallback cover (deterministic per book) -->
            <div
              v-else
              class="w-full h-full flex flex-col justify-between p-4 text-white"
              :style="{ backgroundImage: coverGradient(book) }"
            >
              <span class="text-[10px] font-bold uppercase tracking-[0.2em] opacity-80">
                {{ book.category || 'Tadabbur' }}
              </span>
              <span class="text-base font-extrabold leading-tight line-clamp-4 drop-shadow-sm">
                {{ book.title }}
              </span>
              <span class="text-[11px] font-medium opacity-80 truncate">
                {{ book.author || '' }}
              </span>
            </div>

            <!-- Readability scrim for overlaid pills -->
            <div class="absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-black/35 to-transparent pointer-events-none"></div>

            <!-- Category pill (top-start) -->
            <span
              v-if="book.category"
              class="absolute top-2.5 start-2.5 text-[10px] font-bold uppercase tracking-wider
                     px-2 py-0.5 rounded-full bg-white/90 text-brand backdrop-blur-sm shadow-sm"
            >
              {{ book.category }}
            </span>

            <!-- Audio indicator (top-end) -->
            <div
              v-if="book.has_audio"
              class="absolute top-2.5 end-2.5 w-6 h-6 rounded-full flex items-center justify-center bg-brand shadow-md"
              title="Audiobook available"
            >
              <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"/>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
              </svg>
            </div>

            <!-- Multi-volume indicator (bottom-start) -->
            <span
              v-if="book.volume_count > 1"
              class="absolute bottom-2.5 start-2.5 text-[10px] font-bold tracking-wider
                     px-2 py-0.5 rounded-full bg-black/55 text-white backdrop-blur-sm shadow-sm
                     flex items-center gap-1"
              :title="`${book.volume_count} volumes`"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.5 4 10l8 3.5L20 10l-8-3.5zM4 14l8 3.5L20 14"/>
              </svg>
              {{ book.volume_count }} vols
            </span>
          </div>

          <!-- Info -->
          <div class="pt-3 px-0.5 flex flex-col">
            <h3
              class="text-gray-900 text-sm font-bold leading-snug line-clamp-2
                     group-hover:text-brand transition-colors duration-200"
            >
              {{ book.title }}
            </h3>
            <p class="text-gray-500 text-xs mt-1 truncate">{{ book.author || 'Unknown' }}</p>

            <!-- Meta row -->
            <div class="flex items-center gap-2 mt-2 text-[11px] text-gray-400">
              <span v-if="book.page_count">{{ book.page_count }} pages</span>
              <span v-if="book.page_count && book.language && book.language !== 'en'" class="text-gray-300">·</span>
              <span
                v-if="book.language && book.language !== 'en'"
                class="font-semibold uppercase tracking-wider"
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
import { ref, onMounted, onServerPrefetch } from 'vue'
import { libraryApi } from '@/api/library'
import { useSsrDataStore } from '@/stores/ssrData'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

useSeo({
  title: 'Islamic Library',
  description: 'Free Islamic books: read online, listen as audiobook, or download. Scholar-reviewed collection for every Muslim.',
  url: `${SEO_ORIGIN}/library`,
})

const ssr            = useSsrDataStore()
const books          = ref(ssr.get('library:books') ?? [])
const categories     = ref([])
const loading        = ref(ssr.get('library:books') == null)
const error          = ref('')

// Prerender the default (unfiltered) book grid into the static HTML.
onServerPrefetch(async () => {
  try {
    books.value = await libraryApi.getBooks()
    ssr.set('library:books', books.value)
  } catch {
    /* leave empty; client surfaces the error */
  } finally {
    loading.value = false
  }
})
const searchQuery    = ref('')
const categoryFilter = ref('')
const langFilter     = ref('')

let debounceTimer = null

// Deterministic gradient for books without a cover, so they still look intentional.
const COVER_PALETTES = [
  ['#234ecc', '#0e2a73'],
  ['#0f766e', '#053b35'],
  ['#7c3aed', '#3b1278'],
  ['#b45309', '#5c2a06'],
  ['#be123c', '#5e0a1e'],
  ['#1e3a8a', '#0b1736'],
  ['#0369a1', '#06283d'],
]
function coverGradient(book) {
  const key = book.slug || book.title || ''
  let hash = 0
  for (let i = 0; i < key.length; i++) hash = (hash * 31 + key.charCodeAt(i)) >>> 0
  const [from, to] = COVER_PALETTES[hash % COVER_PALETTES.length]
  return `linear-gradient(150deg, ${from} 0%, ${to} 100%)`
}

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
  // Books are prerendered/hydrated; only fetch if we have none (avoids the
  // skeleton flash). Categories (filter chips) aren't prerendered — load them.
  if (!books.value.length) fetchBooks()
  try {
    categories.value = await libraryApi.getCategories()
  } catch {
    /* filter chips are non-critical */
  }
})
</script>
