<template>
  <div>
    <!-- Hero -->
    <section class="bg-gradient-to-br from-emerald-900 to-emerald-700 text-white py-24 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <p class="arabic-text text-3xl mb-4 text-emerald-200">
          وَقُل رَّبِّ زِدْنِي عِلْمًا
        </p>
        <p class="text-emerald-300 text-sm mb-8 italic">
          {{ t('home.verseTranslation') }}
        </p>
        <h1 class="text-4xl sm:text-5xl font-bold mb-6 leading-tight">
          {{ t('home.headline') }}
        </h1>
        <p class="text-emerald-100 text-lg mb-10 max-w-2xl mx-auto">
          {{ t('home.subheadline') }}
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <RouterLink
            to="/learn"
            class="bg-white text-emerald-800 hover:bg-emerald-50 px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            {{ t('home.ctaLearn') }}
          </RouterLink>
          <RouterLink
            v-if="!auth.isLoggedIn"
            to="/register"
            class="border border-emerald-400 hover:bg-emerald-800 text-white px-8 py-3 rounded-lg font-semibold transition-colors"
          >
            {{ t('home.ctaRegister') }}
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-20 px-4 bg-gray-50">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          {{ t('home.featuresTitle') }}
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div class="text-3xl mb-4">📚</div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ t('home.feature1Title') }}</h3>
            <p class="text-gray-600 text-sm">{{ t('home.feature1Desc') }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div class="text-3xl mb-4">🕌</div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ t('home.feature2Title') }}</h3>
            <p class="text-gray-600 text-sm">{{ t('home.feature2Desc') }}</p>
          </div>
          <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div class="text-3xl mb-4">🌍</div>
            <h3 class="font-semibold text-gray-900 mb-2">{{ t('home.feature3Title') }}</h3>
            <p class="text-gray-600 text-sm">{{ t('home.feature3Desc') }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const auth = useAuthStore()
</script>
