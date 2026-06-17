<template>
  <div class="max-w-2xl mx-auto px-4 py-10">

    <nav class="text-sm text-gray-400 mb-8 flex items-center gap-2">
      <RouterLink to="/admin" class="hover:text-emerald-700 transition-colors">Admin</RouterLink>
      <span>/</span>
      <span class="text-gray-600">{{ isEdit ? 'Edit Subject' : 'New Subject' }}</span>
    </nav>

    <h1 class="text-2xl font-bold text-gray-900 mb-8">{{ isEdit ? 'Edit Subject' : 'New Subject' }}</h1>

    <div v-if="loadingSubject" class="space-y-4 animate-pulse">
      <div class="bg-gray-100 rounded-xl h-12" />
      <div class="bg-gray-100 rounded-xl h-12" />
    </div>

    <form v-else @submit.prevent="save" class="space-y-5">

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Track <span class="text-red-500">*</span></label>
        <select
          v-model="form.track_slug"
          required
          :disabled="isEdit"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 bg-white disabled:bg-gray-50 disabled:text-gray-500"
        >
          <option value="" disabled>Select a track…</option>
          <option v-for="t in tracks" :key="t.slug" :value="t.slug">{{ t.title }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
        <input
          v-model="form.title"
          @input="autofillSlug"
          type="text"
          required
          placeholder="e.g. Pillars of Islam"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug <span class="text-red-500">*</span></label>
        <input
          v-model="form.slug"
          @input="slugWasEdited = true"
          type="text"
          required
          placeholder="e.g. pillars-of-islam"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Description</label>
        <textarea
          v-model="form.description"
          rows="3"
          placeholder="Short description…"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400 resize-none"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1.5">Display Order</label>
        <input
          v-model.number="form.order"
          type="number"
          min="0"
          class="w-32 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
      </div>

      <div class="flex items-center justify-between bg-gray-50 border border-gray-100 rounded-xl px-5 py-4">
        <div>
          <p class="text-sm font-medium text-gray-800">Published</p>
          <p class="text-xs text-gray-400 mt-0.5">Visible to learners when on.</p>
        </div>
        <button
          type="button"
          @click="form.is_published = !form.is_published"
          class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
          :class="form.is_published ? 'bg-emerald-600' : 'bg-gray-300'"
        >
          <span
            class="inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform"
            :class="form.is_published ? 'translate-x-6' : 'translate-x-1'"
          />
        </button>
      </div>

      <div v-if="apiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
        {{ apiError }}
      </div>

      <div class="flex gap-3 pt-2">
        <button
          type="submit"
          :disabled="saving"
          class="flex-1 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white py-2.5 rounded-xl text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create Subject') }}
        </button>
        <RouterLink
          to="/admin"
          class="px-5 py-2.5 border border-gray-200 hover:border-gray-300 text-gray-600 rounded-xl text-sm font-medium transition-colors"
        >
          Cancel
        </RouterLink>
      </div>
    </form>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const form = ref({
  track_slug: route.query.track || '',
  title: '',
  slug: '',
  description: '',
  order: 0,
  is_published: false,
})
const tracks = ref([])
const loadingSubject = ref(false)
const saving = ref(false)
const apiError = ref('')
let slugWasEdited = false

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (!slugWasEdited) form.value.slug = slugify(form.value.title)
}

async function save() {
  apiError.value = ''
  saving.value = true
  try {
    if (isEdit.value) {
      await adminApi.updateSubject(route.params.slug, {
        title: form.value.title,
        slug: form.value.slug,
        description: form.value.description,
        order: form.value.order,
        is_published: form.value.is_published,
      })
    } else {
      await adminApi.createSubject(form.value)
    }
    router.push({ name: 'admin' })
  } catch (e) {
    const data = e.response?.data
    apiError.value = typeof data === 'object'
      ? Object.values(data).flat().join(' ')
      : 'Could not save subject.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  tracks.value = await adminApi.listTracks()

  if (!isEdit.value) return
  loadingSubject.value = true
  try {
    const data = await adminApi.getSubject(route.params.slug)
    form.value = {
      track_slug: data.track_slug || '',
      title: data.title,
      slug: data.slug,
      description: data.description || '',
      order: data.order ?? 0,
      is_published: data.is_published,
    }
    slugWasEdited = true
  } finally {
    loadingSubject.value = false
  }
})
</script>
