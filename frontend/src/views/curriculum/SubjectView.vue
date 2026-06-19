<template>
  <div class="max-w-4xl mx-auto px-4 py-6 sm:py-12">

    <!-- Breadcrumb -->
    <nav class="text-sm text-gray-400 mb-8 flex items-center gap-2 flex-wrap">
      <RouterLink to="/learn" class="hover:text-emerald-700 transition-colors">{{ t('nav.learn') }}</RouterLink>
      <span>/</span>
      <RouterLink
        v-if="subject"
        :to="{ name: 'track', params: { trackSlug: $route.params.trackSlug } }"
        class="hover:text-emerald-700 transition-colors"
      >
        {{ subject.track_title }}
      </RouterLink>
      <span>/</span>
      <span class="text-gray-600">{{ subject?.title || '…' }}</span>
    </nav>

    <!-- Loading -->
    <div v-if="loading">
      <div class="bg-gray-100 rounded-2xl h-20 w-2/3 mb-10 animate-pulse" />
      <div class="space-y-3">
        <div v-for="n in 4" :key="n" class="bg-gray-100 rounded-xl h-16 animate-pulse" />
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <template v-else-if="subject">
      <!-- Subject header -->
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">{{ subject.title }}</h1>
        <p class="text-gray-500">{{ subject.description }}</p>
      </div>

      <!-- Progress bar (logged-in users only) -->
      <div v-if="auth.isLoggedIn && totalLessons > 0" class="mb-8 bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-2.5">
          <span class="text-sm font-medium text-gray-700">{{ t('subject.progressLabel') }}</span>
          <span class="text-sm font-semibold" :class="completedCount === totalLessons ? 'text-emerald-600' : 'text-gray-600'">
            {{ completedCount }}/{{ totalLessons }} {{ t('subject.lessonsCompleted') }}
          </span>
        </div>
        <div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
          <div
            class="h-2 rounded-full transition-all duration-700 ease-out"
            :class="completedCount === totalLessons ? 'bg-emerald-500' : 'bg-[#234ecc]'"
            :style="{ width: progressPercent + '%' }"
          />
        </div>
        <p class="mt-1.5 text-xs text-gray-400">{{ Math.round(progressPercent) }}% {{ t('subject.percentComplete') }}</p>
      </div>

      <!-- Lesson list -->
      <h2 class="text-lg font-semibold text-gray-700 mb-4">{{ t('subject.lessons') }}</h2>

      <div v-if="subject.lessons?.length === 0" class="text-gray-400 text-sm">
        {{ t('subject.noLessons') }}
      </div>

      <div v-else class="space-y-3">
        <RouterLink
          v-for="(lesson, idx) in subject.lessons"
          :key="lesson.id"
          :to="{ name: 'lesson', params: { lessonSlug: lesson.slug } }"
          class="group flex items-center gap-3 sm:gap-4 bg-white border rounded-xl px-4 py-3 sm:px-5 sm:py-4 shadow-sm hover:shadow-md transition-all"
          :class="isCompleted(lesson.slug)
            ? 'border-emerald-200 hover:border-emerald-300'
            : isInProgress(lesson.slug)
              ? 'border-blue-200 hover:border-blue-300'
              : 'border-gray-100 hover:border-emerald-200'"
        >
          <!-- Status circle -->
          <span
            class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-colors"
            :class="isCompleted(lesson.slug)
              ? 'bg-emerald-100 text-emerald-700'
              : isInProgress(lesson.slug)
                ? 'bg-blue-50 text-[#234ecc]'
                : 'bg-gray-50 text-gray-500 group-hover:bg-emerald-50 group-hover:text-emerald-700'"
          >
            <!-- Checkmark -->
            <svg v-if="isCompleted(lesson.slug)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"/>
            </svg>
            <!-- Play icon -->
            <svg v-else-if="isInProgress(lesson.slug)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                clip-rule="evenodd"/>
            </svg>
            <!-- Number -->
            <span v-else>{{ idx + 1 }}</span>
          </span>

          <!-- Title + badge -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <p
                class="font-medium transition-colors truncate"
                :class="isCompleted(lesson.slug)
                  ? 'text-gray-400 group-hover:text-emerald-600'
                  : 'text-gray-900 group-hover:text-emerald-700'"
              >
                {{ lesson.title }}
              </p>
              <span
                v-if="isCompleted(lesson.slug)"
                class="flex-shrink-0 text-[10px] font-bold uppercase tracking-wider bg-emerald-50 text-emerald-700 border border-emerald-200 px-1.5 py-0.5 rounded-full"
              >
                {{ t('subject.statusCompleted') }}
              </span>
              <span
                v-else-if="isInProgress(lesson.slug)"
                class="flex-shrink-0 text-[10px] font-bold uppercase tracking-wider bg-blue-50 text-[#234ecc] border border-blue-200 px-1.5 py-0.5 rounded-full"
              >
                {{ t('subject.statusInProgress') }}
              </span>
            </div>
            <p v-if="lesson.summary" class="text-xs text-gray-400 truncate mt-0.5">{{ lesson.summary }}</p>
          </div>

          <span v-if="lesson.estimated_minutes" class="flex-shrink-0 text-xs text-gray-400 whitespace-nowrap">
            {{ lesson.estimated_minutes }} {{ t('subject.min') }}
          </span>
        </RouterLink>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const { t } = useI18n()
const auth = useAuthStore()
const progress = useProgressStore()

const subject = ref(null)
const loading = ref(true)
const error = ref('')

const totalLessons = computed(() => subject.value?.lessons?.length ?? 0)

const completedCount = computed(() => {
  if (!subject.value?.lessons) return 0
  return subject.value.lessons.filter(l => progress.isCompleted(l.slug)).length
})

const progressPercent = computed(() =>
  totalLessons.value > 0 ? (completedCount.value / totalLessons.value) * 100 : 0
)

function isCompleted(slug) {
  return auth.isLoggedIn && progress.isCompleted(slug)
}

function isInProgress(slug) {
  return auth.isLoggedIn
    && progress.continueLesson?.lesson_slug === slug
    && !progress.isCompleted(slug)
}

onMounted(async () => {
  try {
    subject.value = await curriculumApi.getSubject(route.params.subjectSlug)
    if (auth.isLoggedIn) await progress.fetchProgress()
  } catch (e) {
    error.value = e.response?.status === 404 ? t('subject.notFound') : t('subject.loadError')
  } finally {
    loading.value = false
  }
})
</script>
