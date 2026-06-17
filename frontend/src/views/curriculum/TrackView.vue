<template>
  <div class="max-w-7xl mx-auto px-4 py-6 sm:py-12">

    <!-- Breadcrumb -->
    <nav class="text-sm text-gray-400 mb-8 flex items-center gap-2">
      <RouterLink to="/learn" class="hover:text-emerald-700 transition-colors">{{ t('nav.learn') }}</RouterLink>
      <span>/</span>
      <span class="text-gray-600">{{ track?.title || '…' }}</span>
    </nav>

    <!-- Loading -->
    <div v-if="loading">
      <div class="bg-gray-100 rounded-2xl h-24 w-2/3 mb-10 animate-pulse" />
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
        <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-2xl h-40 animate-pulse" />
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <template v-else-if="track">
      <!-- Track header -->
      <div class="mb-10 flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">{{ track.title }}</h1>
          <p class="text-gray-500 max-w-2xl">{{ track.description }}</p>
        </div>

        <!-- Enroll button (authenticated users only) -->
        <div v-if="auth.isLoggedIn" class="shrink-0">
          <button
            v-if="!progress.isEnrolled(track.slug)"
            :disabled="progress.enrolling"
            @click="handleEnroll"
            class="flex items-center gap-2 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white px-5 py-2.5 rounded-xl text-sm font-semibold transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            {{ progress.enrolling ? t('track.enrolling') : t('track.enroll') }}
          </button>
          <div
            v-else
            class="flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-200 px-5 py-2.5 rounded-xl text-sm font-semibold"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            {{ t('track.enrolled') }}
          </div>
        </div>
        <RouterLink
          v-else
          :to="{ name: 'login', query: { redirect: $route.fullPath } }"
          class="shrink-0 border border-emerald-300 text-emerald-700 hover:bg-emerald-50 px-5 py-2.5 rounded-xl text-sm font-semibold transition-colors"
        >
          {{ t('track.loginToEnroll') }}
        </RouterLink>
      </div>

      <!-- Subjects -->
      <h2 class="text-lg font-semibold text-gray-700 mb-5">{{ t('track.subjects') }}</h2>

      <div v-if="track.subjects?.length === 0" class="text-gray-400 text-sm">
        {{ t('track.noSubjects') }}
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 sm:gap-6">
        <RouterLink
          v-for="subject in track.subjects"
          :key="subject.id"
          :to="{ name: 'subject', params: { trackSlug: $route.params.trackSlug, subjectSlug: subject.slug } }"
          class="group bg-white border border-gray-100 rounded-2xl p-6 shadow-sm hover:shadow-md hover:border-emerald-200 transition-all"
        >
          <h3 class="font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors mb-2">
            {{ subject.title }}
          </h3>
          <p class="text-sm text-gray-500 line-clamp-2 mb-4">{{ subject.description }}</p>
          <span class="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
            {{ t('track.viewLessons') }}
            <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </span>
        </RouterLink>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const auth = useAuthStore()
const progress = useProgressStore()
const { t } = useI18n()

const track = ref(null)
const loading = ref(true)
const error = ref('')

async function handleEnroll() {
  await progress.enrollTrack(track.value.slug)
}

onMounted(async () => {
  try {
    track.value = await curriculumApi.getTrack(route.params.trackSlug)
    if (auth.isLoggedIn) await progress.fetchProgress()
  } catch (e) {
    error.value = e.response?.status === 404 ? t('track.notFound') : t('track.loadError')
  } finally {
    loading.value = false
  }
})
</script>
