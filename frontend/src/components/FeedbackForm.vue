<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/60 flex items-center justify-center z-[60] p-4 backdrop-blur-sm"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full overflow-hidden">
      <!-- Header -->
      <div class="px-6 pt-6 pb-2 text-center">
        <div class="mx-auto w-12 h-12 rounded-full bg-[#234ecc]/10 flex items-center justify-center mb-3">
          <svg class="w-6 h-6 text-[#234ecc]" fill="none" stroke="currentColor" stroke-width="1.75" viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>
        </div>
        <h2 class="text-lg font-bold text-gray-900">{{ t('feedback.trackCompleted') }}</h2>
        <p class="text-sm text-gray-500 mt-1">{{ t('feedback.leaveReview') }}</p>
      </div>

      <!-- Body -->
      <div class="px-6 py-4">
        <p class="text-xs font-medium text-gray-500 mb-2 text-center">{{ t('feedback.rating') }}</p>
        <div class="flex justify-center gap-1.5 mb-4">
          <button
            v-for="n in 5" :key="n"
            type="button"
            @click="rating = n"
            @mouseenter="hover = n"
            @mouseleave="hover = 0"
            class="transition-transform hover:scale-110"
          >
            <svg class="w-9 h-9" :class="(hover || rating) >= n ? 'text-amber-400' : 'text-gray-200'"
              fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
            </svg>
          </button>
        </div>

        <textarea
          v-model="comment"
          :placeholder="t('feedback.commentPlaceholder')"
          rows="3"
          maxlength="2000"
          class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
        />

        <p v-if="error" class="text-sm text-red-600 mt-2">{{ error }}</p>
      </div>

      <!-- Footer -->
      <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between gap-3">
        <button @click="$emit('close')" class="text-sm text-gray-500 hover:text-gray-800 transition-colors">
          {{ t('feedback.skip') }}
        </button>
        <button
          :disabled="!rating || submitting"
          @click="submit"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
        >
          {{ submitting ? t('feedback.sending') : t('feedback.submit') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { feedbackApi } from '@/api/feedback'

const props = defineProps({
  show: { type: Boolean, default: false },
  trackSlug: { type: String, required: true },
  trackTitle: { type: String, default: '' },
})
const emit = defineEmits(['close', 'submitted'])
const { t } = useI18n()

const rating = ref(0)
const hover = ref(0)
const comment = ref('')
const submitting = ref(false)
const error = ref('')

// Reset when the dialog is (re)opened.
watch(() => props.show, (open) => {
  if (open) { rating.value = 0; hover.value = 0; comment.value = ''; error.value = ''; submitting.value = false }
})

async function submit() {
  if (!rating.value) return
  submitting.value = true
  error.value = ''
  try {
    await feedbackApi.submit(props.trackSlug, { rating: rating.value, comment: comment.value.trim() })
    emit('submitted', { rating: rating.value })
  } catch {
    error.value = t('feedback.error')
    submitting.value = false
  }
}
</script>
