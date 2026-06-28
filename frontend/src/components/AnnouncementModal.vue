<template>
  <div
    v-if="current"
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-[60] p-4 backdrop-blur-sm"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden">
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 px-6 py-4 border-b border-gray-100 shrink-0">
        <h2 class="text-lg font-bold text-gray-900">{{ current.title }}</h2>
        <button
          @click="close"
          :title="t('announce.close')"
          class="shrink-0 -me-1 -mt-1 w-8 h-8 rounded-lg inline-flex items-center justify-center text-gray-400 hover:text-gray-700 hover:bg-gray-100 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Content (scrollable) -->
      <div class="px-6 py-5 overflow-y-auto">
        <BlockRenderer :blocks="current.content_blocks || []" />
      </div>

      <!-- Footer -->
      <div class="px-6 py-3 border-t border-gray-100 flex justify-end shrink-0">
        <button
          @click="close"
          class="px-5 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white text-sm font-semibold rounded-xl transition-colors"
        >
          {{ queue.length > 1 ? t('announce.next') : t('announce.close') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { announcementsApi } from '@/api/announcements'
import BlockRenderer from '@/components/blocks/BlockRenderer.vue'

const route = useRoute()
const auth = useAuthStore()
const { t } = useI18n()

const queue = ref([])
const fetched = ref(false)
const viewed = new Set()

// Don't surface modals on full-screen chrome (admin / launch) pages.
const current = computed(() =>
  (!route.meta.fullScreen && queue.value.length) ? queue.value[0] : null
)

async function load() {
  if (fetched.value) return
  fetched.value = true
  try {
    queue.value = await announcementsApi.getActive()
  } catch {
    queue.value = []
  }
}

// Record a view the first time each announcement is actually shown.
watch(current, (a) => {
  if (a && !viewed.has(a.id)) {
    viewed.add(a.id)
    announcementsApi.recordView(a.id).catch(() => {})
  }
}, { immediate: true })

function close() {
  const a = queue.value[0]
  if (a) announcementsApi.dismiss(a.id).catch(() => {})
  queue.value.shift()  // reveal the next queued modal, if any
}

// Fetch once the user is logged in and their profile is loaded.
watch(
  () => auth.isLoggedIn && !!auth.user,
  (ready) => { if (ready) load() },
  { immediate: true },
)
</script>
