<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Content Overview</h1>
        <p class="text-gray-500 text-sm mt-0.5">Manage tracks, subjects, lessons and books.</p>
      </div>
      <div class="flex items-center gap-2">
        <RouterLink :to="{ name: 'admin-track-new' }" class="bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-3 py-2 rounded-lg transition-colors">
          + Track
        </RouterLink>
        <RouterLink :to="{ name: 'admin-subject-new' }" class="bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-3 py-2 rounded-lg transition-colors">
          + Subject
        </RouterLink>
        <RouterLink :to="{ name: 'admin-lesson-new' }" class="bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-3 py-2 rounded-lg transition-colors">
          + Lesson
        </RouterLink>
      </div>
    </div>

    <!-- Stats grid -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="w-8 h-8 rounded-lg bg-[#234ecc]/10 flex items-center justify-center mb-3">
          <svg class="w-4 h-4 text-[#234ecc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ stats.tracks.total }}</div>
        <div class="text-xs text-gray-500 mt-1">Tracks</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ stats.tracks.published }} published · {{ stats.tracks.draft }} draft</div>
      </div>
      <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="w-8 h-8 rounded-lg bg-purple-50 flex items-center justify-center mb-3">
          <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ stats.subjects.total }}</div>
        <div class="text-xs text-gray-500 mt-1">Subjects</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ stats.subjects.published }} published · {{ stats.subjects.draft }} draft</div>
      </div>
      <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="w-8 h-8 rounded-lg bg-orange-50 flex items-center justify-center mb-3">
          <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ stats.lessons.total }}</div>
        <div class="text-xs text-gray-500 mt-1">Lessons</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ stats.lessons.published }} published · {{ stats.lessons.draft }} draft</div>
      </div>
      <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center mb-3">
          <svg class="w-4 h-4 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"/>
          </svg>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ stats.books.total }}</div>
        <div class="text-xs text-gray-500 mt-1">Books</div>
        <div class="text-xs text-gray-400 mt-0.5">{{ stats.books.published }} published · {{ stats.books.draft }} draft</div>
      </div>
    </div>

    <!-- Curriculum section header -->
    <h2 class="text-base font-semibold text-gray-700 mb-4">Curriculum</h2>

    <!-- Loading skeleton -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="i in 3" :key="i" class="bg-gray-100 rounded-2xl h-16" />
    </div>

    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">
      {{ error }}
    </div>

    <!-- Curriculum tree -->
    <div v-else class="space-y-3">
      <div v-if="tracks.length === 0" class="text-gray-400 text-sm py-8 text-center">
        No tracks yet. Create your first track to get started.
      </div>

      <div
        v-for="track in tracks"
        :key="track.slug"
        class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm"
      >
        <!-- Track header row -->
        <div class="px-5 py-4 flex items-center gap-3">
          <button
            @click="toggleExpand(track.slug)"
            class="shrink-0 w-6 h-6 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-transform duration-200"
            :class="expandedTracks.has(track.slug) ? 'rotate-90' : ''"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
          <span
            class="shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full"
            :class="track.is_published ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
          >
            {{ track.is_published ? 'Published' : 'Draft' }}
          </span>
          <span class="font-semibold text-gray-900 truncate flex-1">{{ track.title }}</span>
          <div class="flex items-center gap-1 shrink-0">
            <button
              @click="togglePublishTrack(track)"
              :title="track.is_published ? 'Unpublish' : 'Publish'"
              class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-500 transition-colors"
            >
              <svg v-if="track.is_published" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
              </svg>
            </button>
            <RouterLink
              :to="{ name: 'admin-track-edit', params: { slug: track.slug } }"
              title="Edit track"
              class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </RouterLink>
            <RouterLink
              :to="{ name: 'admin-subject-new', query: { track: track.slug } }"
              title="Add subject"
              class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
            </RouterLink>
            <button
              @click="confirmDelete({ type: 'track', item: track })"
              title="Delete track"
              class="w-8 h-8 rounded-lg bg-gray-100 hover:bg-red-50 hover:text-red-500 flex items-center justify-center text-gray-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Subjects (collapsible) -->
        <div v-show="expandedTracks.has(track.slug)" class="border-t border-gray-100">
          <div v-if="loadingSubjects[track.slug]" class="px-12 py-3 text-xs text-gray-400 animate-pulse">
            Loading…
          </div>
          <div v-else-if="!subjects[track.slug]?.length" class="px-12 py-3 text-xs text-gray-400 italic">
            No subjects yet.
          </div>
          <div
            v-for="subj in subjects[track.slug]"
            :key="subj.slug"
            class="flex items-center gap-3 px-5 py-3 pl-12 border-b border-gray-50 last:border-0 hover:bg-gray-50/60"
          >
            <span class="shrink-0 w-2 h-2 rounded-full" :class="subj.is_published ? 'bg-emerald-500' : 'bg-gray-300'" />
            <span class="text-sm text-gray-700 truncate flex-1">{{ subj.title }}</span>
            <div class="flex items-center gap-1 shrink-0">
              <button
                @click="togglePublishSubject(subj)"
                :title="subj.is_published ? 'Unpublish' : 'Publish'"
                class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-400 transition-colors"
              >
                <svg v-if="subj.is_published" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                </svg>
              </button>
              <RouterLink
                :to="{ name: 'admin-subject-edit', params: { slug: subj.slug } }"
                title="Edit subject"
                class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-400 transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </RouterLink>
              <RouterLink
                :to="{ name: 'admin-lesson-new', query: { subject: subj.slug } }"
                title="Add lesson"
                class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-400 transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
              </RouterLink>
              <button
                @click="confirmDelete({ type: 'subject', item: subj, trackSlug: track.slug })"
                title="Delete subject"
                class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-red-50 hover:text-red-500 flex items-center justify-center text-gray-400 transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete modal -->
    <div
      v-if="deleteTarget"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
      @click.self="deleteTarget = null"
    >
      <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-2">
          Delete {{ deleteTarget.type === 'track' ? 'Track' : 'Subject' }}?
        </h3>
        <p class="text-sm text-gray-500 mb-5">
          "<strong>{{ deleteTarget.item.title }}</strong>" will be permanently deleted. This cannot be undone.
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
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const tracks = ref([])
const subjects = ref({})
const loadingSubjects = reactive({})
const expandedTracks = ref(new Set())
const loading = ref(true)
const error = ref('')
const deleteTarget = ref(null)
const deleting = ref(false)

const stats = ref({
  tracks:   { total: 0, published: 0, draft: 0 },
  subjects: { total: 0, published: 0, draft: 0 },
  lessons:  { total: 0, published: 0, draft: 0 },
  books:    { total: 0, published: 0, draft: 0 },
})

function toggleExpand(slug) {
  const s = new Set(expandedTracks.value)
  if (s.has(slug)) s.delete(slug)
  else s.add(slug)
  expandedTracks.value = s
}

async function loadSubjects(trackSlug) {
  loadingSubjects[trackSlug] = true
  try {
    subjects.value[trackSlug] = await adminApi.listSubjects(trackSlug)
  } finally {
    loadingSubjects[trackSlug] = false
  }
}

async function togglePublishTrack(track) {
  const prev = track.is_published
  track.is_published = !prev
  try {
    await adminApi.updateTrack(track.slug, { is_published: track.is_published })
    recomputeTrackStats()
  } catch {
    track.is_published = prev
  }
}

async function togglePublishSubject(subj) {
  const prev = subj.is_published
  subj.is_published = !prev
  try {
    await adminApi.updateSubject(subj.slug, { is_published: subj.is_published })
    recomputeSubjectStats()
  } catch {
    subj.is_published = prev
  }
}

function recomputeTrackStats() {
  const all = tracks.value
  stats.value.tracks = {
    total: all.length,
    published: all.filter(t => t.is_published).length,
    draft: all.filter(t => !t.is_published).length,
  }
}

function recomputeSubjectStats() {
  const all = Object.values(subjects.value).flat()
  stats.value.subjects = {
    total: all.length,
    published: all.filter(s => s.is_published).length,
    draft: all.filter(s => !s.is_published).length,
  }
}

function confirmDelete(target) {
  deleteTarget.value = target
}

async function doDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    const { type, item, trackSlug } = deleteTarget.value
    if (type === 'track') {
      await adminApi.deleteTrack(item.slug)
      tracks.value = tracks.value.filter(t => t.slug !== item.slug)
      delete subjects.value[item.slug]
      recomputeTrackStats()
      recomputeSubjectStats()
    } else {
      await adminApi.deleteSubject(item.slug)
      if (trackSlug && subjects.value[trackSlug]) {
        subjects.value[trackSlug] = subjects.value[trackSlug].filter(s => s.slug !== item.slug)
      }
      recomputeSubjectStats()
    }
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  try {
    const [tracksData, booksData] = await Promise.all([
      adminApi.listTracks(),
      adminApi.listBooks(),
    ])
    tracks.value = tracksData

    await Promise.all(tracksData.map(t => loadSubjects(t.slug)))

    let lessonsData = []
    try {
      lessonsData = await adminApi.listLessons()
    } catch {
      // listLessons without subject filter may not be supported — counts stay 0
    }

    const allSubjects = Object.values(subjects.value).flat()
    stats.value = {
      tracks: {
        total: tracksData.length,
        published: tracksData.filter(t => t.is_published).length,
        draft: tracksData.filter(t => !t.is_published).length,
      },
      subjects: {
        total: allSubjects.length,
        published: allSubjects.filter(s => s.is_published).length,
        draft: allSubjects.filter(s => !s.is_published).length,
      },
      lessons: {
        total: lessonsData.length,
        published: lessonsData.filter(l => l.status === 'published').length,
        draft: lessonsData.filter(l => l.status !== 'published').length,
      },
      books: {
        total: booksData.length,
        published: booksData.filter(b => b.is_published).length,
        draft: booksData.filter(b => !b.is_published).length,
      },
    }
  } catch (e) {
    error.value = 'Could not load content. Make sure your account has author access.'
  } finally {
    loading.value = false
  }
})
</script>
