<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Sticky top bar -->
    <div class="sticky top-0 z-10 bg-white/95 backdrop-blur border-b border-gray-200 -mx-6 px-6 py-3 flex items-center justify-between mb-8">
      <nav class="text-sm text-gray-400 flex items-center gap-2">
        <RouterLink to="/admin" class="hover:text-gray-600 transition-colors">Admin</RouterLink>
        <span>/</span>
        <span class="text-gray-600">{{ isEdit ? 'Edit Track' : 'New Track' }}</span>
      </nav>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-500">{{ form.is_published ? 'Published' : 'Draft' }}</span>
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
        <button
          type="button"
          :disabled="saving"
          @click="save"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create Track') }}
        </button>
        <RouterLink to="/admin" class="text-sm text-gray-500 hover:text-gray-700 transition-colors">
          Cancel
        </RouterLink>
      </div>
    </div>

    <div v-if="loadingTrack" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 bg-gray-100 rounded-2xl h-64" />
      <div class="bg-gray-100 rounded-2xl h-48" />
    </div>

    <form v-else @submit.prevent="save">
      <div v-if="apiError" class="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
        {{ apiError }}
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left: main fields -->
        <div class="lg:col-span-2 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
            <input
              v-model="form.title"
              @input="autofillSlug"
              type="text"
              required
              placeholder="e.g. Foundations of Islam"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug <span class="text-red-500">*</span></label>
            <div class="flex gap-2">
              <input
                v-model="form.slug"
                @input="slugWasEdited = true"
                type="text"
                required
                placeholder="e.g. foundations-of-islam"
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
            <p class="text-xs text-gray-400 mt-1">URL-safe identifier. Auto-filled from title.</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Description</label>
            <textarea
              v-model="form.description"
              rows="4"
              placeholder="Short description of this track…"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
            />
          </div>
        </div>

        <!-- Right: metadata + thumbnail -->
        <div class="lg:col-span-1 lg:sticky lg:top-24 space-y-4">
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Thumbnail URL</label>
              <input
                v-model="form.thumbnail_url"
                type="url"
                placeholder="https://…"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <img
                v-if="thumbnailValid"
                :src="form.thumbnail_url"
                class="rounded-xl aspect-video object-cover w-full mt-2"
                alt="Thumbnail preview"
              />
              <div v-else class="mt-2 rounded-xl aspect-video bg-gray-50 border border-gray-100 flex items-center justify-center">
                <span class="text-xs text-gray-300">Preview</span>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Display Order</label>
              <input
                v-model.number="form.order"
                type="number"
                min="0"
                class="w-32 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
          </div>

          <!-- SEO -->
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="m21 21-4.35-4.35"/></svg>
                Search & Social (SEO)
              </h3>
            </div>
            <p class="text-xs text-gray-400 -mt-1">Optional. Left blank, Google uses the title &amp; description above.</p>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Meta Title</label>
              <input
                v-model="form.meta_title"
                type="text"
                maxlength="70"
                :placeholder="form.title || 'Defaults to track title'"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <p class="text-[11px] mt-1" :class="(form.meta_title?.length || 0) > 60 ? 'text-amber-500' : 'text-gray-400'">
                {{ form.meta_title?.length || 0 }}/70 — aim for ≤ 60
              </p>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Meta Description</label>
              <textarea
                v-model="form.meta_description"
                rows="3"
                maxlength="200"
                :placeholder="form.description || 'Defaults to track description'"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
              />
              <p class="text-[11px] mt-1" :class="(form.meta_description?.length || 0) > 160 ? 'text-amber-500' : 'text-gray-400'">
                {{ form.meta_description?.length || 0 }}/200 — aim for ≤ 160
              </p>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">Social Image URL</label>
              <input
                v-model="form.og_image"
                type="url"
                :placeholder="form.thumbnail_url || 'https://… (defaults to thumbnail)'"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <p class="text-[11px] text-gray-400 mt-1">Shown when shared on social. 1200×630 recommended.</p>
            </div>
          </div>
        </div>

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

const form = ref({ title: '', slug: '', description: '', thumbnail_url: '', order: 0, is_published: false, meta_title: '', meta_description: '', og_image: '' })
const loadingTrack = ref(false)
const saving = ref(false)
const apiError = ref('')
let slugWasEdited = false

const thumbnailValid = computed(() => form.value.thumbnail_url?.startsWith('http'))

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (!slugWasEdited) {
    form.value.slug = slugify(form.value.title)
  }
}

function regenerateSlug() {
  form.value.slug = slugify(form.value.title)
  slugWasEdited = false
}

async function save() {
  apiError.value = ''
  saving.value = true
  try {
    if (isEdit.value) {
      await adminApi.updateTrack(route.params.slug, { ...form.value })
    } else {
      await adminApi.createTrack({ ...form.value })
    }
    router.push({ name: 'admin' })
  } catch (e) {
    const data = e.response?.data
    apiError.value = typeof data === 'object'
      ? Object.values(data).flat().join(' ')
      : 'Could not save track.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (!isEdit.value) return
  loadingTrack.value = true
  try {
    const data = await adminApi.getTrack(route.params.slug)
    form.value = {
      title: data.title,
      slug: data.slug,
      description: data.description || '',
      thumbnail_url: data.thumbnail_url || '',
      order: data.order ?? 0,
      is_published: data.is_published,
      meta_title: data.meta_title || '',
      meta_description: data.meta_description || '',
      og_image: data.og_image || '',
    }
    slugWasEdited = true
  } finally {
    loadingTrack.value = false
  }
})
</script>
