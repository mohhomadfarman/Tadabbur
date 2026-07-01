<template>
  <div>
    <!-- Reading progress bar -->
    <div class="fixed top-0 left-0 right-0 z-50 h-1 bg-gray-100">
      <div
        class="h-full bg-emerald-500 transition-all duration-100"
        :style="{ width: readingProgress + '%' }"
      />
    </div>

    <div class="max-w-3xl mx-auto px-4 py-6 sm:py-12">

      <!-- Breadcrumb -->
      <nav class="text-sm text-gray-400 mb-8 flex items-center gap-2 flex-wrap">
        <RouterLink to="/learn" class="hover:text-emerald-700 transition-colors">{{ t('nav.learn') }}</RouterLink>
        <span>/</span>
        <span class="text-gray-600 truncate max-w-[140px] sm:max-w-[200px]">{{ lesson?.subject_title || '…' }}</span>
      </nav>

      <!-- Loading -->
      <div v-if="loading" class="space-y-6 animate-pulse">
        <div class="bg-gray-100 rounded-2xl h-10 w-3/4" />
        <div class="bg-gray-100 rounded-xl h-4 w-full" />
        <div class="bg-gray-100 rounded-xl h-4 w-5/6" />
        <div class="bg-gray-100 rounded-xl h-32 w-full mt-8" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-xl text-sm">
        {{ error }}
      </div>

      <template v-else-if="lesson">

        <!-- Lesson header -->
        <div class="mb-8">
          <!-- Language switcher -->
          <div v-if="lesson.available_languages?.length && features.isEnabled('ai_translation')" class="flex justify-end mb-3">
            <label class="inline-flex items-center gap-2 text-xs text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.75" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
              <select
                :value="currentLang"
                @change="changeLanguage($event.target.value)"
                class="border border-gray-200 rounded-lg px-2.5 py-1.5 text-sm bg-white text-gray-600 cursor-pointer focus:outline-none focus:ring-2 focus:ring-emerald-500/40"
              >
                <option value="">{{ t('lesson.original') }}</option>
                <option v-for="l in lesson.available_languages" :key="l.code" :value="l.code">{{ l.name }}</option>
              </select>
            </label>
          </div>

          <h1 :dir="contentDir" class="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 leading-snug">{{ lesson.title }}</h1>
          <div class="flex items-center gap-3 text-sm text-gray-400 flex-wrap">
            <span v-if="lesson.estimated_minutes" class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ lesson.estimated_minutes }} {{ t('lesson.minRead') }}
            </span>
            <span class="text-gray-200">|</span>
            <RouterLink
              :to="{ name: 'subject', params: { trackSlug: '_', subjectSlug: lesson.subject_slug } }"
              class="hover:text-emerald-700 transition-colors truncate max-w-[140px] sm:max-w-[200px]"
            >
              {{ lesson.subject_title }}
            </RouterLink>
            <span v-if="progress.isCompleted(lesson.slug)" class="flex items-center gap-1 text-emerald-600 font-medium">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              {{ t('lesson.completed') }}
            </span>
          </div>
          <p v-if="lesson.summary" :dir="contentDir" class="text-gray-500 mt-4 text-base leading-relaxed">
            {{ lesson.summary }}
          </p>
        </div>

        <hr class="border-gray-100 mb-8" />

        <!-- Enrollment gate (logged in, not enrolled) -->
        <div v-if="lesson.needs_enrollment" class="mt-2">
          <div class="border border-gray-200 rounded-2xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-br from-[#234ecc] to-[#1a3ba8] px-8 py-8 text-center text-white">
              <div class="w-14 h-14 rounded-2xl bg-white/10 flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
              <h3 class="text-xl font-bold mb-1">{{ t('lesson.enrollRequired') }}</h3>
              <p class="text-white/70 text-sm">{{ lesson.track_title }}</p>
            </div>
            <div class="bg-white px-8 py-7 text-center">
              <p class="text-gray-500 text-sm mb-6 max-w-sm mx-auto">{{ t('lesson.enrollRequiredDesc') }}</p>
              <button
                :disabled="progress.enrolling || enrolling"
                @click="handleEnroll"
                class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60
                       text-white px-8 py-3 rounded-xl font-semibold transition-colors"
              >
                <svg v-if="!progress.enrolling && !enrolling" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                {{ (progress.enrolling || enrolling) ? t('lesson.enrolling') : t('lesson.enrollBtn') }}
              </button>
            </div>
          </div>
        </div>

        <!-- Content blocks -->
        <BlockRenderer
          v-else
          :blocks="lesson.content_blocks"
          :dir="contentDir"
          @quiz-answer="onQuizAnswer"
        />

        <!-- 25% gate (unauthenticated) -->
        <div v-if="lesson.is_truncated" class="relative mt-10">
          <div class="absolute inset-x-0 -top-24 h-24 bg-gradient-to-b from-transparent to-white pointer-events-none" />
          <div class="border border-gray-200 rounded-2xl shadow-lg overflow-hidden">
            <div class="bg-gradient-to-br from-emerald-900 to-emerald-700 px-8 py-6 text-center text-white">
              <p class="text-emerald-300 text-sm mb-1">{{ t('lesson.previewNote') }}</p>
              <h3 class="text-xl font-bold">{{ t('lesson.continueReading') }}</h3>
            </div>
            <div class="bg-white px-8 py-6 text-center">
              <p class="text-gray-500 text-sm mb-6">{{ t('lesson.gateDesc') }}</p>
              <div class="flex flex-col sm:flex-row gap-3 justify-center">
                <RouterLink
                  to="/register"
                  class="bg-emerald-700 hover:bg-emerald-800 text-white px-6 py-2.5 rounded-xl font-semibold transition-colors"
                >
                  {{ t('lesson.createAccount') }}
                </RouterLink>
                <RouterLink
                  :to="{ name: 'login', query: { redirect: $route.fullPath } }"
                  class="border border-gray-200 hover:border-emerald-300 text-gray-700 px-6 py-2.5 rounded-xl font-medium transition-colors"
                >
                  {{ t('lesson.logIn') }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>

        <!-- Mark complete (enrolled, full content) -->
        <div v-else-if="auth.isLoggedIn && !lesson.needs_enrollment" class="mt-10 flex justify-center">
          <button
            v-if="!progress.isCompleted(lesson.slug)"
            :disabled="progress.marking"
            @click="handleMarkComplete"
            class="flex items-center gap-2 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white px-8 py-3 rounded-xl font-semibold transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            {{ progress.marking ? t('lesson.saving') : t('lesson.markComplete') }}
          </button>
          <div
            v-else
            class="flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-200 px-8 py-3 rounded-xl font-semibold"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            {{ t('lesson.lessonCompleted') }}
          </div>
        </div>

        <!-- Prev / Next navigation -->
        <div class="mt-12 pt-8 border-t border-gray-100 grid grid-cols-2 gap-3">
          <RouterLink
            v-if="lesson.prev_lesson"
            :to="{ name: 'lesson', params: { lessonSlug: lesson.prev_lesson.slug } }"
            class="group flex flex-col gap-1 p-4 border border-gray-100 rounded-xl hover:border-emerald-200 hover:shadow-sm transition-all"
          >
            <span class="text-xs text-gray-400 flex items-center gap-1">
              <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
              {{ t('lesson.previous') }}
            </span>
            <span class="text-sm font-medium text-gray-700 group-hover:text-emerald-700 transition-colors line-clamp-2">
              {{ lesson.prev_lesson.title }}
            </span>
          </RouterLink>
          <div v-else />

          <RouterLink
            v-if="lesson.next_lesson"
            :to="{ name: 'lesson', params: { lessonSlug: lesson.next_lesson.slug } }"
            class="group flex flex-col gap-1 p-4 border border-gray-100 rounded-xl hover:border-emerald-200 hover:shadow-sm transition-all text-end col-start-2"
          >
            <span class="text-xs text-gray-400 flex items-center gap-1 justify-end">
              {{ t('lesson.next') }}
              <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </span>
            <span class="text-sm font-medium text-gray-700 group-hover:text-emerald-700 transition-colors line-clamp-2">
              {{ lesson.next_lesson.title }}
            </span>
          </RouterLink>
        </div>

      </template>
    </div>

    <!-- Track-completion feedback prompt -->
    <FeedbackForm
      :show="showFeedback"
      :track-slug="feedbackTrackSlug"
      :track-title="feedbackTrackTitle"
      @close="onFeedbackClose"
      @submitted="onFeedbackSubmitted"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onServerPrefetch, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { progressApi } from '@/api/progress'
import BlockRenderer from '@/components/blocks/BlockRenderer.vue'
import FeedbackForm from '@/components/FeedbackForm.vue'
import { feedbackApi } from '@/api/feedback'
import { useBadgesStore } from '@/stores/badges'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'
import { useFeaturesStore } from '@/stores/features'
import { useSsrDataStore } from '@/stores/ssrData'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

const route = useRoute()
const auth = useAuthStore()
const progress = useProgressStore()
const features = useFeaturesStore()
const badges = useBadgesStore()
const ssr = useSsrDataStore()
const { t } = useI18n()

const ssrKey = `lesson:${route.params.lessonSlug}`
// Hydrate from the prerendered snapshot when present (matches the static HTML).
const lesson = ref(ssr.get(ssrKey))
const loading = ref(lesson.value == null)
const error = ref('')

// Prerender (build time): fetch the public lesson so its content + SEO meta land
// in the static HTML, and stash it for the client to hydrate from.
onServerPrefetch(async () => {
  try {
    lesson.value = await curriculumApi.getLesson(route.params.lessonSlug)
    ssr.set(ssrKey, lesson.value)
  } catch {
    /* leave empty; client will surface the error */
  } finally {
    loading.value = false
  }
})
const readingProgress = ref(0)
const enrolling = ref(false)

useSeo(() => {
  const l = lesson.value
  if (!l) return {}
  const url = `${SEO_ORIGIN}/lesson/${l.slug}`
  const desc = l.meta_description || l.summary
  return {
    title: l.meta_title || l.title,
    description: desc,
    url,
    image: l.og_image || undefined,
    noindex: l.is_beta || undefined,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'LearningResource',
      name: l.title,
      description: desc,
      url,
      learningResourceType: 'Lesson',
      timeRequired: l.estimated_minutes ? `PT${l.estimated_minutes}M` : undefined,
      isPartOf: l.subject_title
        ? {
            '@type': 'Course',
            name: l.subject_title,
            url: l.track_slug && l.subject_slug
              ? `${SEO_ORIGIN}/learn/${l.track_slug}/${l.subject_slug}`
              : undefined,
          }
        : undefined,
      provider: { '@type': 'Organization', name: 'Tadabbur', url: SEO_ORIGIN },
    },
  }
})

// ── Language switcher ────────────────────────────────────────────────────
const currentLang = computed(() => lesson.value?.active_lang || '')
const activeLangObj = computed(() =>
  (lesson.value?.available_languages || []).find(l => l.code === currentLang.value) || null
)
const contentDir = computed(() => (activeLangObj.value?.rtl ? 'rtl' : 'ltr'))

async function changeLanguage(code) {
  if (code === currentLang.value) return
  // Persist the per-track preference for logged-in learners.
  if (auth.isLoggedIn && lesson.value?.track_slug) {
    try { await progress.setTrackLanguage(lesson.value.track_slug, code) } catch { /* non-blocking */ }
  }
  await loadLesson(route.params.lessonSlug, code)
}

function onQuizAnswer({ blockOrder, selectedIndex }) {
  // Persist answer for enrolled users (fire-and-forget, non-blocking)
  if (auth.isLoggedIn && lesson.value && !lesson.value.needs_enrollment) {
    progressApi.saveQuizAnswer(lesson.value.slug, {
      block_order: blockOrder,
      selected_index: selectedIndex,
    }).catch(() => {})
  }
}

function updateReadingProgress() {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  readingProgress.value = docHeight > 0 ? Math.min(100, Math.round((scrollTop / docHeight) * 100)) : 0
}

async function loadLesson(slug, lang) {
  // Only show the skeleton when there's nothing on screen yet — keeps the
  // prerendered content visible while a logged-in refetch upgrades it in place.
  if (!lesson.value) loading.value = true
  error.value = ''
  try {
    lesson.value = await curriculumApi.getLesson(slug, lang)
    if (auth.isLoggedIn) await progress.fetchProgress()
  } catch (e) {
    error.value = e.response?.status === 404 ? t('lesson.notFound') : t('lesson.loadError')
  } finally {
    loading.value = false
  }
}

const showFeedback = ref(false)
const feedbackTrackSlug = ref('')
const feedbackTrackTitle = ref('')

async function handleMarkComplete() {
  await progress.markComplete(lesson.value.slug)
  // Pull any freshly-earned badges (the global modal pops them with confetti).
  if (features.isEnabled('badges')) await badges.fetchUnseen()
  // Only prompt for feedback if no badge celebration is queued (avoid overlap).
  if (!badges.queue.length) maybePromptFeedback()
}

// After a completion, if it finished the whole track, prompt for feedback once.
async function maybePromptFeedback() {
  const slug = lesson.value?.track_slug
  if (!slug || !features.isEnabled('track_feedback')) return
  if (localStorage.getItem(`feedback_seen_${slug}`)) return
  // Invalidate any cached track progress so the percent is fresh.
  delete progress.trackProgressCache[slug]
  const tp = await progress.fetchTrackProgress(slug)
  if (!tp || tp.percent !== 100) return
  // Skip if the learner already submitted feedback for this track on the server.
  try {
    const mine = await feedbackApi.mySubmission(slug)
    if (mine?.submitted) { localStorage.setItem(`feedback_seen_${slug}`, '1'); return }
  } catch { /* non-blocking */ }
  feedbackTrackSlug.value = slug
  feedbackTrackTitle.value = lesson.value?.track_title || ''
  showFeedback.value = true
}

function markFeedbackSeen() {
  if (feedbackTrackSlug.value) localStorage.setItem(`feedback_seen_${feedbackTrackSlug.value}`, '1')
}
function onFeedbackClose() { markFeedbackSeen(); showFeedback.value = false }
function onFeedbackSubmitted() { markFeedbackSeen(); showFeedback.value = false }

async function handleEnroll() {
  if (enrolling.value) return
  enrolling.value = true
  try {
    await progress.enrollTrack(lesson.value.track_slug)
    // Reload the lesson — backend will now return full content
    await loadLesson(route.params.lessonSlug)
  } finally {
    enrolling.value = false
  }
}

watch(() => route.params.lessonSlug, (slug) => { if (slug) loadLesson(slug) })

onMounted(() => {
  // Public content is already prerendered/hydrated; refetch only when there's
  // nothing yet, or to personalize for a logged-in user (enrollment, progress,
  // full content beyond the public preview).
  if (!lesson.value || auth.isLoggedIn) {
    loadLesson(route.params.lessonSlug)
  }
  window.addEventListener('scroll', updateReadingProgress)
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateReadingProgress)
})
</script>
