<template>
  <div class="max-w-6xl mx-auto px-4 py-8">

    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-xl sm:text-2xl font-bold text-gray-900">
        {{ auth.user?.full_name ? t('dashboard.welcomeName', { name: auth.user.full_name }) : t('dashboard.welcome') }}
      </h1>
      <p class="text-gray-500 mt-1 text-sm">{{ t('dashboard.subtitle') }}</p>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-gray-100 rounded-2xl h-32" />
        <div class="grid grid-cols-2 gap-4">
          <div v-for="i in 4" :key="i" class="bg-gray-100 rounded-2xl h-24" />
        </div>
        <div class="bg-gray-100 rounded-2xl h-28" />
      </div>
      <div class="space-y-4">
        <div class="bg-gray-100 rounded-2xl h-36" />
        <div class="bg-gray-100 rounded-2xl h-48" />
      </div>
    </div>

    <template v-else>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Main column -->
        <div class="lg:col-span-2 space-y-6">

          <!-- Continue Learning hero -->
          <div
            v-if="progress.continueLesson"
            class="bg-gradient-to-br from-[#234ecc] to-[#1a3ba8] rounded-2xl p-6 text-white"
          >
            <p class="text-white/60 text-xs uppercase tracking-wider font-medium mb-1">{{ t('dashboard.continueLearning') }}</p>
            <p class="text-white/80 text-sm mb-1">{{ progress.continueLesson.subject_title }}</p>
            <p class="text-xl font-bold mb-4">{{ progress.continueLesson.lesson_title }}</p>
            <RouterLink
              :to="{ name: 'lesson', params: { lessonSlug: progress.continueLesson.lesson_slug } }"
              class="inline-flex items-center gap-2 bg-white text-[#234ecc] font-semibold text-sm rounded-xl px-5 py-2.5 hover:bg-white/90 transition-colors"
            >
              {{ t('dashboard.resume') }}
              <svg class="w-4 h-4 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>

          <!-- Stats grid (2×2) -->
          <div class="grid grid-cols-2 gap-4">
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <div class="w-10 h-10 rounded-xl bg-[#234ecc]/10 flex items-center justify-center mb-3">
                <svg class="w-5 h-5 text-[#234ecc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="text-2xl sm:text-3xl font-bold text-gray-900">{{ progress.totalCompleted }}</div>
              <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lessonsCompleted') }}</div>
            </div>
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <div class="w-10 h-10 rounded-xl bg-purple-50 flex items-center justify-center mb-3">
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
              <div class="text-2xl sm:text-3xl font-bold text-gray-900">{{ progress.enrolledTracks.length }}</div>
              <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.tracksEnrolled') }}</div>
            </div>
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <div class="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center mb-3">
                <svg class="w-5 h-5 text-orange-500" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248ZM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1A5.99 5.99 0 0112 12.75a.75.75 0 01.75.75v.008l-.001.008a3.75 3.75 0 013.001 2.734Z" clip-rule="evenodd"/>
                </svg>
              </div>
              <div class="text-2xl sm:text-3xl font-bold text-gray-900">{{ progress.currentStreak }}</div>
              <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.dayStreak') }}</div>
            </div>
            <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
              <div class="w-10 h-10 rounded-xl bg-teal-50 flex items-center justify-center mb-3">
                <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="text-2xl sm:text-3xl font-bold text-gray-900">{{ lastActivityLabel }}</div>
              <div class="text-xs text-gray-500 mt-1">{{ t('dashboard.lastActivity') }}</div>
            </div>
          </div>

          <!-- Enrolled tracks with subject breakdown -->
          <div v-if="progress.enrolledTracks.length > 0">
            <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">{{ t('dashboard.yourTracks') }}</h2>
            <div class="space-y-3">
              <div
                v-for="slug in progress.enrolledTracks"
                :key="slug"
                class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm"
              >
                <div v-if="trackStats[slug]">
                  <div class="flex items-start justify-between mb-3">
                    <RouterLink
                      :to="{ name: 'track', params: { trackSlug: slug } }"
                      class="font-semibold text-gray-900 hover:text-[#234ecc] transition-colors"
                    >
                      {{ trackStats[slug].track_title }}
                    </RouterLink>
                    <span class="text-sm font-semibold text-[#234ecc] ms-4 shrink-0">
                      {{ trackStats[slug].percent }}%
                    </span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-2 mb-3">
                    <div
                      class="bg-[#234ecc] h-2 rounded-full transition-all duration-500"
                      :style="{ width: trackStats[slug].percent + '%' }"
                    />
                  </div>
                  <p class="text-xs text-gray-400 mb-3">
                    {{ t('dashboard.lessonsProgress', { completed: trackStats[slug].completed_lessons, total: trackStats[slug].total_lessons }) }}
                  </p>
                  <!-- Subject breakdown -->
                  <div v-if="trackStats[slug]?.subjects?.length" class="mt-3 space-y-1.5 border-t border-gray-50 pt-3">
                    <div
                      v-for="subj in trackStats[slug].subjects"
                      :key="subj.subject_slug"
                      class="flex items-center gap-3 text-xs"
                    >
                      <span class="text-gray-500 truncate w-28">{{ subj.subject_title }}</span>
                      <div class="flex-1 bg-gray-100 rounded-full h-1.5">
                        <div class="bg-[#234ecc]/50 h-1.5 rounded-full" :style="{ width: subj.percent + '%' }" />
                      </div>
                      <span class="text-gray-400 w-7 text-right">{{ subj.percent }}%</span>
                    </div>
                  </div>
                </div>
                <div v-else class="animate-pulse flex items-center gap-3">
                  <div class="bg-gray-100 rounded h-4 flex-1" />
                  <div class="bg-gray-100 rounded h-4 w-10" />
                </div>
              </div>
            </div>
          </div>

          <!-- Empty state -->
          <div v-else class="bg-blue-50 border border-blue-100 rounded-2xl p-8 text-center">
            <div class="mb-3 flex justify-center">
              <svg class="w-12 h-12 text-[#234ecc]/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
            </div>
            <h2 class="font-semibold text-gray-900 mb-1">{{ t('dashboard.emptyTitle') }}</h2>
            <p class="text-gray-500 text-sm mb-5">{{ t('dashboard.emptyDesc') }}</p>
            <RouterLink
              to="/learn"
              class="inline-block bg-[#234ecc] hover:bg-[#1a3ba8] text-white px-6 py-2.5 rounded-xl text-sm font-semibold transition-colors"
            >
              {{ t('dashboard.browseCurriculum') }}
            </RouterLink>
          </div>

        </div>

        <!-- Sidebar -->
        <div class="lg:col-span-1 space-y-4">

          <!-- Streak card -->
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm text-center">
            <svg class="w-10 h-10 text-orange-400 mx-auto mb-2" viewBox="0 0 24 24" fill="currentColor">
              <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248ZM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1A5.99 5.99 0 0112 12.75a.75.75 0 01.75.75v.008l-.001.008a3.75 3.75 0 013.001 2.734Z" clip-rule="evenodd"/>
            </svg>
            <div class="text-4xl font-black text-gray-900">{{ progress.currentStreak }}</div>
            <div class="text-sm text-gray-500 mt-1">{{ t('dashboard.dayStreak') }}</div>
            <div v-if="progress.longestStreak > 1" class="text-xs text-gray-400 mt-1">
              {{ t('dashboard.bestStreak', { count: progress.longestStreak }) }}
            </div>
          </div>

          <!-- Quick links -->
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-4">Explore</p>
            <div class="space-y-1">
              <RouterLink to="/learn" class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-50 text-gray-700 hover:text-[#234ecc] transition-colors group">
                <div class="w-8 h-8 rounded-lg bg-[#234ecc]/10 flex items-center justify-center group-hover:bg-[#234ecc]/20 transition-colors">
                  <svg class="w-4 h-4 text-[#234ecc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                  </svg>
                </div>
                <span class="text-sm font-medium">Browse Curriculum</span>
              </RouterLink>
              <RouterLink to="/library" class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-50 text-gray-700 hover:text-[#234ecc] transition-colors group">
                <div class="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center group-hover:bg-purple-100 transition-colors">
                  <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
                  </svg>
                </div>
                <span class="text-sm font-medium">Open Library</span>
              </RouterLink>
              <RouterLink to="/videos" class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-gray-50 text-gray-700 hover:text-[#234ecc] transition-colors group">
                <div class="w-8 h-8 rounded-lg bg-red-50 flex items-center justify-center group-hover:bg-red-100 transition-colors">
                  <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                  </svg>
                </div>
                <span class="text-sm font-medium">Watch Videos</span>
              </RouterLink>
            </div>
          </div>

        </div>
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
  await Promise.all(
    progress.enrolledTracks.map(async (slug) => {
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
