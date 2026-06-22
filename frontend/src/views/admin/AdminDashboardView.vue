<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Curriculum</h1>
        <p class="text-gray-400 text-sm mt-0.5">
          {{ filteredTracks.length }} track{{ filteredTracks.length !== 1 ? 's' : '' }}
          <template v-if="filterStatus !== 'all' || search"> matching filters</template>
        </p>
      </div>
      <RouterLink
        :to="{ name: 'admin-track-new' }"
        class="bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
      >
        + New Track
      </RouterLink>
    </div>

    <!-- Search + Sort + Filter bar -->
    <div class="flex flex-wrap gap-3 mb-6">
      <!-- Search -->
      <div class="relative flex-1 min-w-[200px] max-w-sm">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input
          v-model="search"
          type="text"
          placeholder="Search tracks…"
          class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-xl text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
        />
      </div>

      <!-- Sort -->
      <select
        v-model="sortBy"
        class="border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
      >
        <option value="published_first">Published first (default)</option>
        <option value="order">Manual order</option>
        <option value="title_asc">Title A–Z</option>
        <option value="title_desc">Title Z–A</option>
        <option value="draft_first">Drafts first</option>
      </select>

      <!-- Filter -->
      <div class="flex rounded-xl border border-gray-200 overflow-hidden bg-white text-sm">
        <button
          v-for="opt in [['all','All'], ['published','Published'], ['draft','Drafts']]"
          :key="opt[0]"
          @click="filterStatus = opt[0]"
          class="px-3 py-2 transition-colors"
          :class="filterStatus === opt[0] ? 'bg-[#234ecc] text-white font-semibold' : 'text-gray-500 hover:text-gray-700'"
        >
          {{ opt[1] }}
        </button>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 animate-pulse">
      <div v-for="i in 6" :key="i" class="bg-gray-100 rounded-2xl h-56" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <!-- Empty state -->
    <div v-else-if="filteredTracks.length === 0 && tracks.length === 0" class="text-center py-20 text-gray-400">
      <svg class="w-12 h-12 mx-auto text-gray-200 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
      </svg>
      <p class="font-medium text-gray-500 mb-1">No tracks yet</p>
      <p class="text-sm mb-4">Create your first track to start building curriculum.</p>
      <RouterLink :to="{ name: 'admin-track-new' }" class="bg-[#234ecc] text-white text-sm font-semibold px-5 py-2 rounded-xl hover:bg-[#1a3ba8] transition-colors">
        + Create Track
      </RouterLink>
    </div>

    <div v-else-if="filteredTracks.length === 0" class="text-center py-16 text-gray-400 text-sm">
      No tracks match your search or filter.
    </div>

    <!-- Track cards grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div
        v-for="track in filteredTracks"
        :key="track.slug"
        class="group bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-md hover:border-[#234ecc]/20 transition-all duration-200 flex flex-col"
      >
        <!-- Thumbnail / gradient placeholder -->
        <div class="relative aspect-[16/7] overflow-hidden shrink-0">
          <img
            v-if="track.thumbnail_url"
            :src="track.thumbnail_url"
            :alt="track.title"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="w-full h-full flex items-center justify-center text-3xl font-bold text-white/50"
            :class="gradientFor(track.title)"
          >
            {{ track.title.charAt(0).toUpperCase() }}
          </div>

          <!-- Status badge -->
          <span
            class="absolute top-2.5 right-2.5 text-xs font-semibold px-2 py-0.5 rounded-full shadow-sm"
            :class="track.is_published ? 'bg-emerald-500 text-white' : 'bg-white/95 text-gray-600 border border-gray-200'"
          >
            {{ track.is_published ? 'Published' : 'Draft' }}
          </span>

          <!-- Hover action overlay -->
          <div class="absolute top-2.5 left-2.5 hidden group-hover:flex gap-1.5">
            <button
              @click.stop="togglePublish(track)"
              :title="track.is_published ? 'Unpublish' : 'Publish'"
              class="w-7 h-7 bg-white/95 rounded-lg shadow-sm flex items-center justify-center text-gray-500 hover:text-[#234ecc] transition-colors"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="track.is_published" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
            <button
              @click.stop="deleteTarget = track"
              title="Delete track"
              class="w-7 h-7 bg-white/95 rounded-lg shadow-sm flex items-center justify-center text-gray-500 hover:text-red-500 transition-colors"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Card body -->
        <div class="p-5 flex flex-col flex-1">
          <h3 class="font-bold text-gray-900 mb-1 truncate text-base">{{ track.title }}</h3>
          <p class="text-sm text-gray-400 line-clamp-2 mb-4 flex-1 leading-relaxed">
            {{ track.description || 'No description.' }}
          </p>

          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-400">
              {{ subjectCounts[track.slug] !== undefined ? subjectCounts[track.slug] + ' subject' + (subjectCounts[track.slug] !== 1 ? 's' : '') : '…' }}
            </span>
            <RouterLink
              :to="{ name: 'admin-track-detail', params: { slug: track.slug } }"
              class="text-xs font-semibold text-[#234ecc] hover:text-[#1a3ba8] flex items-center gap-1 transition-colors"
            >
              Manage
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div
      v-if="deleteTarget"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
      @click.self="deleteTarget = null"
    >
      <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-2">Delete Track?</h3>
        <p class="text-sm text-gray-500 mb-5">
          "<strong>{{ deleteTarget.title }}</strong>" and all its content will be permanently deleted. This cannot be undone.
        </p>
        <div class="flex gap-3 justify-end">
          <button @click="deleteTarget = null" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900">Cancel</button>
          <button
            :disabled="deleting"
            @click="doDelete"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors"
          >
            {{ deleting ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const tracks = ref([])
const subjectCounts = reactive({})
const loading = ref(true)
const error = ref('')
const search = ref('')
const sortBy = ref('published_first')
const filterStatus = ref('all')
const deleteTarget = ref(null)
const deleting = ref(false)

const GRADIENTS = [
  'bg-gradient-to-br from-[#234ecc] to-[#1a3ba8]',
  'bg-gradient-to-br from-emerald-500 to-emerald-700',
  'bg-gradient-to-br from-purple-500 to-purple-700',
  'bg-gradient-to-br from-amber-500 to-orange-600',
  'bg-gradient-to-br from-rose-500 to-red-700',
  'bg-gradient-to-br from-teal-500 to-cyan-700',
  'bg-gradient-to-br from-indigo-500 to-violet-700',
  'bg-gradient-to-br from-slate-500 to-slate-700',
]

function gradientFor(title) {
  const idx = title.charCodeAt(0) % GRADIENTS.length
  return GRADIENTS[idx]
}

const filteredTracks = computed(() => {
  let list = [...tracks.value]

  if (search.value.trim()) {
    const q = search.value.toLowerCase()
    list = list.filter(t => t.title.toLowerCase().includes(q) || (t.description || '').toLowerCase().includes(q))
  }

  if (filterStatus.value === 'published') list = list.filter(t => t.is_published)
  else if (filterStatus.value === 'draft') list = list.filter(t => !t.is_published)

  if (sortBy.value === 'title_asc') list.sort((a, b) => a.title.localeCompare(b.title))
  else if (sortBy.value === 'title_desc') list.sort((a, b) => b.title.localeCompare(a.title))
  else if (sortBy.value === 'order') list.sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
  else if (sortBy.value === 'draft_first') list.sort((a, b) => Number(a.is_published) - Number(b.is_published))
  else list.sort((a, b) => (Number(b.is_published) - Number(a.is_published)) || ((a.order ?? 0) - (b.order ?? 0)))

  return list
})

async function togglePublish(track) {
  const prev = track.is_published
  track.is_published = !prev
  try {
    await adminApi.updateTrack(track.slug, { is_published: track.is_published })
  } catch {
    track.is_published = prev
  }
}

async function doDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    await adminApi.deleteTrack(deleteTarget.value.slug)
    tracks.value = tracks.value.filter(t => t.slug !== deleteTarget.value.slug)
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  try {
    tracks.value = await adminApi.listTracks()
    // Load subject counts in background (non-blocking)
    tracks.value.forEach(async (t) => {
      try {
        const subjects = await adminApi.listSubjects(t.slug)
        subjectCounts[t.slug] = subjects.length
      } catch {
        subjectCounts[t.slug] = 0
      }
    })
  } catch {
    error.value = 'Could not load tracks. Make sure your account has author access.'
  } finally {
    loading.value = false
  }
})
</script>
