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
      <div class="mb-10">
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">{{ subject.title }}</h1>
        <p class="text-gray-500">{{ subject.description }}</p>
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
          class="group flex items-center gap-3 sm:gap-4 bg-white border border-gray-100 rounded-xl px-4 py-3 sm:px-5 sm:py-4 shadow-sm hover:shadow-md hover:border-emerald-200 transition-all"
        >
          <span class="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center text-sm font-semibold group-hover:bg-emerald-100 transition-colors">
            {{ idx + 1 }}
          </span>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-gray-900 group-hover:text-emerald-700 transition-colors truncate">
              {{ lesson.title }}
            </p>
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { curriculumApi } from '@/api/curriculum'

const route = useRoute()
const { t } = useI18n()
const subject = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    subject.value = await curriculumApi.getSubject(route.params.subjectSlug)
  } catch (e) {
    error.value = e.response?.status === 404 ? t('subject.notFound') : t('subject.loadError')
  } finally {
    loading.value = false
  }
})
</script>
