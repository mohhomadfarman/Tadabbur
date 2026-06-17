<template>
  <!-- Fixed wrapper — always full-width, transparent background -->
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-400 ease-out "
    :class="isScrolled ? 'py-3 px-4 sm:px-6' : 'py-4 px-4 sm:px-6'"
  >
    <!-- Inner container: pill on scroll, full-width transparent on home-top -->
    <div
      class="mx-auto flex items-center justify-between transition-all duration-400 ease-out"
      :class="[
        isScrolled
          ? 'header-pill max-w-6xl px-4 sm:px-6 h-14'
          : isHomePage
            ? 'max-w-7xl h-16 px-4 sm:px-6'
            : 'header-pill max-w-6xl px-4 sm:px-6 h-14',
      ]"
    >

      <!-- ── Logo ──────────────────────────────────────────────── -->
      <RouterLink to="/" class="flex items-center gap-2.5 shrink-0 group">
        <!-- Transparent hero state: show full SVG logo (white text variant) -->
        <template v-if="isHomePage && !isScrolled">
          <!-- Icon mark only (white) -->
          <img
            src="/logo-rounded.png"
            alt="Tadabbur logo"
            class="h-8 w-full rounded-lg object-cover transition-transform duration-200 group-hover:scale-105"
          />
        </template>

        <!-- Scrolled / non-home state: show logo mark + dark wordmark -->
        <template v-else>
          <img
            src="/logo-rounded.png"
            alt="Tadabbur logo"
            class="h-8 w-full rounded-lg object-cover transition-transform duration-200 group-hover:scale-105"
          />
          
        </template>
      </RouterLink>

      <!-- ── Desktop Nav ─────────────────────────────────────── -->
      <nav class="hidden md:flex items-center gap-1" role="navigation" aria-label="Main navigation">
        <RouterLink
          to="/learn"
          :class="navLinkClass"
          active-class="!text-brand bg-brand-muted"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
        >
          <!-- Book icon -->
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          {{ t('nav.learn') }}
        </RouterLink>

        <template v-if="auth.isLoggedIn">
          <RouterLink
            to="/dashboard"
            :class="navLinkClass"
            active-class="!text-brand bg-brand-muted"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          >
            <!-- Grid/dashboard icon -->
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            {{ t('nav.dashboard') }}
          </RouterLink>

          <RouterLink
            v-if="auth.isAuthor"
            to="/admin"
            :class="navLinkClass"
            active-class="!text-brand bg-brand-muted"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          >
            <!-- Shield/admin icon -->
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            {{ t('nav.admin') }}
          </RouterLink>
        </template>
      </nav>

      <!-- ── Right Actions ───────────────────────────────────── -->
      <div class="flex items-center gap-2">

        <!-- Language toggle -->
        <button
          id="lang-toggle-btn"
          @click="toggleLocale"
          :title="locale === 'en' ? 'Switch to Arabic' : 'Switch to English'"
          :class="isHomePage && !isScrolled
            ? 'text-white/70 hover:text-white border-white/20 hover:border-white/50 hover:bg-white/10'
            : 'text-gray-500 hover:text-gray-800 border-gray-200 hover:border-gray-300 hover:bg-gray-50'"
          class="hidden sm:flex items-center gap-1.5 text-xs font-semibold border rounded-lg px-2.5 py-1.5 transition-all duration-200"
        >
          <!-- Globe icon -->
          <svg class="w-3.5 h-3.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          {{ locale === 'en' ? 'العربية' : 'English' }}
        </button>

        <!-- Auth: logged in -->
        <template v-if="auth.isLoggedIn">
          <button
            id="logout-btn"
            @click="auth.logout(); $router.push('/')"
            :class="isHomePage && !isScrolled
              ? 'text-white/60 hover:text-red-400'
              : 'text-gray-400 hover:text-red-500'"
            class="hidden sm:flex items-center gap-1.5 text-sm font-medium transition-colors duration-200 px-2 py-1"
            :title="t('nav.logout')"
          >
            <!-- Log out icon -->
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            {{ t('nav.logout') }}
          </button>
        </template>

        <!-- Auth: logged out -->
        <template v-else>
          <RouterLink
            id="login-btn"
            to="/login"
            :class="isHomePage && !isScrolled
              ? 'text-white/70 hover:text-white'
              : 'text-gray-600 hover:text-gray-900'"
            class="hidden sm:block text-sm font-medium transition-colors duration-200 px-2 py-1"
          >
            {{ t('nav.login') }}
          </RouterLink>

          <RouterLink
            id="get-started-btn"
            to="/register"
            class="flex items-center gap-1.5 bg-brand hover:bg-brand-dark text-white
                   text-sm font-semibold px-4 py-2 rounded-xl transition-all duration-200
                   shadow-sm hover:shadow-brand/30 hover:shadow-md hover:-translate-y-px"
          >
            <!-- Spark/star icon -->
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            {{ t('nav.getStarted') }}
          </RouterLink>
        </template>

      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { setLocale } from '@/i18n'

const auth   = useAuthStore()
const route  = useRoute()
const { t, locale } = useI18n({ useScope: 'global' })

// ── Scroll state ───────────────────────────────────────────────────
const isScrolled  = ref(false)
const SCROLL_THRESHOLD = 60

function handleScroll() {
  isScrolled.value = window.scrollY > SCROLL_THRESHOLD
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll() // initialise
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// ── Route helpers ──────────────────────────────────────────────────
const isHomePage = computed(() => route.name === 'home')

// ── Dynamic nav link classes ───────────────────────────────────────
const navLinkClass = computed(() =>
  isHomePage.value && !isScrolled.value
    ? 'text-white/70 hover:text-white hover:bg-white/10'
    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
)

// ── Locale toggle ──────────────────────────────────────────────────
function toggleLocale() {
  setLocale(locale.value === 'en' ? 'ar' : 'en')
}
</script>
