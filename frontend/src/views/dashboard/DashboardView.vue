<template>
  <div class="max-w-5xl mx-auto px-4 py-6 sm:py-10">

    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-xl sm:text-2xl font-bold text-gray-900">
        {{ auth.user?.full_name ? t('dashboard.welcomeName', { name: auth.user.full_name }) : t('dashboard.welcome') }}
      </h1>
      <p class="text-gray-500 mt-1 text-sm">{{ t('dashboard.subtitle') }}</p>
    </div>

    <div v-if="loading" class="space-y-4 animate-pulse">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="bg-gray-100 rounded-xl h-24" />
      </div>
      <div class="bg-gray-100 rounded-xl h-32 mt-6" />
    </div>

    <template v-else>

      <!-- Stats row -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-2xl sm:text-3xl font-bold text-emerald-700">{{ progress.totalCompleted }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lessonsCompleted') }}</div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-2xl sm:text-3xl font-bold text-emerald-700">{{ progress.enrolledTracks.length }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.tracksEnrolled') }}</div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-2xl sm:text-3xl font-bold text-emerald-700 flex items-center justify-center gap-1">
            {{ progress.currentStreak }}
            <svg v-if="progress.currentStreak > 0" class="w-5 h-5 text-orange-400" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248ZM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1A5.99 5.99 0 0112 12.75a.75.75 0 01.75.75v.008l-.001.008a3.75 3.75 0 013.001 2.734Z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.dayStreak') }}</div>
          <div v-if="progress.longestStreak > 1" class="text-xs text-gray-400 mt-0.5">
            {{ t('dashboard.bestStreak', { count: progress.longestStreak }) }}
          </div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-2xl sm:text-3xl font-bold text-emerald-700">{{ lastActivityLabel }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lastActivity') }}</div>
        </div>
      </div>

      <!-- Continue Learning -->
      <div v-if="progress.continueLesson" class="mb-8">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">{{ t('dashboard.continueLearning') }}</h2>
        <RouterLink
          :to="{ name: 'lesson', params: { lessonSlug: progress.continueLesson.lesson_slug } }"
          class="group flex items-center justify-between bg-white border border-gray-100 shadow-sm rounded-xl px-4 py-3 sm:px-6 sm:py-4 hover:border-emerald-200 hover:shadow-md transition-all"
        >
          <div>
            <p class="text-xs text-emerald-700 font-medium mb-0.5">{{ progress.continueLesson.subject_title }}</p>
            <p class="font-semibold text-gray-900 group-hover:text-emerald-800 transition-colors">
              {{ progress.continueLesson.lesson_title }}
            </p>
          </div>
          <div class="flex items-center gap-2 text-emerald-700 ms-4 shrink-0">
            <span class="text-sm font-medium hidden sm:block">{{ t('dashboard.resume') }}</span>
            <svg class="w-5 h-5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </RouterLink>
      </div>

      <!-- Enrolled Tracks -->
      <div v-if="progress.enrolledTracks.length > 0" class="mb-8">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">{{ t('dashboard.yourTracks') }}</h2>
        <div class="space-y-3">
          <div
            v-for="slug in progress.enrolledTracks"
            :key="slug"
            class="bg-white border border-gray-100 shadow-sm rounded-xl p-5"
          >
            <div v-if="trackStats[slug]">
              <div class="flex items-start justify-between mb-3">
                <RouterLink
                  :to="{ name: 'track', params: { trackSlug: slug } }"
                  class="font-semibold text-gray-900 hover:text-emerald-700 transition-colors"
                >
                  {{ trackStats[slug].track_title }}
                </RouterLink>
                <span class="text-sm font-semibold text-emerald-700 ms-4 shrink-0">
                  {{ trackStats[slug].percent }}%
                </span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-2 mb-2">
                <div
                  class="bg-emerald-500 h-2 rounded-full transition-all duration-500"
                  :style="{ width: trackStats[slug].percent + '%' }"
                />
              </div>
              <p class="text-xs text-gray-400">
                {{ t('dashboard.lessonsProgress', { completed: trackStats[slug].completed_lessons, total: trackStats[slug].total_lessons }) }}
              </p>
            </div>
            <div v-else class="animate-pulse flex items-center gap-3">
              <div class="bg-gray-100 rounded h-4 flex-1" />
              <div class="bg-gray-100 rounded h-4 w-10" />
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state — no tracks enrolled -->
      <div v-else class="bg-emerald-50 border border-emerald-100 rounded-xl p-8 text-center">
        <div class="mb-3 flex justify-center">
          <svg class="w-12 h-12 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <h2 class="font-semibold text-emerald-900 mb-1">{{ t('dashboard.emptyTitle') }}</h2>
        <p class="text-emerald-700 text-sm mb-5">{{ t('dashboard.emptyDesc') }}</p>
        <RouterLink
          to="/learn"
          class="inline-block bg-emerald-700 hover:bg-emerald-800 text-white px-6 py-2.5 rounded-xl text-sm font-semibold transition-colors"
        >
          {{ t('dashboard.browseCurriculum') }}
        </RouterLink>
      </div>

    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const auth = useAuthStore()
const progress = useProgressStore()
const { t } = useI18n()

const loading = ref(true)
const trackStats = ref({})

const lastActivityLabel = computed(() => {
  if (!progress.lastActivity) return '—'
  const d = new Date(progress.lastActivity)
  const today = new Date()
  const diff = Math.floor((today - d) / 86400000)
  if (diff === 0) return t('dashboard.today')
  if (diff === 1) return t('dashboard.yesterday')
  return t('dashboard.daysAgo', { count: diff })
})

async function loadTrackStats() {
  const slugs = progress.enrolledTracks
  await Promise.all(
    slugs.map(async (slug) => {
      const data = await progress.fetchTrackProgress(slug)
      if (data) trackStats.value[slug] = data
    })
  )
}

onMounted(async () => {
  progress.loaded = false
  await progress.fetchProgress()
  await loadTrackStats()
  loading.value = false
})
</script>
