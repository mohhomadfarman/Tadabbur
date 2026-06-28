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
          class="group relative bg-white border rounded-2xl p-6 shadow-sm hover:shadow-md transition-all"
          :class="subjectStatus(subject.slug) === 'completed'
            ? 'border-emerald-200 hover:border-emerald-300'
            : subjectStatus(subject.slug) === 'inprogress'
              ? 'border-blue-100 hover:border-blue-200'
              : 'border-gray-100 hover:border-emerald-200'"
        >
          <!-- Status badge (top-right corner) -->
          <!-- Completed: green tick -->
          <span
            v-if="subjectStatus(subject.slug) === 'completed'"
            class="absolute top-4 right-4 rtl:right-auto rtl:left-4 w-7 h-7 rounded-full bg-emerald-100 flex items-center justify-center"
            :title="t('track.subjectCompleted')"
          >
            <svg class="w-4 h-4 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"/>
            </svg>
          </span>
          <!-- In Progress: blue play dot -->
          <span
            v-else-if="subjectStatus(subject.slug) === 'inprogress'"
            class="absolute top-4 right-4 rtl:right-auto rtl:left-4 inline-flex items-center gap-1
                   text-[10px] font-bold uppercase tracking-wider bg-blue-50 text-[#234ecc]
                   border border-blue-200 px-2 py-0.5 rounded-full"
            :title="t('track.subjectInProgress')"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-[#234ecc] animate-pulse inline-block"></span>
            {{ t('track.subjectInProgress') }}
          </span>

          <h3
            class="font-semibold text-gray-900 group-hover:text-emerald-700 transition-colors mb-2"
            :class="subjectStatus(subject.slug) === 'completed' ? 'pr-9 rtl:pr-0 rtl:pl-9' : ''"
          >
            {{ subject.title }}
          </h3>
          <p class="text-sm text-gray-500 line-clamp-2 mb-4">{{ subject.description }}</p>

          <!-- Progress mini-bar (only when enrolled and has some progress) -->
          <div
            v-if="subjectData(subject.slug) && subjectData(subject.slug).total_lessons > 0"
            class="mb-4"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="text-[11px] text-gray-400">
                {{ subjectData(subject.slug).completed_lessons }}/{{ subjectData(subject.slug).total_lessons }} {{ t('track.lessons') }}
              </span>
              <span class="text-[11px] font-medium"
                :class="subjectStatus(subject.slug) === 'completed' ? 'text-emerald-600' : 'text-[#234ecc]'">
                {{ subjectData(subject.slug).percent }}%
              </span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
              <div
                class="h-1.5 rounded-full transition-all duration-500"
                :class="subjectStatus(subject.slug) === 'completed' ? 'bg-emerald-500' : 'bg-[#234ecc]'"
                :style="{ width: subjectData(subject.slug).percent + '%' }"
              />
            </div>
          </div>

          <span class="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
            {{ t('track.viewLessons') }}
            <svg class="w-3.5 h-3.5 icon-dir" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </span>
        </RouterLink>
      </div>
    </template>

    <!-- Language choice on enroll -->
    <EnrollLanguageModal
      v-if="showEnrollModal"
      :track-title="track?.title || ''"
      :languages="languages"
      :enrolling="progress.enrolling"
      @confirm="confirmEnroll"
      @cancel="showEnrollModal = false"
    />

  </div>
</template>

<script setup>
import { ref, onMounted, onServerPrefetch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'
import { useAuthStore } from '@/stores/auth'
import { useProgressStore } from '@/stores/progress'
import EnrollLanguageModal from '@/components/EnrollLanguageModal.vue'
import { useSsrDataStore } from '@/stores/ssrData'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

const route = useRoute()
const auth = useAuthStore()
const progress = useProgressStore()
const ssr = useSsrDataStore()
const { t } = useI18n()

const ssrKey = `track:${route.params.trackSlug}`
const track = ref(ssr.get(ssrKey))
const loading = ref(track.value == null)
const error = ref('')
const trackProgressData = ref(null)

const showEnrollModal = ref(false)
const languages = ref([])
const languagesLoaded = ref(false)

// Prerender the public track so its subjects + SEO meta land in the static HTML.
onServerPrefetch(async () => {
  try {
    track.value = await curriculumApi.getTrack(route.params.trackSlug)
    ssr.set(ssrKey, track.value)
  } catch {
    /* leave empty; client surfaces the error */
  } finally {
    loading.value = false
  }
})

useSeo(() => {
  const tr = track.value
  if (!tr) return {}
  const url = `${SEO_ORIGIN}/learn/${tr.slug}`
  return {
    title: tr.meta_title || tr.title,
    description: tr.meta_description || tr.description,
    url,
    image: tr.og_image || tr.thumbnail_url || undefined,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'Course',
      name: tr.title,
      description: tr.description,
      url,
      provider: { '@type': 'Organization', name: 'Tadabbur', url: SEO_ORIGIN },
    },
  }
})

function subjectData(slug) {
  return trackProgressData.value?.subjects?.find(s => s.subject_slug === slug) ?? null
}

function subjectStatus(slug) {
  const d = subjectData(slug)
  if (!d || d.total_lessons === 0) return null
  if (d.percent === 100) return 'completed'
  if (d.completed_lessons > 0) return 'inprogress'
  return null
}

async function handleEnroll() {
  // Offer a language choice when translations are available; otherwise enroll directly.
  if (!languagesLoaded.value) {
    try { languages.value = await curriculumApi.getLanguages() } catch { languages.value = [] }
    languagesLoaded.value = true
  }
  if (languages.value.length) {
    showEnrollModal.value = true
  } else {
    await progress.enrollTrack(track.value.slug)
  }
}

async function confirmEnroll(language) {
  await progress.enrollTrack(track.value.slug, language)
  showEnrollModal.value = false
}

onMounted(async () => {
  try {
    // Keep the prerendered/hydrated track; only fetch if we have nothing yet.
    if (!track.value) {
      track.value = await curriculumApi.getTrack(route.params.trackSlug)
    }
    if (auth.isLoggedIn) {
      await progress.fetchProgress()
      // Always fetch fresh — don't serve a stale cached 0% result
      delete progress.trackProgressCache[route.params.trackSlug]
      trackProgressData.value = await progress.fetchTrackProgress(route.params.trackSlug)
    }
  } catch (e) {
    error.value = e.response?.status === 404 ? t('track.notFound') : t('track.loadError')
  } finally {
    loading.value = false
  }
})
</script>
