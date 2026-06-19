<template>
  <div class="px-6 py-8 max-w-5xl mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Analytics</h1>
        <p class="text-gray-400 text-sm mt-0.5">Lesson completions &amp; quiz answers across all users</p>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="n in 5" :key="n" class="bg-gray-100 rounded-2xl h-14" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <template v-else>

      <!-- Summary table -->
      <div v-if="!selectedLesson" class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
        <div class="px-5 py-4 border-b border-gray-100">
          <h2 class="font-semibold text-gray-800">Lesson Completions</h2>
          <p class="text-xs text-gray-400 mt-0.5">Click a lesson to see quiz breakdown</p>
        </div>

        <div v-if="stats.length === 0" class="px-5 py-10 text-center text-gray-400 text-sm">
          No completion data yet.
        </div>

        <table v-else class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-100 text-xs text-gray-400 uppercase tracking-wider">
              <th class="px-5 py-3 text-left font-medium">Lesson</th>
              <th class="px-5 py-3 text-right font-medium">Completions</th>
              <th class="px-5 py-3 text-right font-medium w-10"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="row in stats"
              :key="row.lesson_slug"
              @click="loadDetail(row.lesson_slug)"
              class="border-b border-gray-50 last:border-0 hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <td class="px-5 py-3 font-medium text-gray-800 font-mono text-xs">{{ row.lesson_slug }}</td>
              <td class="px-5 py-3 text-right">
                <span class="inline-flex items-center justify-center bg-[#234ecc]/10 text-[#234ecc] text-xs font-bold rounded-full px-2.5 py-0.5 min-w-[2rem]">
                  {{ row.completion_count }}
                </span>
              </td>
              <td class="px-5 py-3 text-right text-gray-300 hover:text-[#234ecc] transition-colors">
                <svg class="w-4 h-4 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Lesson detail: quiz breakdown -->
      <template v-else>
        <button
          @click="selectedLesson = null; detail = null"
          class="flex items-center gap-1.5 text-sm text-[#234ecc] hover:text-[#1a3ba8] mb-5 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to all lessons
        </button>

        <!-- Detail loading -->
        <div v-if="detailLoading" class="space-y-3 animate-pulse">
          <div class="bg-gray-100 rounded-2xl h-20" />
          <div class="bg-gray-100 rounded-2xl h-40" />
        </div>

        <template v-else-if="detail">
          <!-- Completion summary -->
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm mb-5">
            <p class="text-xs text-gray-400 uppercase tracking-wider mb-1">Lesson</p>
            <p class="font-bold text-gray-900 font-mono text-sm mb-3">{{ detail.lesson_slug }}</p>
            <div class="flex items-center gap-2">
              <span class="text-3xl font-black text-[#234ecc]">{{ detail.completion_count }}</span>
              <span class="text-gray-500 text-sm">users completed this lesson</span>
            </div>
          </div>

          <!-- Quiz blocks -->
          <div v-if="Object.keys(detail.quiz_stats).length === 0" class="text-center py-10 text-gray-400 text-sm bg-white border border-gray-100 rounded-2xl">
            No quiz attempts recorded for this lesson.
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="(quiz, blockOrder) in detail.quiz_stats"
              :key="blockOrder"
              class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm"
            >
              <!-- Quiz header -->
              <div class="bg-gray-50 px-5 py-4 border-b border-gray-100">
                <p class="text-[10px] font-bold uppercase tracking-widest text-gray-400 mb-1">
                  Quiz Block {{ blockOrder }}
                </p>
                <p class="font-semibold text-gray-800 text-sm">{{ quiz.question || '—' }}</p>
                <div class="flex items-center gap-4 mt-2 text-xs text-gray-400">
                  <span>{{ quiz.total_attempts }} attempt{{ quiz.total_attempts !== 1 ? 's' : '' }}</span>
                  <span class="text-emerald-600 font-semibold">
                    {{ quiz.correct_count }} correct
                    ({{ quiz.total_attempts > 0 ? Math.round(quiz.correct_count / quiz.total_attempts * 100) : 0 }}%)
                  </span>
                </div>
              </div>

              <!-- Answer distribution -->
              <div class="p-5 space-y-2.5">
                <div
                  v-for="(count, idx) in answerDistribution(quiz)"
                  :key="idx"
                  class="flex items-center gap-3"
                >
                  <span
                    class="flex-shrink-0 w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center"
                    :class="Number(idx) === quiz.correct_index
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-gray-100 text-gray-500'"
                  >
                    {{ ['A','B','C','D'][Number(idx)] }}
                  </span>
                  <div class="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div
                      class="h-2 rounded-full transition-all duration-500"
                      :class="Number(idx) === quiz.correct_index ? 'bg-emerald-500' : 'bg-gray-300'"
                      :style="{ width: barWidth(count, quiz.total_attempts) + '%' }"
                    />
                  </div>
                  <span class="text-xs text-gray-500 w-12 text-right">
                    {{ count }} <span class="text-gray-300">({{ barWidth(count, quiz.total_attempts) }}%)</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </template>

    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { progressApi } from '@/api/progress'

const stats = ref([])
const loading = ref(true)
const error = ref('')
const selectedLesson = ref(null)
const detail = ref(null)
const detailLoading = ref(false)

function answerDistribution(quiz) {
  // Return ordered by index 0,1,2,3
  const dist = quiz.answer_distribution || {}
  const maxIdx = Math.max(...Object.keys(dist).map(Number), 3)
  const result = {}
  for (let i = 0; i <= maxIdx; i++) {
    result[i] = dist[String(i)] || 0
  }
  return result
}

function barWidth(count, total) {
  if (!total) return 0
  return Math.round(count / total * 100)
}

async function loadDetail(slug) {
  selectedLesson.value = slug
  detailLoading.value = true
  try {
    detail.value = await progressApi.getAdminLessonStats(slug)
  } catch {
    detail.value = null
  } finally {
    detailLoading.value = false
  }
}

onMounted(async () => {
  try {
    stats.value = await progressApi.getAdminLessonStats(null)
  } catch {
    error.value = 'Could not load analytics. Make sure your account has admin access.'
  } finally {
    loading.value = false
  }
})
</script>
