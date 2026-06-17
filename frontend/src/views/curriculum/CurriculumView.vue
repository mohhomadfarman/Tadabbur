<template>
  <div class="max-w-7xl mx-auto px-4 py-6 sm:py-12">

    <!-- Header -->
    <div class="mb-10">
      <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">{{ t('curriculum.title') }}</h1>
      <p class="text-gray-500">{{ t('curriculum.subtitle') }}</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
      <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-2xl h-48 animate-pulse" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <!-- Empty -->
    <div v-else-if="tracks.length === 0" class="text-center py-20 text-gray-400">
      {{ t('curriculum.empty') }}
    </div>

    <!-- Tracks grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
      <RouterLink
        v-for="track in tracks"
        :key="track.id"
        :to="{ name: 'track', params: { trackSlug: track.slug } }"
        class="group bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-200 transition-all"
      >
        <div class="mb-4" v-html="trackIcon(track.slug)"></div>
        <h2 class="text-lg font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors mb-2">
          {{ track.title }}
        </h2>
        <p class="text-sm text-gray-500 line-clamp-2 mb-4">{{ track.description }}</p>
        <span class="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
          {{ t('curriculum.startLearning') }}
          <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </span>
      </RouterLink>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'

const { t } = useI18n()

const tracks = ref([])
const loading = ref(true)
const error = ref('')

const iconMap = {
  'quran-sciences': `<svg style="width:2rem;height:2rem;color:#60a5fa" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>`,
  'fiqh': `<svg style="width:2rem;height:2rem;color:#facc15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z"/></svg>`,
  'aqeedah': `<svg style="width:2rem;height:2rem;color:#c084fc" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"/></svg>`,
  'seerah': `<svg style="width:2rem;height:2rem;color:#fb923c" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"/></svg>`,
  'arabic': `<svg style="width:2rem;height:2rem;color:#34d399" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125"/></svg>`,
}

const fallbackIcon = `<svg style="width:2rem;height:2rem;color:#9ca3af" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>`

function trackIcon(slug) {
  return iconMap[slug] || fallbackIcon
}

onMounted(async () => {
  try {
    tracks.value = await curriculumApi.getTracks()
  } catch {
    error.value = t('curriculum.loadError')
  } finally {
    loading.value = false
  }
})
</script>
