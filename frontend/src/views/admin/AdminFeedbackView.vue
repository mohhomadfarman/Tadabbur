<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Track Feedback</h1>
      <p class="text-gray-400 text-sm mt-0.5">Ratings and comments learners left after completing a track.</p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="n in 3" :key="n" class="bg-gray-100 rounded-2xl h-40" />
    </div>

    <div v-else-if="rows.length === 0" class="py-24 text-center border-2 border-dashed border-gray-200 rounded-2xl">
      <p class="text-gray-600 font-semibold mb-1">No feedback yet</p>
      <p class="text-gray-400 text-sm">It appears here once learners complete tracks and rate them.</p>
    </div>

    <div v-else class="space-y-5">
      <div v-for="row in rows" :key="row.track_slug" class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="flex items-start justify-between gap-4 mb-4">
          <div class="min-w-0">
            <h2 class="text-sm font-semibold text-gray-900 truncate">{{ row.track_slug }}</h2>
            <p class="text-xs text-gray-400 mt-0.5">{{ row.count }} response{{ row.count === 1 ? '' : 's' }}</p>
          </div>
          <div class="text-right shrink-0">
            <div class="flex items-center gap-1.5">
              <span class="text-2xl font-bold text-gray-900">{{ row.average.toFixed(1) }}</span>
              <svg class="w-5 h-5 text-amber-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
          </div>
        </div>

        <!-- Distribution -->
        <div class="space-y-1.5 mb-4">
          <div v-for="n in [5,4,3,2,1]" :key="n" class="flex items-center gap-2 text-xs">
            <span class="w-3 text-gray-400">{{ n }}</span>
            <svg class="w-3 h-3 text-amber-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
              <div class="h-full bg-amber-400 rounded-full" :style="{ width: pct(row, n) + '%' }" />
            </div>
            <span class="w-6 text-right text-gray-400">{{ row.distribution[String(n)] || 0 }}</span>
          </div>
        </div>

        <!-- Recent comments -->
        <div v-if="row.recent_comments.length" class="pt-4 border-t border-gray-100 space-y-3">
          <p class="text-xs font-medium text-gray-500">Recent comments</p>
          <div v-for="(c, i) in row.recent_comments" :key="i" class="text-sm">
            <div class="flex items-center gap-1 mb-0.5">
              <svg v-for="s in c.rating" :key="s" class="w-3 h-3 text-amber-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
            <p class="text-gray-700">{{ c.comment }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const rows = ref([])
const loading = ref(true)
const error = ref('')

function pct(row, n) {
  if (!row.count) return 0
  return Math.round(((row.distribution[String(n)] || 0) / row.count) * 100)
}

async function load() {
  loading.value = true
  try {
    rows.value = await adminApi.listFeedback()
  } catch {
    error.value = 'Could not load feedback. Make sure your account has Feedback access.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
