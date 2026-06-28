<template>
  <div class="space-y-7" :dir="dir">
    <div v-for="block in blocks" :key="block.order">

      <!-- Text -->
      <p v-if="block.type === 'text'" class="text-gray-700 leading-relaxed text-[1.05rem]">
        {{ block.body.text }}
      </p>

      <!-- Verse -->
      <div
        v-else-if="block.type === 'verse'"
        class="bg-emerald-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-emerald-500 rounded-r-2xl rtl:rounded-r-none rtl:rounded-l-2xl px-4 py-4 sm:px-6 sm:py-5"
      >
        <p class="text-2xl text-right arabic-text text-gray-900 leading-loose mb-3 font-medium">
          {{ block.body.arabic }}
        </p>
        <p class="text-gray-600 italic text-sm mb-2">"{{ block.body.translation }}"</p>
        <p class="text-xs text-emerald-700 font-medium">
          {{ t('lesson.surah') }} {{ block.body.surah }}, {{ t('lesson.ayah') }} {{ block.body.ayah }}
        </p>
      </div>

      <!-- Hadith -->
      <div
        v-else-if="block.type === 'hadith'"
        class="bg-amber-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-amber-400 rounded-r-2xl rtl:rounded-r-none rtl:rounded-l-2xl px-4 py-4 sm:px-6 sm:py-5"
      >
        <p class="text-gray-700 italic mb-3 leading-relaxed">"{{ block.body.text }}"</p>
        <p class="text-xs text-amber-700 font-medium">— {{ block.body.source }}</p>
        <p v-if="block.body.narrator" class="text-xs text-amber-600 mt-0.5">
          {{ t('lesson.narratedBy') }} {{ block.body.narrator }}
        </p>
      </div>

      <!-- Image -->
      <figure v-else-if="block.type === 'image'" class="rounded-2xl overflow-hidden">
        <img :src="block.body.url" :alt="block.body.caption || ''" class="w-full object-cover" />
        <figcaption v-if="block.body.caption" class="text-xs text-center text-gray-400 mt-2 px-2">
          {{ block.body.caption }}
        </figcaption>
      </figure>

      <!-- Video -->
      <div v-else-if="block.type === 'video'" class="rounded-2xl overflow-hidden bg-gray-900">
        <div v-if="youtubeId(block.body.url)" class="aspect-video">
          <iframe
            :src="`https://www.youtube.com/embed/${youtubeId(block.body.url)}`"
            class="w-full h-full"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          />
        </div>
        <video v-else controls class="w-full aspect-video">
          <source :src="block.body.url" />
        </video>
        <p v-if="block.body.caption" class="text-xs text-center text-gray-400 py-2 px-4">
          {{ block.body.caption }}
        </p>
      </div>

      <!-- Quiz -->
      <div v-else-if="block.type === 'quiz'" class="border border-gray-200 rounded-2xl overflow-hidden">
        <div class="bg-gray-50 px-5 py-4 border-b border-gray-200">
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">{{ t('lesson.quickCheck') }}</p>
          <p class="font-medium text-gray-900">{{ block.body.question }}</p>
        </div>
        <div class="p-4 space-y-2">
          <button
            v-for="(option, idx) in block.body.options"
            :key="idx"
            :disabled="quizSubmitted[block.order]"
            @click="submitQuiz(block.order, idx, block.body.correct)"
            class="w-full text-start px-4 py-3 rounded-xl border text-sm transition-all"
            :class="quizOptionClass(block.order, idx, block.body.correct)"
          >
            <span class="font-medium me-2">{{ ['A', 'B', 'C', 'D'][idx] }}.</span>
            {{ option }}
          </button>
        </div>
        <div
          v-if="quizSubmitted[block.order] && block.body.explanation"
          class="px-5 py-3 bg-blue-50 border-t border-blue-100 text-sm text-blue-800"
        >
          <span class="font-semibold">{{ t('lesson.explanation') }}: </span>{{ block.body.explanation }}
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useI18n } from 'vue-i18n'

defineProps({
  blocks: { type: Array, default: () => [] },
  dir: { type: String, default: 'ltr' },
})
const emit = defineEmits(['quiz-answer'])

const { t } = useI18n()

const quizSelected = reactive({})
const quizSubmitted = reactive({})

function youtubeId(url) {
  if (!url) return null
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/)
  return match ? match[1] : null
}

function submitQuiz(blockOrder, selectedIdx, correctIdx) {
  quizSelected[blockOrder] = selectedIdx
  quizSubmitted[blockOrder] = true
  emit('quiz-answer', { blockOrder, selectedIndex: selectedIdx, correctIndex: correctIdx })
}

function quizOptionClass(blockOrder, idx, correctIdx) {
  if (!quizSubmitted[blockOrder]) {
    return 'border-gray-200 hover:border-emerald-300 hover:bg-emerald-50 text-gray-700 cursor-pointer'
  }
  if (idx === correctIdx) return 'border-emerald-500 bg-emerald-50 text-emerald-800 cursor-default'
  if (idx === quizSelected[blockOrder]) return 'border-red-400 bg-red-50 text-red-700 cursor-default'
  return 'border-gray-100 text-gray-400 cursor-default'
}
</script>
