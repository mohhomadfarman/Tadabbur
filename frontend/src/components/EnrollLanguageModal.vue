<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="$emit('cancel')">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
      <h3 class="font-bold text-gray-900 text-lg mb-1">{{ t('enroll.title') }}</h3>
      <p class="text-sm text-gray-500 mb-5">{{ t('enroll.subtitle', { track: trackTitle }) }}</p>

      <div class="space-y-2 max-h-72 overflow-y-auto -mx-1 px-1">
        <!-- Original -->
        <button
          type="button"
          @click="selected = ''"
          class="w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl border text-left transition-colors"
          :class="selected === '' ? 'border-emerald-500 bg-emerald-50' : 'border-gray-200 hover:border-gray-300'"
        >
          <span>
            <span class="block text-sm font-semibold text-gray-800">{{ t('enroll.original') }}</span>
            <span class="block text-xs text-gray-400">{{ t('enroll.originalHint') }}</span>
          </span>
          <span v-if="selected === ''" class="text-emerald-600">✓</span>
        </button>

        <!-- Languages -->
        <button
          v-for="lang in languages"
          :key="lang.code"
          type="button"
          @click="selected = lang.code"
          class="w-full flex items-center justify-between gap-3 px-4 py-3 rounded-xl border text-left transition-colors"
          :class="selected === lang.code ? 'border-emerald-500 bg-emerald-50' : 'border-gray-200 hover:border-gray-300'"
        >
          <span>
            <span class="block text-sm font-semibold text-gray-800">{{ lang.name }}</span>
            <span v-if="lang.native_name" class="block text-xs text-gray-400" :dir="lang.rtl ? 'rtl' : 'ltr'">{{ lang.native_name }}</span>
          </span>
          <span v-if="selected === lang.code" class="text-emerald-600">✓</span>
        </button>
      </div>

      <div class="flex gap-3 mt-6">
        <button @click="$emit('cancel')" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">
          {{ t('enroll.cancel') }}
        </button>
        <button :disabled="enrolling" @click="$emit('confirm', selected)"
          class="flex-1 px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
          {{ enrolling ? t('enroll.enrolling') : t('enroll.confirm') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

defineProps({
  trackTitle: { type: String, default: '' },
  languages: { type: Array, default: () => [] },
  enrolling: { type: Boolean, default: false },
})
defineEmits(['confirm', 'cancel'])

const { t } = useI18n()
const selected = ref('')
</script>
