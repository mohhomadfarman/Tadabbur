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
        <span v-if="saved" class="text-sm text-emerald-600 font-medium flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          Saved
        </span>
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

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Category</label>
              <select
                v-model="form.category_slug"
                @change="form.level_slug = ''"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              >
                <option value="">No category</option>
                <option v-for="c in categories" :key="c.slug" :value="c.slug">{{ c.title }}</option>
              </select>
            </div>

            <div v-if="selectedCategory">
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Level</label>
              <select
                v-model="form.level_slug"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              >
                <option value="">No level</option>
                <option v-for="l in selectedCategory.levels" :key="l.slug" :value="l.slug">{{ l.name }}</option>
              </select>
            </div>
          </div>

          <!-- Audience -->
          <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
            <p class="text-sm font-medium text-gray-700 mb-1">Who can see this track</p>
            <p class="text-xs text-gray-400 mb-3">Publish to a few testers first, then switch to "All users" once you're happy with it.</p>
            <div class="flex gap-2">
              <button type="button" @click="form.audience = 'all'"
                class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
                :class="form.audience === 'all' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
                All users
              </button>
              <button type="button" @click="form.audience = 'selected'"
                class="text-xs font-medium px-3 py-1.5 rounded-lg border transition-colors"
                :class="form.audience === 'selected' ? 'border-[#234ecc] bg-[#234ecc]/5 text-[#234ecc]' : 'border-gray-200 text-gray-500 hover:bg-gray-50'">
                Selected users
              </button>
            </div>

            <div v-if="form.audience === 'selected'" class="mt-3">
              <div v-if="form.allowed_user_ids.length" class="flex flex-wrap gap-1.5 mb-2">
                <span v-for="uid in form.allowed_user_ids" :key="uid"
                  class="inline-flex items-center gap-1.5 text-xs bg-gray-100 text-gray-700 rounded-full ps-2.5 pe-1 py-1">
                  {{ userLabel(uid) }}
                  <button @click="removeUser(uid)" class="w-4 h-4 rounded-full inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
                  </button>
                </span>
              </div>
              <div class="relative">
                <input v-model="userSearch" @input="onUserSearch" type="text"
                  placeholder="Search users by email or name…"
                  class="w-full border border-gray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
                <div v-if="userResults.length"
                  class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-xl shadow-lg max-h-56 overflow-y-auto">
                  <button v-for="u in userResults" :key="u.id" @click="addUser(u)"
                    class="w-full text-left px-4 py-2 text-sm hover:bg-gray-50 flex items-center justify-between gap-2"
                    :class="form.allowed_user_ids.includes(u.id) ? 'opacity-50 pointer-events-none' : ''">
                    <span class="truncate">
                      <span class="text-gray-800">{{ u.full_name || u.username }}</span>
                      <span class="text-gray-400 ms-1.5">{{ u.email }}</span>
                    </span>
                  </button>
                </div>
              </div>
              <p class="text-[11px] text-gray-400 mt-1.5">Only these users will see this track while it's published.</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const form = ref({
  title: '', slug: '', description: '', thumbnail_url: '', order: 0, is_published: false,
  category_slug: '', level_slug: '', audience: 'all', allowed_user_ids: [],
  meta_title: '', meta_description: '', og_image: '',
})
const loadingTrack = ref(false)
const saving = ref(false)
const saved = ref(false)
const apiError = ref('')
let slugWasEdited = false

const categories = ref([])
const selectedCategory = computed(() => categories.value.find(c => c.slug === form.value.category_slug) || null)

const userSearch = ref('')
const userResults = ref([])
const userCache = reactive({})
let userSearchTimer = null

function userLabel(uid) {
  const u = userCache[uid]
  return u ? (u.email || u.username || uid) : '…'
}

function onUserSearch() {
  clearTimeout(userSearchTimer)
  const q = userSearch.value.trim()
  if (!q) { userResults.value = []; return }
  userSearchTimer = setTimeout(async () => {
    try {
      const users = await adminApi.searchFeatureUsers(q)
      users.forEach(u => { userCache[u.id] = u })
      userResults.value = users
    } catch { userResults.value = [] }
  }, 250)
}

function addUser(u) {
  if (!form.value.allowed_user_ids.includes(u.id)) form.value.allowed_user_ids.push(u.id)
  userCache[u.id] = u
  userSearch.value = ''
  userResults.value = []
}
function removeUser(uid) {
  form.value.allowed_user_ids = form.value.allowed_user_ids.filter(id => id !== uid)
}

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
  saved.value = false
  saving.value = true
  try {
    if (isEdit.value) {
      await adminApi.updateTrack(route.params.slug, { ...form.value })
      saved.value = true
      setTimeout(() => { saved.value = false }, 2500)
    } else {
      const created = await adminApi.createTrack({ ...form.value })
      slugWasEdited = true
      saved.value = true
      setTimeout(() => { saved.value = false }, 2500)
      if (created?.slug) router.replace({ name: 'admin-track-edit', params: { slug: created.slug } })
    }
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
  adminApi.listCategories().then(list => { categories.value = list }).catch(() => {})

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
      category_slug: data.category?.slug || '',
      level_slug: data.level?.slug || '',
      audience: data.audience || 'all',
      allowed_user_ids: [...(data.allowed_user_ids || [])],
      meta_title: data.meta_title || '',
      meta_description: data.meta_description || '',
      og_image: data.og_image || '',
    }
    slugWasEdited = true
    if (form.value.allowed_user_ids.length) {
      try {
        const users = await adminApi.resolveFeatureUsers(form.value.allowed_user_ids)
        users.forEach(u => { userCache[u.id] = u })
      } catch { /* labels just show as … */ }
    }
  } finally {
    loadingTrack.value = false
  }
})
</script>
