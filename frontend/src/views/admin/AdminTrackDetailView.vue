<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Breadcrumb -->
    <nav class="text-sm text-gray-400 mb-6 flex items-center gap-2">
      <RouterLink to="/admin" class="hover:text-gray-600 transition-colors">Admin</RouterLink>
      <span>/</span>
      <span class="text-gray-900 font-medium">{{ track?.title || '…' }}</span>
    </nav>

    <!-- Skeleton -->
    <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-3">
        <div class="bg-gray-100 rounded-2xl h-16" />
        <div class="bg-gray-100 rounded-2xl h-16" />
        <div class="bg-gray-100 rounded-2xl h-16" />
      </div>
      <div class="bg-gray-100 rounded-2xl h-72" />
    </div>

    <div v-else-if="!track" class="text-center py-16 text-gray-400">Track not found.</div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Main: subjects + lessons -->
      <div class="lg:col-span-2 space-y-4">

        <!-- Subjects header -->
        <div class="flex items-center justify-between">
          <h2 class="text-base font-semibold text-gray-700">
            Subjects
            <span class="ml-1.5 text-xs font-normal text-gray-400">({{ subjects.length }})</span>
          </h2>
          <RouterLink
            :to="{ name: 'admin-subject-new', query: { track: route.params.slug } }"
            class="text-sm font-semibold text-[#234ecc] hover:underline transition-colors"
          >
            + Add Subject
          </RouterLink>
        </div>

        <!-- Empty state -->
        <div v-if="subjects.length === 0" class="text-sm text-gray-400 py-12 text-center border-2 border-dashed border-gray-200 rounded-2xl">
          No subjects yet. Add your first subject above.
        </div>

        <!-- Subject accordion cards -->
        <div class="space-y-3">
          <div
            v-for="subj in subjects"
            :key="subj.slug"
            class="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm transition-shadow hover:shadow-md"
          >
            <!-- Subject header -->
            <div class="flex items-center gap-3 px-5 py-4">
              <button
                @click="toggleSubject(subj.slug)"
                class="shrink-0 w-6 h-6 flex items-center justify-center text-gray-400 hover:text-gray-600 transition-transform duration-200"
                :class="expanded.has(subj.slug) ? 'rotate-90' : ''"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                </svg>
              </button>

              <span
                class="shrink-0 text-xs font-semibold px-2 py-0.5 rounded-full"
                :class="subj.is_published ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
              >
                {{ subj.is_published ? 'Published' : 'Draft' }}
              </span>

              <span class="font-semibold text-gray-900 flex-1 truncate">{{ subj.title }}</span>

              <span class="text-xs text-gray-400 shrink-0 mr-2">
                {{ (lessons[subj.slug] || []).length }} lessons
              </span>

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
                  @click="deleteTarget = { type: 'subject', item: subj }"
                  title="Delete subject"
                  class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-red-50 hover:text-red-500 flex items-center justify-center text-gray-400 transition-colors"
                >
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Lessons (expandable) -->
            <div v-show="expanded.has(subj.slug)" class="border-t border-gray-100">
              <div v-if="loadingLessons[subj.slug]" class="px-8 py-3 text-xs text-gray-400 animate-pulse">
                Loading lessons…
              </div>
              <div v-else-if="!lessons[subj.slug]?.length" class="px-8 py-4 text-sm text-gray-400 italic text-center">
                No lessons yet in this subject.
              </div>

              <div
                v-for="lesson in lessons[subj.slug]"
                :key="lesson.slug"
                class="flex items-center gap-3 px-8 py-3 border-b border-gray-50 last:border-0 hover:bg-gray-50/50 transition-colors"
              >
                <span
                  class="shrink-0 text-[10px] font-semibold px-1.5 py-0.5 rounded-full"
                  :class="lesson.status === 'published' ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
                >
                  {{ lesson.status === 'published' ? 'Live' : 'Draft' }}
                </span>
                <span class="text-sm text-gray-700 flex-1 truncate">{{ lesson.title }}</span>
                <span class="text-xs text-gray-400 shrink-0">{{ lesson.block_count }} blocks · {{ lesson.estimated_minutes }}m</span>

                <div class="flex items-center gap-1 shrink-0">
                  <button
                    @click="togglePublishLesson(lesson, subj.slug)"
                    :title="lesson.status === 'published' ? 'Unpublish' : 'Publish'"
                    class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-400 transition-colors"
                  >
                    <svg v-if="lesson.status === 'published'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
                    </svg>
                  </button>

                  <RouterLink
                    :to="{ name: 'admin-lesson-edit', params: { slug: lesson.slug } }"
                    title="Edit lesson"
                    class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-[#234ecc]/10 hover:text-[#234ecc] flex items-center justify-center text-gray-400 transition-colors"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </RouterLink>

                  <button
                    @click="deleteTarget = { type: 'lesson', item: lesson, subjectSlug: subj.slug }"
                    title="Delete lesson"
                    class="w-7 h-7 rounded-lg bg-gray-100 hover:bg-red-50 hover:text-red-500 flex items-center justify-center text-gray-400 transition-colors"
                  >
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Add lesson footer -->
              <div class="px-8 py-3 border-t border-gray-50 bg-gray-50/50">
                <RouterLink
                  :to="{ name: 'admin-lesson-new', query: { subject: subj.slug } }"
                  class="text-xs font-medium text-[#234ecc] hover:underline"
                >
                  + Add Lesson to {{ subj.title }}
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar: Track Settings -->
      <div class="lg:col-span-1">
        <div class="lg:sticky lg:top-24 bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">

          <!-- Sidebar header -->
          <div class="px-5 py-4 border-b border-gray-100">
            <h3 class="text-sm font-semibold text-gray-700">Track Settings</h3>
          </div>

          <div class="p-5 space-y-4">

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Title <span class="text-red-500">*</span></label>
              <input
                v-model="form.title"
                @input="autofillSlug"
                type="text"
                placeholder="Track title"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Slug</label>
              <div class="flex gap-1.5">
                <input
                  v-model="form.slug"
                  @input="slugEdited = true"
                  type="text"
                  class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-xs font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                />
                <button
                  type="button"
                  @click="regenerateSlug"
                  class="px-2.5 py-2 text-xs text-gray-400 border border-gray-200 rounded-xl hover:border-[#234ecc]/40 hover:text-[#234ecc] transition-colors whitespace-nowrap"
                >
                  Regen
                </button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Description</label>
              <textarea
                v-model="form.description"
                rows="3"
                placeholder="Short description…"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
              />
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Thumbnail URL</label>
              <input
                v-model="form.thumbnail_url"
                type="url"
                placeholder="https://…"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <div v-if="form.thumbnail_url" class="mt-2 rounded-xl overflow-hidden h-20 bg-gray-100">
                <img :src="form.thumbnail_url" class="w-full h-full object-cover" />
              </div>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Display Order</label>
              <input
                v-model.number="form.order"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>

            <!-- Published toggle -->
            <div class="flex items-center justify-between py-1 border-t border-gray-100 pt-3">
              <div>
                <p class="text-sm font-medium text-gray-700">Published</p>
                <p class="text-xs text-gray-400 mt-0.5">Visible to all learners.</p>
              </div>
              <button
                type="button"
                @click="form.is_published = !form.is_published"
                class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
                :class="form.is_published ? 'bg-[#234ecc]' : 'bg-gray-300'"
              >
                <span
                  class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                  :class="form.is_published ? 'translate-x-4' : 'translate-x-1'"
                />
              </button>
            </div>

            <div v-if="saveError" class="text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
              {{ saveError }}
            </div>
            <div v-if="saveSuccess" class="text-xs text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-lg px-3 py-2">
              Track saved successfully.
            </div>

            <button
              type="button"
              @click="saveTrack"
              :disabled="saving"
              class="w-full bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white py-2.5 rounded-xl text-sm font-semibold transition-colors"
            >
              {{ saving ? 'Saving…' : 'Save Track' }}
            </button>

            <!-- Stats -->
            <div class="pt-3 border-t border-gray-100 space-y-1 text-xs text-gray-400">
              <p>{{ subjects.length }} subject{{ subjects.length !== 1 ? 's' : '' }}</p>
              <p>{{ totalLessons }} lesson{{ totalLessons !== 1 ? 's' : '' }}</p>
              <RouterLink
                :to="{ name: 'admin-track-edit', params: { slug: route.params.slug } }"
                class="block text-[#234ecc] hover:underline mt-1"
              >
                Advanced editor ↗
              </RouterLink>
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
          Delete {{ deleteTarget.type === 'subject' ? 'Subject' : 'Lesson' }}?
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()

const track = ref(null)
const subjects = ref([])
const lessons = reactive({})
const loadingLessons = reactive({})
const expanded = ref(new Set())
const loading = ref(true)
const saving = ref(false)
const deleting = ref(false)
const deleteTarget = ref(null)
const saveError = ref('')
const saveSuccess = ref(false)
let slugEdited = false

const form = ref({
  title: '',
  slug: '',
  description: '',
  thumbnail_url: '',
  order: 0,
  is_published: false,
})

const totalLessons = computed(() =>
  Object.values(lessons).reduce((sum, arr) => sum + arr.length, 0)
)

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (!slugEdited) form.value.slug = slugify(form.value.title)
}

function regenerateSlug() {
  form.value.slug = slugify(form.value.title)
  slugEdited = false
}

function toggleSubject(slug) {
  const s = new Set(expanded.value)
  if (s.has(slug)) {
    s.delete(slug)
  } else {
    s.add(slug)
    if (!lessons[slug]) loadLessons(slug)
  }
  expanded.value = s
}

async function loadLessons(subjectSlug) {
  loadingLessons[subjectSlug] = true
  try {
    lessons[subjectSlug] = await adminApi.listLessons(subjectSlug)
  } finally {
    loadingLessons[subjectSlug] = false
  }
}

async function togglePublishSubject(subj) {
  const prev = subj.is_published
  subj.is_published = !prev
  try {
    await adminApi.updateSubject(subj.slug, { is_published: subj.is_published })
  } catch {
    subj.is_published = prev
  }
}

async function togglePublishLesson(lesson, subjectSlug) {
  const prev = lesson.status
  lesson.status = prev === 'published' ? 'draft' : 'published'
  try {
    await adminApi.updateLesson(lesson.slug, { status: lesson.status })
  } catch {
    lesson.status = prev
  }
}

async function saveTrack() {
  saveError.value = ''
  saveSuccess.value = false
  saving.value = true
  try {
    const updated = await adminApi.updateTrack(route.params.slug, {
      title: form.value.title,
      slug: form.value.slug,
      description: form.value.description,
      thumbnail_url: form.value.thumbnail_url,
      order: form.value.order,
      is_published: form.value.is_published,
    })
    track.value = updated
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (e) {
    const data = e.response?.data
    saveError.value = typeof data === 'object' ? Object.values(data).flat().join(' ') : 'Could not save track.'
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  if (!deleteTarget.value) return
  deleting.value = true
  try {
    const { type, item, subjectSlug } = deleteTarget.value
    if (type === 'subject') {
      await adminApi.deleteSubject(item.slug)
      subjects.value = subjects.value.filter(s => s.slug !== item.slug)
    } else {
      await adminApi.deleteLesson(item.slug)
      if (subjectSlug && lessons[subjectSlug]) {
        lessons[subjectSlug] = lessons[subjectSlug].filter(l => l.slug !== item.slug)
      }
    }
    deleteTarget.value = null
  } finally {
    deleting.value = false
  }
}

onMounted(async () => {
  try {
    const [trackData, subjectsData] = await Promise.all([
      adminApi.getTrack(route.params.slug),
      adminApi.listSubjects(route.params.slug),
    ])
    track.value = trackData
    subjects.value = subjectsData
    form.value = {
      title: trackData.title,
      slug: trackData.slug,
      description: trackData.description || '',
      thumbnail_url: trackData.thumbnail_url || '',
      order: trackData.order ?? 0,
      is_published: trackData.is_published,
    }
    slugEdited = true

    // Pre-load lessons for all subjects so counts are visible
    await Promise.all(subjectsData.map(s => loadLessons(s.slug)))
  } catch {
    track.value = null
  } finally {
    loading.value = false
  }
})
</script>
