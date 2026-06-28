<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">

    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Languages</h1>
      <p class="text-gray-400 text-sm mt-0.5">
        Offer AI translations of lessons. Authors generate them in the lesson editor;
        learners pick a language when they enroll.
      </p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <div v-if="loading" class="space-y-3 animate-pulse">
      <div class="bg-gray-100 rounded-2xl h-40" />
      <div class="bg-gray-100 rounded-2xl h-64" />
    </div>

    <template v-else>
      <!-- Gemini settings -->
      <section class="bg-white border border-gray-200 rounded-2xl shadow-sm mb-8">
        <div class="px-5 py-4 border-b border-gray-100">
          <h2 class="font-semibold text-gray-800">Gemini</h2>
          <p class="text-xs text-gray-400 mt-0.5">Used to generate translations. The key is stored securely and never shown again.</p>
        </div>
        <div class="px-5 py-5 grid sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Model</label>
            <input v-model="form.model" type="text" placeholder="gemini-flash-lite-latest"
              class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">
              API key
              <span v-if="hasKey" class="text-emerald-600 font-normal">
                · set ({{ keyHint }}<template v-if="keySource === 'env'"> · from env</template>)
              </span>
              <span v-else class="text-amber-600 font-normal">· not set</span>
            </label>
            <input v-model="keyInput" type="password" autocomplete="off"
              :placeholder="hasKey ? 'Enter a new key to replace it' : 'Paste your Gemini API key'"
              class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            <button v-if="hasKey && keySource === 'admin'" type="button" @click="clearKey = !clearKey"
              class="mt-1.5 text-xs" :class="clearKey ? 'text-red-600 font-semibold' : 'text-gray-400 hover:text-red-500'">
              {{ clearKey ? 'Key will be removed on save · undo' : 'Remove stored key' }}
            </button>
          </div>
          <div class="sm:col-span-2">
            <details>
              <summary class="text-xs font-medium text-gray-500 cursor-pointer select-none">Translation instructions (advanced)</summary>
              <textarea v-model="form.system_instruction" rows="6"
                class="mt-2 w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm font-mono leading-relaxed focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-y"></textarea>
              <p class="text-[11px] text-gray-400 mt-1">Guides tone and what to preserve (Arabic, ﷺ, names, Islamic terms).</p>
            </details>
          </div>
        </div>
      </section>

      <!-- Languages list -->
      <section class="bg-white border border-gray-200 rounded-2xl shadow-sm mb-8">
        <div class="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h2 class="font-semibold text-gray-800">Offered languages</h2>
            <p class="text-xs text-gray-400 mt-0.5">The <span class="font-medium">Name</span> is what Gemini translates into (e.g. “Hinglish”, “Urdu”).</p>
          </div>
          <button @click="addLanguage" type="button"
            class="inline-flex items-center gap-1.5 text-sm font-semibold text-[#234ecc] hover:text-[#1a3ba8] transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
            Add
          </button>
        </div>

        <div v-if="!languages.length" class="px-5 py-12 text-center text-sm text-gray-400">
          No languages yet. Add one to start offering translations.
        </div>

        <div v-else class="divide-y divide-gray-100">
          <div v-for="(lang, i) in languages" :key="i" class="px-5 py-4 grid grid-cols-1 sm:grid-cols-12 gap-3 items-center">
            <div class="sm:col-span-4">
              <label class="block text-[11px] font-medium text-gray-400 mb-1 sm:hidden">Name</label>
              <input v-model="lang.name" type="text" placeholder="Hinglish"
                class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div class="sm:col-span-3">
              <label class="block text-[11px] font-medium text-gray-400 mb-1 sm:hidden">Code</label>
              <input v-model="lang.code" type="text" :placeholder="slugify(lang.name) || 'code'"
                class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div class="sm:col-span-3">
              <label class="block text-[11px] font-medium text-gray-400 mb-1 sm:hidden">Native name</label>
              <input v-model="lang.native_name" type="text" placeholder="Native name (optional)"
                class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
            <div class="sm:col-span-2 flex items-center justify-between gap-3">
              <label class="inline-flex items-center gap-1.5 text-xs text-gray-500 cursor-pointer" title="Right-to-left script">
                <input v-model="lang.rtl" type="checkbox" class="rounded border-gray-300 text-[#234ecc] focus:ring-[#234ecc]/40" /> RTL
              </label>
              <label class="inline-flex items-center gap-1.5 text-xs text-gray-500 cursor-pointer" title="Show to learners">
                <input v-model="lang.enabled" type="checkbox" class="rounded border-gray-300 text-[#234ecc] focus:ring-[#234ecc]/40" /> On
              </label>
              <button @click="languages.splice(i, 1)" type="button" title="Remove"
                class="w-7 h-7 rounded-lg inline-flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors shrink-0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Save bar -->
      <div class="flex flex-wrap items-center gap-3">
        <button @click="save" :disabled="saving"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors">
          {{ saving ? 'Saving…' : 'Save changes' }}
        </button>
        <span v-if="saved" class="text-sm text-emerald-600 font-semibold">Saved ✓</span>
        <span v-if="saveError" class="text-sm text-red-600">{{ saveError }}</span>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const loading = ref(true)
const error = ref('')
const saving = ref(false)
const saved = ref(false)
const saveError = ref('')

const form = reactive({ model: '', system_instruction: '' })
const languages = ref([])
const hasKey = ref(false)
const keyHint = ref('')
const keySource = ref('none')
const keyInput = ref('')
const clearKey = ref(false)

function slugify(text) {
  return (text || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
}

function addLanguage() {
  languages.value.push({ code: '', name: '', native_name: '', rtl: false, enabled: true })
}

function applySettings(s) {
  form.model = s.model || ''
  form.system_instruction = s.system_instruction || ''
  languages.value = (s.languages || []).map(l => ({
    code: l.code || '', name: l.name || '', native_name: l.native_name || '',
    rtl: !!l.rtl, enabled: l.enabled !== false,
  }))
  hasKey.value = !!s.has_key
  keyHint.value = s.key_hint || ''
  keySource.value = s.key_source || 'none'
  keyInput.value = ''
  clearKey.value = false
}

async function save() {
  saveError.value = ''
  // Validate languages have a name; derive code if blank.
  const cleaned = languages.value
    .map(l => ({ ...l, name: (l.name || '').trim(), code: (l.code || '').trim() || slugify(l.name) }))
    .filter(l => l.name)
  if (cleaned.length !== languages.value.filter(l => (l.name || '').trim() || (l.code || '').trim()).length) {
    saveError.value = 'Every language needs a name.'
    return
  }

  const payload = {
    model: form.model.trim(),
    system_instruction: form.system_instruction,
    languages: cleaned,
  }
  if (clearKey.value) payload.clear_key = true
  else if (keyInput.value.trim()) payload.gemini_api_key = keyInput.value.trim()

  saving.value = true
  try {
    const s = await adminApi.updateTranslationSettings(payload)
    applySettings(s)
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
  } catch (e) {
    saveError.value = e?.response?.data?.languages || 'Could not save. Make sure your account has Languages access.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    applySettings(await adminApi.getTranslationSettings())
  } catch {
    error.value = 'Could not load translation settings. Make sure your account has Languages access.'
  } finally {
    loading.value = false
  }
})
</script>
