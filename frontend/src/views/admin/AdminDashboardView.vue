<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Overview</h1>
      <p class="text-gray-400 text-sm mt-0.5">Platform activity at a glance.</p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-6 animate-pulse">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="n in 4" :key="n" class="bg-gray-100 rounded-2xl h-24" />
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div class="bg-gray-100 rounded-2xl h-72" />
        <div class="bg-gray-100 rounded-2xl h-72" />
      </div>
    </div>

    <template v-else-if="stats">
      <!-- Stat cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <p class="text-xs text-gray-400 mb-1">Total users</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.total_users.toLocaleString() }}</p>
          <p class="text-[11px] text-gray-400 mt-1">{{ stats.verified_users.toLocaleString() }} verified</p>
        </div>
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <p class="text-xs text-gray-400 mb-1">Active last 7 days</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.active_users_7d.toLocaleString() }}</p>
          <p class="text-[11px] text-gray-400 mt-1">read a lesson</p>
        </div>
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <p class="text-xs text-gray-400 mb-1">Lessons completed</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.total_lessons_completed.toLocaleString() }}</p>
          <p class="text-[11px] text-gray-400 mt-1">{{ stats.published_lessons.toLocaleString() }} published lessons</p>
        </div>
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <p class="text-xs text-gray-400 mb-1">Feedback average</p>
          <p class="text-2xl font-bold text-gray-900">{{ stats.feedback_average || '—' }}<span v-if="stats.feedback_average" class="text-sm text-gray-400">/5</span></p>
          <p class="text-[11px] text-gray-400 mt-1">{{ stats.feedback_count.toLocaleString() }} responses</p>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-sm font-semibold text-gray-900">New signups</h2>
            <div class="flex rounded-lg border border-gray-200 overflow-hidden text-xs">
              <button
                v-for="d in [7, 30, 90]"
                :key="d"
                @click="days = d"
                class="px-2.5 py-1 transition-colors"
                :class="days === d ? 'bg-[#234ecc] text-white font-semibold' : 'text-gray-500 hover:text-gray-700'"
              >
                {{ d }}d
              </button>
            </div>
          </div>
          <div class="h-56">
            <Line :data="signupsData" :options="lineOptions" />
          </div>
        </div>

        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
          <h2 class="text-sm font-semibold text-gray-900 mb-4">Readers, last 7 days</h2>
          <div class="h-56">
            <Bar :data="readersData" :options="barOptions" />
          </div>
        </div>
      </div>

      <!-- Top tracks -->
      <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-sm font-semibold text-gray-900">Top tracks by completions</h2>
          <RouterLink :to="{ name: 'admin-curriculum' }" class="text-xs font-semibold text-[#234ecc] hover:text-[#1a3ba8]">
            Manage curriculum →
          </RouterLink>
        </div>
        <div v-if="stats.top_tracks.length === 0" class="text-sm text-gray-400 py-6 text-center">No completions yet.</div>
        <div v-else class="space-y-2">
          <div v-for="t in stats.top_tracks" :key="t.track_slug" class="flex items-center gap-3 text-sm">
            <span class="text-gray-700 flex-1 truncate">{{ t.track_slug }}</span>
            <span class="text-gray-400">{{ t.completions.toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Line, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, BarElement, Tooltip, Filler,
} from 'chart.js'
import { adminApi } from '@/api/admin'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Tooltip, Filler)

const stats = ref(null)
const loading = ref(true)
const error = ref('')
const days = ref(30)

const BRAND = '#234ecc'

function shortDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
}

const signupsData = computed(() => {
  const series = stats.value?.signups_series || []
  return {
    labels: series.map(p => shortDate(p.date)),
    datasets: [{
      label: 'Signups',
      data: series.map(p => p.count),
      borderColor: BRAND,
      backgroundColor: `${BRAND}22`,
      fill: true,
      tension: 0.35,
      pointRadius: 0,
      pointHoverRadius: 4,
    }],
  }
})

const readersData = computed(() => {
  const series = stats.value?.readers_series || []
  return {
    labels: series.map(p => shortDate(p.date)),
    datasets: [{
      label: 'Readers',
      data: series.map(p => p.count),
      backgroundColor: BRAND,
      borderRadius: 6,
      maxBarThickness: 28,
    }],
  }
})

const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#0c0c0e',
      padding: 10,
      cornerRadius: 8,
      titleFont: { size: 12 },
      bodyFont: { size: 12 },
    },
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 11 }, color: '#9ca3af' } },
    y: { beginAtZero: true, ticks: { precision: 0, font: { size: 11 }, color: '#9ca3af' }, grid: { color: '#f3f4f6' } },
  },
}
const lineOptions = commonOptions
const barOptions = commonOptions

async function load() {
  loading.value = true
  error.value = ''
  try {
    stats.value = await adminApi.getOverviewStats(days.value)
  } catch {
    error.value = 'Could not load dashboard stats. Make sure your account has Analytics access.'
  } finally {
    loading.value = false
  }
}

watch(days, load)
onMounted(load)
</script>
