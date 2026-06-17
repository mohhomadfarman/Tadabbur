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
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-3 leading-snug">{{ lesson.title }}</h1>
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
          <p v-if="lesson.summary" class="text-gray-500 mt-4 text-base leading-relaxed">
            {{ lesson.summary }}
          </p>
        </div>

        <hr class="border-gray-100 mb-8" />

        <!-- Content blocks -->
        <div class="space-y-7">
          <div v-for="block in lesson.content_blocks" :key="block.order">

            <!-- Text -->
            <p v-if="block.type === 'text'" class="text-gray-700 leading-relaxed text-[1.05rem]">
              {{ block.body.text }}
            </p>

            <!-- Verse -->
            <div
              v-else-if="block.type === 'verse'"
              class="bg-emerald-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-emerald-500 rounded-r-2xl rtl:rounded-r-none rtl:rounded-l-2xl px-4 py-4 sm:px-6 sm:py-5"
            >
              <p class="text-2xl text-right arabic-text text-gray-900 leading-loose mb-3 font-medium">
                {{ block.body.arabic }}
              </p>
              <p class="text-gray-600 italic text-sm mb-2">"{{ block.body.translation }}"</p>
              <p class="text-xs text-emerald-700 font-medium">
                {{ t('lesson.surah') }} {{ block.body.surah }}, {{ t('lesson.ayah') }} {{ block.body.ayah }}
              </p>
            </div>

            <!-- Hadith -->
            <div
              v-else-if="block.type === 'hadith'"
              class="bg-amber-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-amber-400 rounded-r-2xl rtl:rounded-r-none rtl:rounded-l-2xl px-4 py-4 sm:px-6 sm:py-5"
            >
              <p class="text-gray-700 italic mb-3 leading-relaxed">"{{ block.body.text }}"</p>
              <p class="text-xs text-amber-700 font-medium">— {{ block.body.source }}</p>
              <p v-if="block.body.narrator" class="text-xs text-amber-600 mt-0.5">
                {{ t('lesson.narratedBy') }} {{ block.body.narrator }}
              </p>
            </div>

            <!-- Image -->
            <figure v-else-if="block.type === 'image'" class="rounded-2xl overflow-hidden">
              <img :src="block.body.url" :alt="block.body.caption || ''" class="w-full object-cover" />
              <figcaption v-if="block.body.caption" class="text-xs text-center text-gray-400 mt-2 px-2">
                {{ block.body.caption }}
              </figcaption>
            </figure>

            <!-- Video -->
            <div v-else-if="block.type === 'video'" class="rounded-2xl overflow-hidden bg-gray-900">
              <div v-if="youtubeId(block.body.url)" class="aspect-video">
                <iframe
                  :src="`https://www.youtube.com/embed/${youtubeId(block.body.url)}`"
                  class="w-full h-full"
                  frameborder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowfullscreen
                />
              </div>
              <video v-else controls class="w-full aspect-video">
                <source :src="block.body.url" />
              </video>
              <p v-if="block.body.caption" class="text-xs text-center text-gray-400 py-2 px-4">
                {{ block.body.caption }}
              </p>
            </div>

            <!-- Quiz -->
            <div v-else-if="block.type === 'quiz'" class="border border-gray-200 rounded-2xl overflow-hidden">
              <div class="bg-gray-50 px-5 py-4 border-b border-gray-200">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">{{ t('lesson.quickCheck') }}</p>
                <p class="font-medium text-gray-900">{{ block.body.question }}</p>
              </div>
              <div class="p-4 space-y-2">
                <button
                  v-for="(option, idx) in block.body.options"
                  :key="idx"
                  :disabled="quizSubmitted[block.order]"
                  @click="submitQuiz(block.order, idx, block.body.correct)"
                  class="w-full text-start px-4 py-3 rounded-xl border text-sm transition-all"
                  :class="quizOptionClass(block.order, idx, block.body.correct)"
                >
                  <span class="font-medium me-2">{{ ['A', 'B', 'C', 'D'][idx] }}.</span>
                  {{ option }}
                </button>
              </div>
              <div
                v-if="quizSubmitted[block.order] && block.body.explanation"
                class="px-5 py-3 bg-blue-50 border-t border-blue-100 text-sm text-blue-800"
              >
                <span class="font-semibold">{{ t('lesson.explanation') }}: </span>{{ block.body.explanation }}
              </div>
            </div>

          </div>
        </div>

        <!-- 25% gate -->
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

        <!-- Mark complete (logged in, full content) -->
        <div v-else-if="auth.isLoggedIn" class="mt-10 flex justify-center">
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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'

const route = useRoute()
const auth = useAuthStore()
const progress = useProgressStore()
const { t } = useI18n()

const lesson = ref(null)
const loading = ref(true)
const error = ref('')
const readingProgress = ref(0)

const quizSelected = reactive({})
const quizSubmitted = reactive({})

function youtubeId(url) {
  if (!url) return null
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/)
  return match ? match[1] : null
}

function submitQuiz(blockOrder, selectedIdx, correctIdx) {
  quizSelected[blockOrder] = selectedIdx
  quizSubmitted[blockOrder] = true
}

function quizOptionClass(blockOrder, idx, correctIdx) {
  if (!quizSubmitted[blockOrder]) {
    return 'border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 text-gray-700 cursor-pointer'
  }
  if (idx === correctIdx) return 'border-emerald-500 bg-emerald-50 text-emerald-800 cursor-default'
  if (idx === quizSelected[blockOrder]) return 'border-red-400 bg-red-50 text-red-700 cursor-default'
  return 'border-gray-100 text-gray-400 cursor-default'
}

function updateReadingProgress() {
  const scrollTop = window.scrollY
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  readingProgress.value = docHeight > 0 ? Math.min(100, Math.round((scrollTop / docHeight) * 100)) : 0
}

async function loadLesson(slug) {
  loading.value = true
  error.value = ''
  lesson.value = null
  try {
    lesson.value = await curriculumApi.getLesson(slug)
    if (auth.isLoggedIn) await progress.fetchProgress()
  } catch (e) {
    error.value = e.response?.status === 404 ? t('lesson.notFound') : t('lesson.loadError')
  } finally {
    loading.value = false
  }
}

async function handleMarkComplete() {
  await progress.markComplete(lesson.value.slug)
}

watch(() => route.params.lessonSlug, (slug) => { if (slug) loadLesson(slug) })

onMounted(() => {
  loadLesson(route.params.lessonSlug)
  window.addEventListener('scroll', updateReadingProgress)
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateReadingProgress)
})
</script>
