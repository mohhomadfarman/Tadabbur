<template>
  <div class="max-w-7xl mx-auto px-4 py-12">

    <!-- Header -->
    <div class="mb-10">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ t('curriculum.title') }}</h1>
      <p class="text-gray-500">{{ t('curriculum.subtitle') }}</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
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
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouterLink
        v-for="track in tracks"
        :key="track.id"
        :to="{ name: 'track', params: { trackSlug: track.slug } }"
        class="group bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-200 transition-all"
      >
        <div class="text-3xl mb-4">{{ trackIcon(track.slug) }}</div>
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
  'quran-sciences': '📖',
  'fiqh': '⚖️',
  'aqeedah': '🌙',
  'seerah': '🕌',
  'arabic': '✍️',
}

function trackIcon(slug) {
  return iconMap[slug] || '📚'
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
