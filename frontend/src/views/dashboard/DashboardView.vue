<template>
  <div class="max-w-5xl mx-auto px-4 py-10">

    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">
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
          <div class="text-3xl font-bold text-emerald-700">{{ progress.totalCompleted }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lessonsCompleted') }}</div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-3xl font-bold text-emerald-700">{{ progress.enrolledTracks.length }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.tracksEnrolled') }}</div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-3xl font-bold text-emerald-700 flex items-center justify-center gap-1">
            {{ progress.currentStreak }}
            <span class="text-xl" v-if="progress.currentStreak > 0">🔥</span>
          </div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.dayStreak') }}</div>
          <div v-if="progress.longestStreak > 1" class="text-xs text-gray-400 mt-0.5">
            {{ t('dashboard.bestStreak', { count: progress.longestStreak }) }}
          </div>
        </div>
        <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm text-center">
          <div class="text-3xl font-bold text-emerald-700">{{ lastActivityLabel }}</div>
          <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lastActivity') }}</div>
        </div>
      </div>

      <!-- Continue Learning -->
      <div v-if="progress.continueLesson" class="mb-8">
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">{{ t('dashboard.continueLearning') }}</h2>
        <RouterLink
          :to="{ name: 'lesson', params: { lessonSlug: progress.continueLesson.lesson_slug } }"
          class="group flex items-center justify-between bg-white border border-gray-100 shadow-sm rounded-xl px-6 py-4 hover:border-emerald-200 hover:shadow-md transition-all"
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
        <div class="text-4xl mb-3">📚</div>
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
