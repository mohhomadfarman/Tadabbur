<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-10">

    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-1.5">{{ t('curriculum.title') }}</h1>
      <p class="text-gray-500">{{ t('curriculum.subtitle') }}</p>
    </div>

    <!-- Toolbar: Search + Sort + View toggle -->
    <div class="flex flex-col sm:flex-row gap-3 mb-4">

      <!-- Search input -->
      <div class="relative flex-1">
        <span class="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 pointer-events-none">
          <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0"/>
          </svg>
        </span>
        <input
          v-model="searchQuery"
          type="search"
          :placeholder="t('curriculum.searchPlaceholder')"
          class="w-full pl-9 pr-9 py-2.5 text-sm bg-white border border-gray-200 rounded-xl
                 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-400
                 placeholder-gray-400 transition-all"
        />
        <button
          v-if="searchQuery"
          @click="searchQuery = ''"
          class="absolute right-3 rtl:right-auto rtl:left-3 top-1/2 -translate-y-1/2
                 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Sort + View toggle -->
      <div class="flex items-center gap-2 shrink-0">
        <select
          v-model="sortOrder"
          class="text-sm bg-white border border-gray-200 rounded-xl px-3 py-2.5
                 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-400
                 text-gray-700 cursor-pointer transition-all"
        >
          <option value="default">{{ t('curriculum.sortDefault') }}</option>
          <option value="az">{{ t('curriculum.sortAZ') }}</option>
          <option value="za">{{ t('curriculum.sortZA') }}</option>
        </select>

        <!-- View mode toggle -->
        <div class="flex items-center bg-gray-100 rounded-xl p-1 gap-0.5">
          <button
            @click="viewMode = 'icon'"
            :title="t('curriculum.viewIcon')"
            :class="viewMode === 'icon' ? 'bg-white text-gray-800 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
            class="p-2 rounded-lg transition-all"
          >
            <!-- 2×2 grid (icon view) -->
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="3" y="3" width="7" height="7" rx="1.5" stroke-width="1.75"/>
              <rect x="14" y="3" width="7" height="7" rx="1.5" stroke-width="1.75"/>
              <rect x="3" y="14" width="7" height="7" rx="1.5" stroke-width="1.75"/>
              <rect x="14" y="14" width="7" height="7" rx="1.5" stroke-width="1.75"/>
            </svg>
          </button>
          <button
            @click="viewMode = 'card'"
            :title="t('curriculum.viewCard')"
            :class="viewMode === 'card' ? 'bg-white text-gray-800 shadow-sm' : 'text-gray-400 hover:text-gray-600'"
            class="p-2 rounded-lg transition-all"
          >
            <!-- Card with image header (card view) -->
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="3" y="3" width="18" height="18" rx="2" stroke-width="1.75"/>
              <line x1="3" y1="10" x2="21" y2="10" stroke-width="1.75"/>
              <line x1="7" y1="14" x2="17" y2="14" stroke-width="1.5" stroke-linecap="round"/>
              <line x1="7" y1="17" x2="13" y2="17" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Filter chips (logged-in users only) -->
    <div v-if="auth.isLoggedIn" class="flex items-center gap-2 mb-6 flex-wrap">
      <button
        v-for="f in filterOptions"
        :key="f.value"
        @click="filterMode = f.value"
        :class="filterMode === f.value
          ? 'bg-emerald-700 text-white border-emerald-700'
          : 'bg-white text-gray-600 border-gray-200 hover:border-emerald-300 hover:text-emerald-700'"
        class="text-xs font-medium px-3.5 py-1.5 rounded-full border transition-all"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="n in 3" :key="n"
        class="bg-gray-100 rounded-2xl animate-pulse"
        :class="viewMode === 'card' ? 'h-64' : 'h-44'"
      />
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm"
    >
      {{ error }}
    </div>

    <!-- No tracks at all -->
    <div v-else-if="tracks.length === 0" class="text-center py-20 text-gray-400">
      {{ t('curriculum.empty') }}
    </div>

    <!-- No results from search/filter -->
    <div v-else-if="displayedTracks.length === 0" class="text-center py-16">
      <p class="text-gray-500 font-medium mb-2">{{ t('curriculum.noResults') }}</p>
      <button @click="clearFilters" class="text-sm text-emerald-700 hover:underline">
        {{ t('curriculum.clearFilters') }}
      </button>
    </div>

    <!-- ICON VIEW -->
    <div v-else-if="viewMode === 'icon'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <RouterLink
        v-for="track in displayedTracks"
        :key="track.id"
        :to="{ name: 'track', params: { trackSlug: track.slug } }"
        class="group relative bg-white border border-gray-100 rounded-2xl p-6 shadow-sm
               hover:shadow-md hover:border-emerald-200 transition-all"
      >
        <!-- Enrolled badge -->
        <span
          v-if="auth.isLoggedIn && progress.isEnrolled(track.slug)"
          class="absolute top-4 right-4 rtl:right-auto rtl:left-4 inline-flex items-center gap-1
                 text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200
                 px-2 py-0.5 rounded-full"
        >
          <svg class="w-3 h-3 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clip-rule="evenodd"/>
          </svg>
          {{ t('curriculum.enrolled') }}
        </span>

        <!-- Icon -->
        <div class="mb-4" v-html="buildIcon(track.slug, '2rem')"></div>

        <!-- Title -->
        <h2 class="text-base font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors mb-1.5">
          {{ track.title }}
        </h2>

        <!-- Description -->
        <p class="text-sm text-gray-500 line-clamp-2 mb-3">{{ track.description }}</p>

        <!-- Available translation languages -->
        <TrackLanguages :languages="track.languages" :title="t('curriculum.availableIn')" class="mb-4" />

        <!-- CTA -->
        <span class="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
          {{ t('curriculum.startLearning') }}
          <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </span>
      </RouterLink>
    </div>

    <!-- CARD VIEW (image / gradient hero) -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <RouterLink
        v-for="track in displayedTracks"
        :key="track.id"
        :to="{ name: 'track', params: { trackSlug: track.slug } }"
        class="group bg-white border border-gray-100 rounded-2xl shadow-sm
               hover:shadow-md hover:border-emerald-200 transition-all overflow-hidden"
      >
        <!-- Hero: real image or gradient + icon -->
        <div class="relative h-36 overflow-hidden">
          <img
            v-if="track.thumbnail_url"
            :src="track.thumbnail_url"
            :alt="track.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center"
            :style="trackGradient(track.slug)"
          >
            <div v-html="buildIcon(track.slug, '3rem', 'rgba(255,255,255,0.88)')"></div>
          </div>

          <!-- Enrolled badge overlay -->
          <span
            v-if="auth.isLoggedIn && progress.isEnrolled(track.slug)"
            class="absolute top-3 right-3 rtl:right-auto rtl:left-3 inline-flex items-center gap-1
                   text-xs font-semibold bg-white/95 text-emerald-700 px-2.5 py-1 rounded-full shadow-sm"
          >
            <svg class="w-3 h-3 shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"/>
            </svg>
            {{ t('curriculum.enrolled') }}
          </span>
        </div>

        <!-- Card body -->
        <div class="p-5">
          <h2 class="text-base font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors mb-1.5">
            {{ track.title }}
          </h2>
          <p class="text-sm text-gray-500 line-clamp-2 mb-3">{{ track.description }}</p>

          <!-- Available translation languages -->
          <TrackLanguages :languages="track.languages" :title="t('curriculum.availableIn')" class="mb-4" />

          <span class="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
            {{ t('curriculum.startLearning') }}
            <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </span>
        </div>
      </RouterLink>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onServerPrefetch } from 'vue'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'
import { useSsrDataStore } from '@/stores/ssrData'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'
import TrackLanguages from '@/components/TrackLanguages.vue'

const { t } = useI18n()
const auth = useAuthStore()
const progress = useProgressStore()
const ssr = useSsrDataStore()

const ssrKey = 'tracks'
const tracks = ref(ssr.get(ssrKey) ?? [])
const loading = ref(ssr.get(ssrKey) == null)
const error = ref('')

// Prerender the track list so /learn ships the full grid + ItemList JSON-LD.
onServerPrefetch(async () => {
  try {
    tracks.value = await curriculumApi.getTracks()
    ssr.set(ssrKey, tracks.value)
  } catch {
    /* leave empty; client surfaces the error */
  } finally {
    loading.value = false
  }
})

useSeo(() => ({
  title: 'Learning Tracks',
  description: 'Browse Tadabbur’s structured Islamic learning tracks — scholar-verified curriculum from beginner to advanced, free forever.',
  url: `${SEO_ORIGIN}/learn`,
  jsonLd: tracks.value.length
    ? {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        name: 'Tadabbur Learning Tracks',
        itemListElement: tracks.value.map((tr, i) => ({
          '@type': 'ListItem',
          position: i + 1,
          name: tr.title,
          url: `${SEO_ORIGIN}/learn/${tr.slug}`,
        })),
      }
    : undefined,
}))

const viewMode = ref('card')      // 'icon' | 'card' — default to card view
const searchQuery = ref('')
const sortOrder = ref('default')  // 'default' | 'az' | 'za'
const filterMode = ref('all')     // 'all' | 'enrolled' | 'not-enrolled'

const filterOptions = computed(() => [
  { value: 'all',          label: t('curriculum.filterAll') },
  { value: 'enrolled',     label: t('curriculum.filterEnrolled') },
  { value: 'not-enrolled', label: t('curriculum.filterNotEnrolled') },
])

const displayedTracks = computed(() => {
  let result = tracks.value

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(track =>
      track.title.toLowerCase().includes(q) ||
      (track.description || '').toLowerCase().includes(q)
    )
  }

  if (auth.isLoggedIn) {
    if (filterMode.value === 'enrolled')
      result = result.filter(track => progress.isEnrolled(track.slug))
    else if (filterMode.value === 'not-enrolled')
      result = result.filter(track => !progress.isEnrolled(track.slug))
  }

  if (sortOrder.value === 'az') return [...result].sort((a, b) => a.title.localeCompare(b.title))
  if (sortOrder.value === 'za') return [...result].sort((a, b) => b.title.localeCompare(a.title))
  return result
})

function clearFilters() {
  searchQuery.value = ''
  sortOrder.value = 'default'
  filterMode.value = 'all'
}

// --- Icon & gradient system ---

const iconData = {
  'quran-sciences': {
    path: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    color: '#60a5fa',
    gradient: 'linear-gradient(135deg, #3b82f6, #4338ca)',
  },
  'fiqh': {
    path: 'M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z',
    color: '#f59e0b',
    gradient: 'linear-gradient(135deg, #f59e0b, #d97706)',
  },
  'aqeedah': {
    path: 'M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z',
    color: '#c084fc',
    gradient: 'linear-gradient(135deg, #a855f7, #7c3aed)',
  },
  'seerah': {
    path: 'M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z',
    color: '#fb923c',
    gradient: 'linear-gradient(135deg, #f97316, #e11d48)',
  },
  'arabic': {
    path: 'M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125',
    color: '#34d399',
    gradient: 'linear-gradient(135deg, #10b981, #0891b2)',
  },
}

const defaultIcon = {
  path: 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
  color: '#9ca3af',
  gradient: 'linear-gradient(135deg, #6b7280, #4b5563)',
}

function buildIcon(slug, size = '2rem', color = null) {
  const data = iconData[slug] ?? defaultIcon
  const c = color ?? data.color
  return `<svg style="width:${size};height:${size};color:${c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="${data.path}"/></svg>`
}

function trackGradient(slug) {
  return { background: (iconData[slug] ?? defaultIcon).gradient }
}

onMounted(async () => {
  try {
    if (!tracks.value.length) {
      tracks.value = await curriculumApi.getTracks()
    }
    if (auth.isLoggedIn) await progress.fetchProgress()
  } catch {
    error.value = t('curriculum.loadError')
  } finally {
    loading.value = false
  }
})
</script>
