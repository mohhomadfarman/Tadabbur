<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Sticky top bar -->
    <div class="sticky top-0 z-10 bg-white/95 backdrop-blur border-b border-gray-200 -mx-6 px-6 py-3 flex items-center justify-between mb-8">
      <nav class="text-sm text-gray-400 flex items-center gap-2">
        <RouterLink to="/admin" class="hover:text-gray-600 transition-colors">Admin</RouterLink>
        <span>/</span>
        <span class="text-gray-600">{{ isEdit ? 'Edit Lesson' : 'New Lesson' }}</span>
      </nav>
      <div class="flex items-center gap-3">
        <span
          class="text-xs font-semibold px-2.5 py-1 rounded-full"
          :class="form.status === 'published' ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
        >
          {{ form.status === 'published' ? 'Published' : 'Draft' }}
        </span>
        <button
          type="button"
          :disabled="saving"
          @click="save"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create Lesson') }}
        </button>
        <RouterLink to="/admin" class="text-sm text-gray-500 hover:text-gray-700 transition-colors">
          Cancel
        </RouterLink>
      </div>
    </div>

    <div v-if="loadingLesson" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-gray-100 rounded-2xl h-48" />
        <div class="bg-gray-100 rounded-2xl h-64" />
      </div>
      <div class="bg-gray-100 rounded-2xl h-64" />
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left: metadata + blocks -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Metadata card -->
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
            <input
              v-model="form.title"
              @input="autofillSlug"
              type="text"
              required
              placeholder="e.g. The Five Pillars of Islam"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug</label>
            <div class="flex gap-2">
              <input
                v-model="form.slug"
                @input="slugWasEdited = true"
                type="text"
                placeholder="auto-generated"
                class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <button
                type="button"
                @click="regenerateSlug"
                class="px-3 py-2.5 text-xs text-gray-500 border border-gray-200 rounded-xl hover:border-[#234ecc]/40 hover:text-[#234ecc] transition-colors"
              >
                Regenerate
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Summary</label>
            <textarea
              v-model="form.summary"
              rows="2"
              placeholder="Brief description shown in lesson lists…"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
            />
          </div>
        </div>

        <!-- Content blocks card -->
        <div class="bg-white border border-gray-200 rounded-2xl shadow-sm overflow-hidden">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h2 class="text-sm font-semibold text-gray-700">Content Blocks</h2>
            <span class="text-xs text-gray-400">{{ form.content_blocks.length }} block{{ form.content_blocks.length !== 1 ? 's' : '' }}</span>
          </div>

          <!-- Block list -->
          <div class="p-4 space-y-3">
            <div v-if="form.content_blocks.length === 0" class="text-center text-gray-400 text-sm py-6">
              No blocks yet. Add one below.
            </div>

            <div
              v-for="(block, idx) in form.content_blocks"
              :key="idx"
              class="border border-gray-200 rounded-xl overflow-hidden"
            >
              <!-- Block header with colored type badge -->
              <div class="bg-gray-50 border-b border-gray-200 px-4 py-2.5 flex items-center gap-3">
                <span
                  class="rounded-md px-2 py-0.5 text-[11px] font-semibold uppercase tracking-wide"
                  :class="BLOCK_BADGE_CLASSES[block.type]"
                >
                  {{ block.type }}
                </span>
                <span class="text-xs text-gray-400">#{{ idx + 1 }}</span>
                <div class="flex-1" />
                <div class="flex items-center gap-1">
                  <button type="button" @click="moveBlock(idx, -1)" :disabled="idx === 0"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100 disabled:opacity-30 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                    </svg>
                  </button>
                  <button type="button" @click="moveBlock(idx, 1)" :disabled="idx === form.content_blocks.length - 1"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-gray-100 disabled:opacity-30 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </button>
                  <button type="button" @click="removeBlock(idx)"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-red-300 hover:text-red-500 hover:bg-red-50 transition-colors ml-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Block body fields -->
              <div class="p-4 space-y-3">
                <template v-if="block.type === 'text'">
                  <textarea v-model="block.body.text" rows="4" placeholder="Paragraph text…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y" />
                </template>

                <template v-else-if="block.type === 'verse'">
                  <textarea v-model="block.body.arabic" rows="2" placeholder="Arabic text (with harakat)…" dir="rtl"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-lg text-right arabic-text focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none" />
                  <textarea v-model="block.body.translation" rows="2" placeholder="English translation…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none" />
                  <div class="flex gap-3">
                    <input v-model="block.body.surah" type="text" placeholder="Surah name"
                      class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                    <input v-model.number="block.body.ayah" type="number" placeholder="Ayah #"
                      class="w-28 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  </div>
                </template>

                <template v-else-if="block.type === 'hadith'">
                  <textarea v-model="block.body.text" rows="3" placeholder="Hadith text (English)…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y" />
                  <input v-model="block.body.source" type="text" placeholder="Source (e.g. Sahih Bukhari 1)"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <input v-model="block.body.narrator" type="text" placeholder="Narrator (optional)"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                </template>

                <template v-else-if="block.type === 'image'">
                  <input v-model="block.body.url" type="url" placeholder="Image URL (MinIO or external)…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <input v-model="block.body.caption" type="text" placeholder="Caption (optional)"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <img v-if="block.body.url" :src="block.body.url" class="rounded-xl max-h-40 object-cover mt-1" />
                </template>

                <template v-else-if="block.type === 'video'">
                  <input v-model="block.body.url" type="url" placeholder="Video URL (YouTube or MinIO)…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <input v-model="block.body.caption" type="text" placeholder="Caption (optional)"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                </template>

                <template v-else-if="block.type === 'quiz'">
                  <input v-model="block.body.question" type="text" placeholder="Question…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                  <div class="space-y-2">
                    <div v-for="(opt, oi) in (block.body.options || ['', '', '', ''])" :key="oi" class="flex items-center gap-2">
                      <input type="radio" :name="`quiz-correct-${idx}`" :value="oi" v-model="block.body.correct"
                        class="accent-[#234ecc]" title="Mark as correct answer" />
                      <input :value="opt" @input="setOption(block, oi, $event.target.value)" type="text"
                        :placeholder="`Option ${['A','B','C','D'][oi]}`"
                        class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                    </div>
                  </div>
                  <p class="text-xs text-gray-400">Select the radio button next to the correct answer.</p>
                  <textarea v-model="block.body.explanation" rows="2" placeholder="Explanation shown after answer (optional)…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none" />
                </template>
              </div>
            </div>
          </div>

          <!-- Add block pills -->
          <div class="flex flex-wrap gap-2 px-4 pb-5">
            <button
              v-for="type in BLOCK_TYPES"
              :key="type.value"
              type="button"
              @click="addBlock(type.value)"
              class="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-200 hover:border-[#234ecc]/30 hover:bg-[#234ecc]/5 hover:text-[#234ecc] text-xs font-medium text-gray-500 transition-colors"
            >
              <svg class="w-3.5 h-3.5 shrink-0" :class="type.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="type.icon" />
              </svg>
              {{ type.label }}
            </button>
          </div>
        </div>

        <div v-if="apiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
          {{ apiError }}
        </div>
      </div>

      <!-- Right: sidebar -->
      <div class="lg:col-span-1 lg:sticky lg:top-24 space-y-4">
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject <span class="text-red-500">*</span></label>
            <select
              v-model="form.subject_slug"
              required
              :disabled="isEdit"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 bg-white disabled:bg-gray-50 disabled:text-gray-500"
            >
              <option value="" disabled>Select a subject…</option>
              <optgroup v-for="track in tracks" :key="track.slug" :label="track.title">
                <option v-for="subj in subjectsByTrack[track.slug] || []" :key="subj.slug" :value="subj.slug">
                  {{ subj.title }}
                </option>
              </optgroup>
            </select>
          </div>

          <div class="flex gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Order</label>
              <input
                v-model.number="form.order"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Est. Minutes</label>
              <input
                v-model.number="form.estimated_minutes"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
          </div>

          <div class="flex items-center justify-between py-1">
            <div>
              <p class="text-sm font-medium text-gray-700">Published</p>
              <p class="text-xs text-gray-400 mt-0.5">Visible to learners when on.</p>
            </div>
            <button
              type="button"
              @click="toggleStatus"
              class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
              :class="form.status === 'published' ? 'bg-[#234ecc]' : 'bg-gray-300'"
            >
              <span
                class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                :class="form.status === 'published' ? 'translate-x-4' : 'translate-x-1'"
              />
            </button>
          </div>

          <div class="pt-1 border-t border-gray-100">
            <p class="text-xs text-gray-400">{{ form.content_blocks.length }} content block{{ form.content_blocks.length !== 1 ? 's' : '' }}</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const BLOCK_TYPES = [
  {
    value: 'text', label: 'Text',
    icon: 'M4 6h16M4 12h16M4 18h7',
    iconColor: 'text-gray-500',
  },
  {
    value: 'verse', label: 'Verse (Ayah)',
    icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
    iconColor: 'text-[#234ecc]',
  },
  {
    value: 'hadith', label: 'Hadith',
    icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
    iconColor: 'text-emerald-600',
  },
  {
    value: 'image', label: 'Image',
    icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
    iconColor: 'text-orange-500',
  },
  {
    value: 'video', label: 'Video',
    icon: 'M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
    iconColor: 'text-red-500',
  },
  {
    value: 'quiz', label: 'Quiz',
    icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    iconColor: 'text-purple-500',
  },
]

const BLOCK_BADGE_CLASSES = {
  text:   'bg-gray-100 text-gray-600',
  verse:  'bg-[#234ecc]/10 text-[#234ecc]',
  hadith: 'bg-emerald-50 text-emerald-700',
  image:  'bg-orange-50 text-orange-600',
  video:  'bg-red-50 text-red-600',
  quiz:   'bg-purple-50 text-purple-600',
}

const BLOCK_DEFAULTS = {
  text:   { text: '' },
  verse:  { arabic: '', translation: '', surah: '', ayah: null },
  hadith: { text: '', source: '', narrator: '' },
  image:  { url: '', caption: '' },
  video:  { url: '', caption: '' },
  quiz:   { question: '', options: ['', '', '', ''], correct: 0, explanation: '' },
}

const form = ref({
  subject_slug: route.query.subject || '',
  title: '',
  slug: '',
  summary: '',
  estimated_minutes: 10,
  order: 0,
  status: 'draft',
  content_blocks: [],
})

const tracks = ref([])
const subjectsByTrack = ref({})
const loadingLesson = ref(false)
const saving = ref(false)
const apiError = ref('')
let slugWasEdited = false

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (!slugWasEdited) form.value.slug = slugify(form.value.title)
}

function regenerateSlug() {
  form.value.slug = slugify(form.value.title)
  slugWasEdited = false
}

function toggleStatus() {
  form.value.status = form.value.status === 'published' ? 'draft' : 'published'
}

function addBlock(type) {
  form.value.content_blocks.push({ type, body: { ...BLOCK_DEFAULTS[type] } })
}

function removeBlock(idx) {
  form.value.content_blocks.splice(idx, 1)
}

function moveBlock(idx, dir) {
  const blocks = form.value.content_blocks
  const target = idx + dir
  if (target < 0 || target >= blocks.length) return
  const tmp = blocks[idx]
  blocks[idx] = blocks[target]
  blocks[target] = tmp
}

function setOption(block, oi, val) {
  if (!block.body.options) block.body.options = ['', '', '', '']
  block.body.options[oi] = val
}

async function save() {
  apiError.value = ''
  saving.value = true
  try {
    const payload = {
      subject_slug: form.value.subject_slug,
      title: form.value.title,
      slug: form.value.slug,
      summary: form.value.summary,
      estimated_minutes: form.value.estimated_minutes,
      order: form.value.order,
      status: form.value.status,
      content_blocks: form.value.content_blocks.map((b, i) => ({
        type: b.type,
        order: i,
        body: b.body,
      })),
    }
    if (isEdit.value) {
      await adminApi.updateLesson(route.params.slug, payload)
    } else {
      await adminApi.createLesson(payload)
    }
    router.push({ name: 'admin' })
  } catch (e) {
    const data = e.response?.data
    apiError.value = typeof data === 'object'
      ? Object.values(data).flat().join(' ')
      : 'Could not save lesson.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  tracks.value = await adminApi.listTracks()
  await Promise.all(
    tracks.value.map(async (t) => {
      subjectsByTrack.value[t.slug] = await adminApi.listSubjects(t.slug)
    })
  )

  if (!isEdit.value) return
  loadingLesson.value = true
  try {
    const data = await adminApi.getLesson(route.params.slug)
    form.value = {
      subject_slug: data.subject_slug,
      title: data.title,
      slug: data.slug,
      summary: data.summary || '',
      estimated_minutes: data.estimated_minutes || 10,
      order: data.order ?? 0,
      status: data.status,
      content_blocks: (data.content_blocks || []).map(b => ({
        type: b.type,
        body: { ...BLOCK_DEFAULTS[b.type], ...b.body },
      })),
    }
    slugWasEdited = true
  } finally {
    loadingLesson.value = false
  }
})
</script>
