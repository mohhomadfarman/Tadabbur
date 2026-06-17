<template>
  <div class="max-w-3xl mx-auto px-4 py-10">

    <nav class="text-sm text-gray-400 mb-8 flex items-center gap-2">
      <RouterLink to="/admin" class="hover:text-emerald-700 transition-colors">Admin</RouterLink>
      <span>/</span>
      <span class="text-gray-600">{{ isEdit ? 'Edit Lesson' : 'New Lesson' }}</span>
    </nav>

    <div class="flex items-start justify-between mb-8 gap-4">
      <h1 class="text-2xl font-bold text-gray-900">{{ isEdit ? 'Edit Lesson' : 'New Lesson' }}</h1>
      <!-- Publish toggle top -->
      <div class="flex items-center gap-3 shrink-0">
        <span class="text-sm text-gray-500">{{ form.status === 'published' ? 'Published' : 'Draft' }}</span>
        <button
          type="button"
          @click="toggleStatus"
          class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
          :class="form.status === 'published' ? 'bg-emerald-600' : 'bg-gray-300'"
        >
          <span
            class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform"
            :class="form.status === 'published' ? 'translate-x-6' : 'translate-x-1'"
          />
        </button>
      </div>
    </div>

    <div v-if="loadingLesson" class="space-y-4 animate-pulse">
      <div class="bg-gray-100 rounded-xl h-12" />
      <div class="bg-gray-100 rounded-xl h-12" />
      <div class="bg-gray-100 rounded-xl h-32" />
    </div>

    <div v-else class="space-y-6">

      <!-- Metadata -->
      <div class="bg-white border border-gray-100 rounded-2xl shadow-sm p-6 space-y-4">
        <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Lesson Info</h2>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject <span class="text-red-500">*</span></label>
          <select
            v-model="form.subject_slug"
            required
            :disabled="isEdit"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 bg-white disabled:bg-gray-50"
          >
            <option value="" disabled>Select a subject…</option>
            <optgroup v-for="track in tracks" :key="track.slug" :label="track.title">
              <option
                v-for="subj in subjectsByTrack[track.slug] || []"
                :key="subj.slug"
                :value="subj.slug"
              >
                {{ subj.title }}
              </option>
            </optgroup>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
          <input
            v-model="form.title"
            @input="autofillSlug"
            type="text"
            required
            placeholder="e.g. The Five Pillars of Islam"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug</label>
          <input
            v-model="form.slug"
            @input="slugWasEdited = true"
            type="text"
            placeholder="auto-generated"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-emerald-400"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Summary</label>
          <textarea
            v-model="form.summary"
            rows="2"
            placeholder="Brief description shown in lesson lists…"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none"
          />
        </div>

        <div class="flex gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Est. Minutes</label>
            <input
              v-model.number="form.estimated_minutes"
              type="number" min="0"
              class="w-28 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Order</label>
            <input
              v-model.number="form.order"
              type="number" min="0"
              class="w-28 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
          </div>
        </div>
      </div>

      <!-- Content blocks -->
      <div class="bg-white border border-gray-100 rounded-2xl shadow-sm p-6">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Content Blocks</h2>
          <span class="text-xs text-gray-400">{{ form.content_blocks.length }} block{{ form.content_blocks.length !== 1 ? 's' : '' }}</span>
        </div>

        <!-- Block list -->
        <div class="space-y-3 mb-5">
          <div v-if="form.content_blocks.length === 0" class="text-center text-gray-400 text-sm py-6">
            No blocks yet. Add one below.
          </div>

          <div
            v-for="(block, idx) in form.content_blocks"
            :key="idx"
            class="border border-gray-100 rounded-xl overflow-hidden"
          >
            <!-- Block header -->
            <div class="flex items-center justify-between bg-gray-50 px-4 py-2 gap-2">
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-400">#{{ idx + 1 }}</span>
                <span class="text-xs font-semibold text-gray-600 uppercase tracking-wide">{{ block.type }}</span>
              </div>
              <div class="flex items-center gap-1">
                <button type="button" @click="moveBlock(idx, -1)" :disabled="idx === 0"
                  class="p-1 text-gray-400 hover:text-gray-700 disabled:opacity-30">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                  </svg>
                </button>
                <button type="button" @click="moveBlock(idx, 1)" :disabled="idx === form.content_blocks.length - 1"
                  class="p-1 text-gray-400 hover:text-gray-700 disabled:opacity-30">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </button>
                <button type="button" @click="removeBlock(idx)"
                  class="p-1 text-red-300 hover:text-red-500 ml-1">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Block body fields -->
            <div class="p-4 space-y-3">

              <!-- Text -->
              <template v-if="block.type === 'text'">
                <textarea v-model="block.body.text" rows="4" placeholder="Paragraph text…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-y" />
              </template>

              <!-- Verse -->
              <template v-else-if="block.type === 'verse'">
                <textarea v-model="block.body.arabic" rows="2" placeholder="Arabic text (with harakat)…" dir="rtl"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-lg text-right arabic-text focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none" />
                <textarea v-model="block.body.translation" rows="2" placeholder="English translation…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none" />
                <div class="flex gap-3">
                  <input v-model="block.body.surah" type="text" placeholder="Surah name"
                    class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                  <input v-model.number="block.body.ayah" type="number" placeholder="Ayah #"
                    class="w-28 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                </div>
              </template>

              <!-- Hadith -->
              <template v-else-if="block.type === 'hadith'">
                <textarea v-model="block.body.text" rows="3" placeholder="Hadith text (English)…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-y" />
                <input v-model="block.body.source" type="text" placeholder="Source (e.g. Sahih Bukhari 1)"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                <input v-model="block.body.narrator" type="text" placeholder="Narrator (optional)"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
              </template>

              <!-- Image -->
              <template v-else-if="block.type === 'image'">
                <input v-model="block.body.url" type="url" placeholder="Image URL (MinIO or external)…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                <input v-model="block.body.caption" type="text" placeholder="Caption (optional)"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                <img v-if="block.body.url" :src="block.body.url" class="rounded-xl max-h-40 object-cover mt-1" />
              </template>

              <!-- Video -->
              <template v-else-if="block.type === 'video'">
                <input v-model="block.body.url" type="url" placeholder="Video URL (YouTube or MinIO)…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                <input v-model="block.body.caption" type="text" placeholder="Caption (optional)"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
              </template>

              <!-- Quiz -->
              <template v-else-if="block.type === 'quiz'">
                <input v-model="block.body.question" type="text" placeholder="Question…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400" />
                <div class="space-y-2">
                  <div v-for="(opt, oi) in (block.body.options || ['', '', '', ''])" :key="oi"
                    class="flex items-center gap-2">
                    <input
                      type="radio"
                      :name="`quiz-correct-${idx}`"
                      :value="oi"
                      v-model="block.body.correct"
                      class="accent-emerald-600"
                      title="Mark as correct answer"
                    />
                    <input
                      :value="opt"
                      @input="setOption(block, oi, $event.target.value)"
                      type="text"
                      :placeholder="`Option ${['A','B','C','D'][oi]}`"
                      class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
                    />
                  </div>
                </div>
                <p class="text-xs text-gray-400">Select the radio button next to the correct answer.</p>
                <textarea v-model="block.body.explanation" rows="2" placeholder="Explanation shown after answer (optional)…"
                  class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none" />
              </template>

            </div>
          </div>
        </div>

        <!-- Add block buttons -->
        <div class="flex flex-wrap gap-2">
          <button v-for="type in BLOCK_TYPES" :key="type.value" type="button"
            @click="addBlock(type.value)"
            class="text-xs border border-gray-200 hover:border-emerald-300 hover:text-emerald-700 text-gray-500 px-3 py-1.5 rounded-lg transition-colors"
          >
            + {{ type.label }}
          </button>
        </div>
      </div>

      <!-- Error -->
      <div v-if="apiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
        {{ apiError }}
      </div>

      <!-- Save / Cancel -->
      <div class="flex gap-3">
        <button
          type="button"
          @click="save"
          :disabled="saving"
          class="flex-1 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white py-2.5 rounded-xl text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create Lesson') }}
        </button>
        <RouterLink
          to="/admin"
          class="px-5 py-2.5 border border-gray-200 hover:border-gray-300 text-gray-600 rounded-xl text-sm font-medium transition-colors"
        >
          Cancel
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const BLOCK_TYPES = [
  { value: 'text', label: 'Text' },
  { value: 'verse', label: 'Verse (Ayah)' },
  { value: 'hadith', label: 'Hadith' },
  { value: 'image', label: 'Image' },
  { value: 'video', label: 'Video' },
  { value: 'quiz', label: 'Quiz' },
]

const BLOCK_DEFAULTS = {
  text: { text: '' },
  verse: { arabic: '', translation: '', surah: '', ayah: null },
  hadith: { text: '', source: '', narrator: '' },
  image: { url: '', caption: '' },
  video: { url: '', caption: '' },
  quiz: { question: '', options: ['', '', '', ''], correct: 0, explanation: '' },
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
