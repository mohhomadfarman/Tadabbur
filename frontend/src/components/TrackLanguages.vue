<template>
  <div v-if="languages?.length" class="flex flex-wrap items-center gap-1.5" :title="title">
    <svg class="w-3.5 h-3.5 text-emerald-600 shrink-0" fill="none" stroke="currentColor" stroke-width="1.75" viewBox="0 0 24 24">
      <path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>
    </svg>
    <span
      v-for="l in shown"
      :key="l.code"
      :dir="l.rtl ? 'rtl' : 'ltr'"
      class="text-[10px] leading-none font-medium bg-emerald-50 text-emerald-700 border border-emerald-100 px-1.5 py-1 rounded-full"
    >
      {{ l.native_name || l.name }}
    </span>
    <span v-if="extra > 0" class="text-[10px] text-gray-400">+{{ extra }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  languages: { type: Array, default: () => [] },
  max: { type: Number, default: 3 },
  title: { type: String, default: '' },
})

const shown = computed(() => props.languages.slice(0, props.max))
const extra = computed(() => Math.max(0, props.languages.length - props.max))
</script>
