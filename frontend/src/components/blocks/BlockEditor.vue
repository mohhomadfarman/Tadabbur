<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-sm font-semibold text-gray-700">Content</h2>
      <span class="text-xs text-gray-400">{{ blocks.length }} block{{ blocks.length !== 1 ? 's' : '' }}</span>
    </div>

    <!-- Block list -->
    <div class="space-y-3">
      <div v-if="blocks.length === 0" class="text-center text-gray-400 text-sm py-10 border-2 border-dashed border-gray-200 rounded-2xl">
        No content yet — add your first block below.
      </div>

      <div
        v-for="(block, idx) in blocks"
        :key="idx"
        class="border rounded-2xl overflow-hidden shadow-sm"
        :class="BLOCK_BORDER_CLASSES[block.type]"
      >
        <!-- Block header -->
        <div class="flex items-center gap-3 px-4 py-2.5 border-b" :class="BLOCK_HEADER_CLASSES[block.type]">
          <span class="text-[11px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full" :class="BLOCK_BADGE_CLASSES[block.type]">
            {{ block.type }}
          </span>
          <span class="text-xs text-gray-400">#{{ idx + 1 }}</span>
          <div class="flex-1" />
          <div v-if="allowStructure" class="flex items-center gap-1">
            <button type="button" @click="moveBlock(idx, -1)" :disabled="idx === 0"
              class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-white/60 disabled:opacity-30 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/></svg>
            </button>
            <button type="button" @click="moveBlock(idx, 1)" :disabled="idx === blocks.length - 1"
              class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-white/60 disabled:opacity-30 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
            <button type="button" @click="removeBlock(idx)"
              class="w-7 h-7 flex items-center justify-center rounded-lg text-red-300 hover:text-red-500 hover:bg-red-50 transition-colors ml-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>
        </div>

        <!-- TEXT -->
        <template v-if="block.type === 'text'">
          <div class="bg-white px-5 py-4 space-y-2">
            <textarea v-model="block.body.text" placeholder="Start writing your paragraph…" rows="5" :dir="dir"
              class="w-full text-gray-700 leading-relaxed text-[1.05rem] resize-y bg-transparent border-0 focus:outline-none focus:ring-0 placeholder:text-gray-300" />
            <div class="flex items-center gap-2 text-xs pt-2 border-t border-gray-100">
              <span class="text-gray-400">Source:</span>
              <input v-model="block.body.source" placeholder="Optional reference (e.g. book/page, scholar, link)…"
                class="flex-1 text-gray-500 bg-transparent border-0 focus:outline-none placeholder:text-gray-300" />
            </div>
          </div>
        </template>

        <!-- VERSE -->
        <template v-else-if="block.type === 'verse'">
          <div class="bg-emerald-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-emerald-500 px-6 py-5 space-y-3">
            <textarea v-model="block.body.arabic" rows="3" dir="rtl" placeholder="أدخل الآية الكريمة بالتشكيل…"
              class="w-full text-2xl text-right arabic-text text-gray-900 leading-loose bg-transparent border-0 border-b border-emerald-200 focus:outline-none focus:border-emerald-400 resize-none pb-2 placeholder:text-emerald-200" />
            <textarea v-model="block.body.translation" rows="2" :dir="dir" placeholder="Enter English translation…"
              class="w-full text-gray-600 italic text-sm bg-transparent border-0 border-b border-emerald-200 focus:outline-none focus:border-emerald-400 resize-none pb-2 placeholder:text-emerald-300" />
            <div class="flex items-center gap-2 text-xs text-emerald-700 font-medium flex-wrap">
              <span class="text-emerald-400">Surah</span>
              <input v-model="block.body.surah" placeholder="Name"
                class="flex-1 min-w-[6rem] bg-transparent border-0 focus:outline-none text-emerald-700 placeholder:text-emerald-300 font-medium" />
              <span class="text-emerald-300 mx-1">·</span>
              <span class="text-emerald-400">Ayah</span>
              <input v-model.number="block.body.ayah" type="number" placeholder="0"
                class="w-16 text-right bg-transparent border-0 focus:outline-none text-emerald-700 placeholder:text-emerald-300" />
            </div>
          </div>
        </template>

        <!-- HADITH -->
        <template v-else-if="block.type === 'hadith'">
          <div class="bg-amber-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-amber-400 px-6 py-5 space-y-3">
            <textarea v-model="block.body.text" rows="4" :dir="dir" placeholder="Enter hadith text…"
              class="w-full text-gray-700 italic leading-relaxed bg-transparent border-0 border-b border-amber-200 focus:outline-none focus:border-amber-400 resize-y pb-2 placeholder:text-amber-200" />
            <div class="flex items-center gap-2 text-xs">
              <span class="text-amber-400 font-medium">—</span>
              <input v-model="block.body.source" placeholder="Source (e.g. Sahih Bukhari 1)"
                class="flex-1 text-amber-700 font-medium bg-transparent border-0 focus:outline-none placeholder:text-amber-300" />
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="text-amber-300">Narrated by:</span>
              <input v-model="block.body.narrator" placeholder="Narrator (optional)"
                class="flex-1 text-amber-600 bg-transparent border-0 focus:outline-none placeholder:text-amber-300" />
            </div>
          </div>
        </template>

        <!-- IMAGE -->
        <template v-else-if="block.type === 'image'">
          <div class="bg-white p-4 space-y-3">
            <div v-if="block.body.url" class="rounded-xl overflow-hidden border border-gray-100">
              <img :src="block.body.url" :alt="block.body.caption || ''" class="w-full object-cover max-h-72" />
            </div>
            <div v-else class="rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 h-36 flex flex-col items-center justify-center gap-2 text-gray-400 text-sm">
              <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <span>Paste a URL or upload an image</span>
            </div>
            <div class="flex gap-2">
              <input v-model="block.body.url" type="url" placeholder="Paste image URL…"
                class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
              <button type="button" @click="imageInputRefs[idx]?.click()" :disabled="imageUploading[idx]"
                class="shrink-0 px-3 py-2 text-xs font-medium border border-[#234ecc]/30 text-[#234ecc] rounded-xl hover:bg-[#234ecc]/5 disabled:opacity-60 transition-colors">
                {{ imageUploading[idx] ? 'Uploading…' : 'Upload' }}
              </button>
              <input :ref="el => imageInputRefs[idx] = el" type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="hidden" @change="handleImageUpload(idx, $event)" />
            </div>
            <input v-model="block.body.caption" placeholder="Caption (optional)"
              class="w-full text-xs text-center text-gray-400 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300" />
          </div>
        </template>

        <!-- VIDEO -->
        <template v-else-if="block.type === 'video'">
          <div class="bg-white p-4 space-y-3">
            <div v-if="youtubeId(block.body.url)" class="rounded-xl overflow-hidden bg-gray-900 aspect-video">
              <iframe :src="`https://www.youtube.com/embed/${youtubeId(block.body.url)}`" class="w-full h-full" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />
            </div>
            <div v-else-if="block.body.url" class="rounded-xl overflow-hidden bg-gray-900">
              <video controls class="w-full aspect-video"><source :src="block.body.url" /></video>
            </div>
            <div v-else class="rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 h-36 flex flex-col items-center justify-center gap-2 text-gray-400 text-sm">
              <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
              <span>Paste a YouTube or video URL below to preview</span>
            </div>
            <input v-model="block.body.url" type="url" placeholder="YouTube or video URL…"
              class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            <input v-model="block.body.caption" placeholder="Caption (optional)"
              class="w-full text-xs text-center text-gray-400 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300" />
          </div>
        </template>

        <!-- QUIZ -->
        <template v-else-if="block.type === 'quiz'">
          <div class="bg-gray-50 px-5 py-4 border-b border-gray-200">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Quick Check</p>
            <input v-model="block.body.question" :dir="dir" placeholder="Enter your question…"
              class="w-full font-medium text-gray-900 bg-transparent border-0 focus:outline-none text-base placeholder:text-gray-300" />
          </div>
          <div class="bg-white px-4 py-4 space-y-2">
            <div v-for="(opt, oi) in (block.body.options || ['', '', '', ''])" :key="oi" class="flex items-center gap-2.5">
              <input type="radio" :name="`quiz-correct-${idx}`" :value="oi" v-model="block.body.correct" class="accent-[#234ecc] shrink-0" title="Mark as correct answer" />
              <input :value="opt" @input="setOption(block, oi, $event.target.value)" :placeholder="`Option ${['A', 'B', 'C', 'D'][oi]}`"
                class="flex-1 px-3 py-2.5 rounded-xl border text-sm transition-all focus:outline-none focus:ring-1"
                :class="block.body.correct === oi ? 'border-emerald-500 bg-emerald-50 text-emerald-800 focus:ring-emerald-300' : 'border-gray-200 text-gray-700 hover:border-gray-300 focus:ring-[#234ecc]/30 placeholder:text-gray-300'" />
            </div>
            <p class="text-xs text-gray-400 mt-1 ms-6">Click the radio to mark the correct answer.</p>
          </div>
          <div class="bg-white px-4 pb-4">
            <textarea v-model="block.body.explanation" rows="2" :dir="dir" placeholder="Explanation shown after answering (optional)…"
              class="w-full text-sm text-blue-800 bg-blue-50 border border-blue-100 rounded-xl px-3 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-300 placeholder:text-blue-300" />
          </div>
        </template>

      </div>
    </div>

    <!-- Add block pills -->
    <div v-if="allowStructure" class="flex flex-wrap gap-2 pt-2">
      <button v-for="type in BLOCK_TYPES" :key="type.value" type="button" @click="addBlock(type.value)"
        class="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-200 hover:border-[#234ecc]/30 hover:bg-[#234ecc]/5 hover:text-[#234ecc] text-xs font-medium text-gray-500 transition-colors">
        <svg class="w-3.5 h-3.5 shrink-0" :class="type.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="type.icon" /></svg>
        + {{ type.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { adminApi } from '@/api/admin'
import {
  BLOCK_TYPES, BLOCK_DEFAULTS, BLOCK_BADGE_CLASSES,
  BLOCK_HEADER_CLASSES, BLOCK_BORDER_CLASSES, youtubeId,
} from './blockKit'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
  allowStructure: { type: Boolean, default: true },  // false = lock block add/remove/reorder
  dir: { type: String, default: 'ltr' },
})
const emit = defineEmits(['update:modelValue', 'error'])

// Operate on the bound array in place (parent shares the same reference). Mutating
// array contents is reactive and does not trip Vue's prop-reassignment warning.
const blocks = computed(() => props.modelValue)

const imageUploading = reactive({})
const imageInputRefs = ref([])

function addBlock(type) {
  blocks.value.push({ type, body: { ...BLOCK_DEFAULTS[type] } })
  emit('update:modelValue', blocks.value)
}

function removeBlock(idx) {
  blocks.value.splice(idx, 1)
  emit('update:modelValue', blocks.value)
}

function moveBlock(idx, dir) {
  const target = idx + dir
  if (target < 0 || target >= blocks.value.length) return
  const tmp = blocks.value[idx]
  blocks.value[idx] = blocks.value[target]
  blocks.value[target] = tmp
  emit('update:modelValue', blocks.value)
}

function setOption(block, oi, val) {
  if (!block.body.options) block.body.options = ['', '', '', '']
  block.body.options[oi] = val
}

async function handleImageUpload(idx, event) {
  const file = event.target.files?.[0]
  if (!file) return
  imageUploading[idx] = true
  try {
    const { upload_url, public_url } = await adminApi.getUploadUrl(file.name, file.type, 'image')
    const res = await fetch(upload_url, { method: 'PUT', body: file, headers: { 'Content-Type': file.type } })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    blocks.value[idx].body.url = public_url
  } catch {
    emit('error', 'Image upload failed. Please try again or paste a URL.')
  } finally {
    imageUploading[idx] = false
    if (imageInputRefs.value[idx]) imageInputRefs.value[idx].value = ''
  }
}
</script>
