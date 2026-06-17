<template>
  <header class="sticky top-0 z-50 bg-white border-b border-gray-100 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2 shrink-0">
          <span class="text-emerald-700 font-bold text-xl tracking-tight">Tadabbur</span>
          <span class="text-gray-400 text-lg arabic-text">تدبّر</span>
        </RouterLink>

        <!-- Nav links (desktop) -->
        <nav class="hidden md:flex items-center gap-6">
          <RouterLink
            to="/learn"
            class="text-gray-600 hover:text-emerald-700 font-medium transition-colors"
            active-class="text-emerald-700"
          >
            {{ t('nav.learn') }}
          </RouterLink>
        </nav>

        <!-- Right side actions -->
        <div class="flex items-center gap-3">

          <!-- Language toggle -->
          <button
            @click="toggleLocale"
            class="text-xs font-medium border border-gray-200 rounded-lg px-2.5 py-1.5 text-gray-500 hover:text-emerald-700 hover:border-emerald-300 transition-colors"
            :title="locale === 'en' ? 'Switch to Arabic' : 'Switch to English'"
          >
            {{ locale === 'en' ? 'العربية' : 'English' }}
          </button>

          <!-- Auth actions -->
          <template v-if="auth.isLoggedIn">
            <RouterLink
              to="/dashboard"
              class="text-sm text-gray-600 hover:text-emerald-700 font-medium transition-colors"
            >
              {{ t('nav.dashboard') }}
            </RouterLink>
            <RouterLink
              v-if="auth.isAuthor"
              to="/admin"
              class="text-sm text-gray-600 hover:text-emerald-700 font-medium transition-colors"
              active-class="text-emerald-700"
            >
              {{ t('nav.admin') }}
            </RouterLink>
            <button
              @click="auth.logout(); $router.push('/')"
              class="text-sm text-gray-400 hover:text-red-600 transition-colors"
            >
              {{ t('nav.logout') }}
            </button>
          </template>
          <template v-else>
            <RouterLink
              to="/login"
              class="text-sm text-gray-600 hover:text-emerald-700 font-medium transition-colors"
            >
              {{ t('nav.login') }}
            </RouterLink>
            <RouterLink
              to="/register"
              class="text-sm bg-emerald-700 hover:bg-emerald-800 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              {{ t('nav.getStarted') }}
            </RouterLink>
          </template>
        </div>

      </div>
    </div>
  </header>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { setLocale } from '@/i18n'

const auth = useAuthStore()
const { t, locale } = useI18n({ useScope: 'global' })

function toggleLocale() {
  setLocale(locale.value === 'en' ? 'ar' : 'en')
}
</script>
