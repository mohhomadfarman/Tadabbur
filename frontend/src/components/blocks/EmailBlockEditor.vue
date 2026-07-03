<template>
  <div>
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-sm font-semibold text-gray-700">Content</h2>
      <span class="text-xs text-gray-400">{{ blocks.length }} block{{ blocks.length !== 1 ? 's' : '' }}</span>
    </div>

    <!-- Block list — draggable reorder via the handle icon, up/down buttons kept as a fallback -->
    <VueDraggable v-model="blocks" handle=".drag-handle" tag="div" class="space-y-3" :animation="150">
      <template v-for="(block, idx) in blocks" :key="block.__key">
        <div class="border rounded-2xl overflow-hidden shadow-sm" :class="EMAIL_BLOCK_BORDER_CLASSES[block.type]">
          <!-- Block header -->
          <div class="flex items-center gap-3 px-4 py-2.5 border-b" :class="EMAIL_BLOCK_HEADER_CLASSES[block.type]">
            <span class="drag-handle cursor-grab active:cursor-grabbing text-gray-300 hover:text-gray-500" title="Drag to reorder">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M7 4a1 1 0 100 2 1 1 0 000-2zM7 9a1 1 0 100 2 1 1 0 000-2zM7 14a1 1 0 100 2 1 1 0 000-2zM13 4a1 1 0 100 2 1 1 0 000-2zM13 9a1 1 0 100 2 1 1 0 000-2zM13 14a1 1 0 100 2 1 1 0 000-2z"/></svg>
            </span>
            <span class="text-[11px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full" :class="EMAIL_BLOCK_BADGE_CLASSES[block.type]">
              {{ block.type }}
            </span>
            <span class="text-xs text-gray-400">#{{ idx + 1 }}</span>
            <div class="flex-1" />
            <div class="flex items-center gap-1">
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
            <div class="bg-white px-5 py-4">
              <textarea v-model="block.body.text" placeholder="Start writing your paragraph…" rows="4"
                class="w-full text-gray-700 leading-relaxed text-[1.05rem] resize-y bg-transparent border-0 focus:outline-none focus:ring-0 placeholder:text-gray-300" />
            </div>
          </template>

          <!-- HEADER -->
          <template v-else-if="block.type === 'header'">
            <div class="bg-white px-5 py-4 space-y-2">
              <input v-model="block.body.text" placeholder="Heading text…"
                class="w-full font-semibold text-lg text-gray-900 bg-transparent border-0 focus:outline-none placeholder:text-gray-300" />
              <div class="flex items-center gap-2 text-xs">
                <span class="text-gray-400">Size:</span>
                <select v-model="block.body.level" class="border border-gray-200 rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
                  <option value="h1">Large (H1)</option>
                  <option value="h2">Regular (H2)</option>
                </select>
              </div>
            </div>
          </template>

          <!-- IMAGE -->
          <template v-else-if="block.type === 'image'">
            <div class="bg-white p-4 space-y-3">
              <div v-if="block.body.url" class="rounded-xl overflow-hidden border border-gray-100">
                <img :src="block.body.url" :alt="block.body.alt || ''" class="w-full object-cover max-h-72" />
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
              <input v-model="block.body.alt" placeholder="Alt text (optional)"
                class="w-full text-xs text-gray-500 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300" />
              <input v-model="block.body.link" type="url" placeholder="Link URL (optional — makes the image clickable)"
                class="w-full text-xs text-gray-500 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300" />
            </div>
          </template>

          <!-- BUTTON -->
          <template v-else-if="block.type === 'button'">
            <div class="bg-white px-5 py-4 space-y-2">
              <input v-model="block.body.label" placeholder="Button label (e.g. Verify email)"
                class="w-full font-medium text-gray-900 bg-transparent border-0 focus:outline-none placeholder:text-gray-300" />
              <input v-model="block.body.url" placeholder="URL (or a merge tag like {{verify_url}})"
                class="w-full text-sm text-[#234ecc] font-mono bg-transparent border-0 border-t border-gray-100 pt-2 focus:outline-none placeholder:text-gray-300 placeholder:font-sans" />
            </div>
          </template>

          <!-- DIVIDER -->
          <template v-else-if="block.type === 'divider'">
            <div class="bg-white px-5 py-5">
              <hr class="border-gray-200" />
            </div>
          </template>

          <!-- SPACER -->
          <template v-else-if="block.type === 'spacer'">
            <div class="bg-white px-5 py-4 flex items-center gap-2 text-xs">
              <span class="text-gray-400">Height (px):</span>
              <input v-model.number="block.body.height" type="number" min="0" max="200"
                class="w-20 border border-gray-200 rounded-lg px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
            </div>
          </template>
        </div>
      </template>
    </VueDraggable>

    <div v-if="blocks.length === 0" class="text-center text-gray-400 text-sm py-10 border-2 border-dashed border-gray-200 rounded-2xl">
      No content yet — add your first block below.
    </div>

    <!-- Add block pills -->
    <div class="flex flex-wrap gap-2 pt-3">
      <button v-for="type in EMAIL_BLOCK_TYPES" :key="type.value" type="button" @click="addBlock(type.value)"
        class="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-200 hover:border-[#234ecc]/30 hover:bg-[#234ecc]/5 hover:text-[#234ecc] text-xs font-medium text-gray-500 transition-colors">
        <svg class="w-3.5 h-3.5 shrink-0" :class="type.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="type.icon" /></svg>
        + {{ type.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { adminApi } from '@/api/admin'
import {
  EMAIL_BLOCK_TYPES, EMAIL_BLOCK_DEFAULTS, EMAIL_BLOCK_BADGE_CLASSES,
  EMAIL_BLOCK_HEADER_CLASSES, EMAIL_BLOCK_BORDER_CLASSES,
} from './emailBlockKit'

const props = defineProps({
  modelValue: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue', 'error'])

// Operate on the bound array in place (parent shares the same reference). Mutating
// array contents is reactive and does not trip Vue's prop-reassignment warning.
// VueDraggable needs a stable :key per item — since blocks don't carry a
// persistent id, assign one locally (not sent to the backend).
let keySeq = 0
for (const b of props.modelValue) {
  if (!b.__key) b.__key = ++keySeq
}
const blocks = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const imageUploading = reactive({})
const imageInputRefs = ref([])

function emitUpdate() {
  emit('update:modelValue', blocks.value)
}

function addBlock(type) {
  blocks.value.push({ type, body: { ...EMAIL_BLOCK_DEFAULTS[type] }, __key: ++keySeq })
  emitUpdate()
}

function removeBlock(idx) {
  blocks.value.splice(idx, 1)
  emitUpdate()
}

function moveBlock(idx, dir) {
  const target = idx + dir
  if (target < 0 || target >= blocks.value.length) return
  const tmp = blocks.value[idx]
  blocks.value[idx] = blocks.value[target]
  blocks.value[target] = tmp
  emitUpdate()
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
