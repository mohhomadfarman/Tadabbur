<template>
  <div class="max-w-5xl mx-auto px-4 py-10">

    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Content Dashboard</h1>
        <p class="text-gray-500 text-sm mt-0.5">Manage tracks, subjects, and lessons.</p>
      </div>
      <RouterLink
        :to="{ name: 'admin-track-new' }"
        class="bg-emerald-700 hover:bg-emerald-800 text-white px-4 py-2 rounded-xl text-sm font-semibold transition-colors"
      >
        + New Track
      </RouterLink>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="i in 3" :key="i" class="bg-gray-100 rounded-xl h-20" />
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <!-- Track list -->
    <div v-else class="space-y-3">
      <div v-if="tracks.length === 0" class="text-gray-400 text-sm py-8 text-center">
        No tracks yet. Create your first track to get started.
      </div>

      <div
        v-for="track in tracks"
        :key="track.slug"
        class="bg-white border border-gray-100 rounded-xl shadow-sm"
      >
        <!-- Track row -->
        <div class="flex items-center justify-between px-5 py-4 gap-3">
          <div class="flex items-center gap-3 min-w-0">
            <span
              class="shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full"
              :class="track.is_published
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-gray-100 text-gray-500'"
            >
              {{ track.is_published ? 'Published' : 'Draft' }}
            </span>
            <span class="font-semibold text-gray-900 truncate">{{ track.title }}</span>
            <span class="text-xs text-gray-400 font-mono hidden sm:block">{{ track.slug }}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <RouterLink
              :to="{ name: 'admin-subject-new', query: { track: track.slug } }"
              class="text-xs text-emerald-700 hover:underline"
            >
              + Subject
            </RouterLink>
            <RouterLink
              :to="{ name: 'admin-track-edit', params: { slug: track.slug } }"
              class="text-xs border border-gray-200 hover:border-emerald-300 text-gray-600 hover:text-emerald-700 px-3 py-1 rounded-lg transition-colors"
            >
              Edit
            </RouterLink>
            <button
              @click="confirmDeleteTrack(track)"
              class="text-xs border border-red-100 hover:border-red-300 text-red-400 hover:text-red-600 px-3 py-1 rounded-lg transition-colors"
            >
              Delete
            </button>
          </div>
        </div>

        <!-- Subjects -->
        <div v-if="subjects[track.slug]?.length" class="border-t border-gray-50 divide-y divide-gray-50">
          <div
            v-for="subj in subjects[track.slug]"
            :key="subj.slug"
            class="flex items-center justify-between px-5 py-3 pl-10 gap-3 bg-gray-50/50"
          >
            <div class="flex items-center gap-3 min-w-0">
              <span
                class="shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full"
                :class="subj.is_published
                  ? 'bg-emerald-100 text-emerald-700'
                  : 'bg-gray-100 text-gray-400'"
              >
                {{ subj.is_published ? 'Published' : 'Draft' }}
              </span>
              <span class="text-sm text-gray-700 truncate">{{ subj.title }}</span>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <RouterLink
                :to="{ name: 'admin-lesson-new', query: { subject: subj.slug } }"
                class="text-xs text-emerald-700 hover:underline"
              >
                + Lesson
              </RouterLink>
              <RouterLink
                :to="{ name: 'admin-subject-edit', params: { slug: subj.slug } }"
                class="text-xs border border-gray-200 hover:border-emerald-300 text-gray-600 hover:text-emerald-700 px-3 py-1 rounded-lg transition-colors"
              >
                Edit
              </RouterLink>
            </div>
          </div>
        </div>
        <div
          v-else-if="loadingSubjects[track.slug]"
          class="border-t border-gray-50 px-10 py-3 text-xs text-gray-400 animate-pulse"
        >
          Loading subjects…
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
          "<strong>{{ deleteTarget.title }}</strong>" will be permanently deleted. This cannot be undone.
        </p>
        <div class="flex gap-3 justify-end">
          <button @click="deleteTarget = null" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900">Cancel</button>
          <button
            :disabled="deleting"
            @click="doDeleteTrack"
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
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const tracks = ref([])
const subjects = ref({})
const loadingSubjects = ref({})
const loading = ref(true)
const error = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)

async function loadSubjects(trackSlug) {
  loadingSubjects.value[trackSlug] = true
  try {
    subjects.value[trackSlug] = await adminApi.listSubjects(trackSlug)
  } finally {
    loadingSubjects.value[trackSlug] = false
  }
}

function confirmDeleteTrack(track) {
  deleteTarget.value = track
}

async function doDeleteTrack() {
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
    // Load subjects for all tracks in parallel
    await Promise.all(tracks.value.map(t => loadSubjects(t.slug)))
  } catch (e) {
    error.value = 'Could not load content. Make sure your account has author access.'
  } finally {
    loading.value = false
  }
})
</script>
