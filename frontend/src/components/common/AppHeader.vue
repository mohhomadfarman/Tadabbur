<template>
  <!-- Fixed wrapper — always full-width, transparent background -->
  <header
    class="fixed top-0 left-0 right-0 z-50 transition-all duration-400 ease-out"
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
        <img
          src="/logo-rounded.png"
          alt="Tadabbur logo"
          class="h-11 w-auto rounded-lg object-cover transition-transform duration-200 group-hover:scale-105"
        />
      </RouterLink>

      <!-- ── Desktop Nav ─────────────────────────────────────── -->
      <nav class="hidden md:flex items-center gap-1" role="navigation" aria-label="Main navigation">
        <RouterLink
          to="/learn"
          :class="navLinkClass"
          active-class="!text-brand bg-brand-muted"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          {{ t('nav.learn') }}
        </RouterLink>

        <RouterLink
          to="/library"
          :class="navLinkClass"
          active-class="!text-brand bg-brand-muted"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
          </svg>
          Library
        </RouterLink>

        <RouterLink
          to="/videos"
          :class="navLinkClass"
          active-class="!text-brand bg-brand-muted"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
        >
          <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
          </svg>
          Videos
        </RouterLink>

        <template v-if="auth.isLoggedIn">
          <RouterLink
            to="/dashboard"
            :class="navLinkClass"
            active-class="!text-brand bg-brand-muted"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="3" y="3" width="7" height="7" rx="1"/>
              <rect x="14" y="3" width="7" height="7" rx="1"/>
              <rect x="3" y="14" width="7" height="7" rx="1"/>
              <rect x="14" y="14" width="7" height="7" rx="1"/>
            </svg>
            {{ t('nav.dashboard') }}
          </RouterLink>

          <RouterLink
            v-if="auth.hasAdminAccess"
            to="/admin"
            :class="navLinkClass"
            active-class="!text-brand bg-brand-muted"
            class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            {{ t('nav.admin') }}
          </RouterLink>
        </template>
      </nav>

      <!-- ── Right Actions ───────────────────────────────────── -->
      <div class="flex items-center gap-2">

        <!-- Dark / Light toggle (home page only) -->
        <button
          v-if="isHomePage"
          @click="homeTheme.toggle()"
          :title="homeTheme.theme.value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
          :class="isHomePage && !isScrolled
            ? homeTheme.theme.value === 'dark'
              ? 'text-white/70 hover:text-white border-white/20 hover:border-white/50 hover:bg-white/10'
              : 'text-gray-700 hover:text-gray-900 border-gray-300 hover:border-gray-400 hover:bg-gray-100'
            : 'text-gray-500 hover:text-gray-800 border-gray-200 hover:border-gray-300 hover:bg-gray-50'"
          class="hidden sm:flex items-center justify-center w-8 h-8 border rounded-lg transition-all duration-200"
        >
          <!-- Sun: currently dark → click to go light -->
          <svg v-if="homeTheme.theme.value === 'dark'" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="4"/>
            <path stroke-linecap="round" d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
          </svg>
          <!-- Moon: currently light → click to go dark -->
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>

        <!-- Language toggle (desktop only) -->
        <button
          id="lang-toggle-btn"
          @click="toggleLocale"
          :title="locale === 'en' ? 'Switch to Arabic' : 'Switch to English'"
          :class="isHomePage && !isScrolled
            ? homeTheme.theme.value === 'dark'
              ? 'text-white/70 hover:text-white border-white/20 hover:border-white/50 hover:bg-white/10'
              : 'text-gray-700 hover:text-gray-900 border-gray-300 hover:border-gray-400 hover:bg-gray-100'
            : 'text-gray-500 hover:text-gray-800 border-gray-200 hover:border-gray-300 hover:bg-gray-50'"
          class="hidden sm:flex items-center gap-1.5 text-xs font-semibold border rounded-lg px-2.5 py-1.5 transition-all duration-200"
        >
          <svg class="w-3.5 h-3.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
          {{ locale === 'en' ? 'العربية' : 'English' }}
        </button>

        <!-- Auth: logged in (desktop) -->
        <template v-if="auth.isLoggedIn">
          <button
            id="logout-btn"
            @click="handleLogout"
            :class="isHomePage && !isScrolled
              ? homeTheme.theme.value === 'dark' ? 'text-white/60 hover:text-red-400' : 'text-gray-500 hover:text-red-500'
              : 'text-gray-400 hover:text-red-500'"
            class="hidden sm:flex items-center gap-1.5 text-sm font-medium transition-colors duration-200 px-2 py-1"
            :title="t('nav.logout')"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            {{ t('nav.logout') }}
          </button>
        </template>

        <!-- Auth: logged out (desktop) -->
        <template v-else>
          <RouterLink
            id="login-btn"
            to="/login"
            :class="isHomePage && !isScrolled
              ? homeTheme.theme.value === 'dark' ? 'text-white/70 hover:text-white' : 'text-gray-700 hover:text-gray-900'
              : 'text-gray-600 hover:text-gray-900'"
            class="hidden sm:block text-sm font-medium transition-colors duration-200 px-2 py-1"
          >
            {{ t('nav.login') }}
          </RouterLink>

          <RouterLink
            id="get-started-btn"
            to="/register"
            class="hidden sm:flex items-center gap-1.5 bg-brand hover:bg-brand-dark text-white
                   text-sm font-semibold px-4 py-2 rounded-xl transition-all duration-200
                   shadow-sm hover:shadow-brand/30 hover:shadow-md hover:-translate-y-px"
          >
            <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            {{ t('nav.getStarted') }}
          </RouterLink>
        </template>

        <!-- Hamburger button (mobile only, < md) -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          :class="isHomePage && !isScrolled
            ? homeTheme.theme.value === 'dark'
              ? 'text-white/80 hover:text-white hover:bg-white/10'
              : 'text-gray-800 hover:text-gray-900 hover:bg-black/[0.06]'
            : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
          class="md:hidden flex items-center justify-center w-9 h-9 rounded-lg transition-all duration-200"
          :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
          :aria-expanded="mobileMenuOpen"
        >
          <!-- Hamburger / X icon -->
          <svg v-if="!mobileMenuOpen" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>

      </div>
    </div>

    <!-- ── Mobile Menu Drawer ──────────────────────────────────── -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <div
        v-if="mobileMenuOpen"
        class="md:hidden mt-2 mx-auto max-w-6xl"
      >
        <nav
          class="bg-white border border-gray-100 rounded-2xl shadow-xl overflow-hidden"
          role="navigation"
          aria-label="Mobile navigation"
        >
          <!-- Nav links -->
          <div class="p-3 space-y-1">
            <RouterLink
              to="/learn"
              active-class="bg-brand-muted text-brand"
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
              @click="mobileMenuOpen = false"
            >
              <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              {{ t('nav.learn') }}
            </RouterLink>

            <RouterLink
              to="/library"
              active-class="bg-brand-muted text-brand"
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
              @click="mobileMenuOpen = false"
            >
              <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
              </svg>
              Library
            </RouterLink>

            <RouterLink
              to="/videos"
              active-class="bg-brand-muted text-brand"
              class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
              @click="mobileMenuOpen = false"
            >
              <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
              </svg>
              Videos
            </RouterLink>

            <template v-if="auth.isLoggedIn">
              <RouterLink
                to="/dashboard"
                active-class="bg-brand-muted text-brand"
                class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
                @click="mobileMenuOpen = false"
              >
                <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                active-class="bg-brand-muted text-brand"
                class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 hover:text-gray-900 transition-colors"
                @click="mobileMenuOpen = false"
              >
                <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                {{ t('nav.admin') }}
              </RouterLink>
            </template>
          </div>

          <!-- Divider + footer actions -->
          <div class="border-t border-gray-100 p-3 flex items-center justify-between gap-2">

            <!-- Language toggle -->
            <button
              @click="toggleLocale"
              class="flex items-center gap-1.5 text-xs font-semibold border border-gray-200 text-gray-500 hover:text-gray-800 hover:border-gray-300 hover:bg-gray-50 rounded-lg px-3 py-2 transition-all duration-200"
            >
              <svg class="w-3.5 h-3.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
              </svg>
              {{ locale === 'en' ? 'العربية' : 'English' }}
            </button>

            <!-- Dark / Light toggle (home page only) -->
            <button
              v-if="isHomePage"
              @click="homeTheme.toggle()"
              :title="homeTheme.theme.value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
              class="flex items-center gap-1.5 text-xs font-semibold border border-gray-200 text-gray-500
                     hover:text-gray-800 hover:border-gray-300 hover:bg-gray-50 rounded-lg px-3 py-2
                     transition-all duration-200"
            >
              <svg v-if="homeTheme.theme.value === 'dark'" class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="4"/>
                <path stroke-linecap="round" d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
              </svg>
              <svg v-else class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
              {{ homeTheme.theme.value === 'dark' ? 'Light mode' : 'Dark mode' }}
            </button>

            <!-- Auth actions -->
            <div class="flex items-center gap-2">
              <template v-if="auth.isLoggedIn">
                <button
                  @click="handleLogout"
                  class="flex items-center gap-1.5 text-sm font-medium text-gray-400 hover:text-red-500 px-3 py-2 rounded-xl transition-colors"
                >
                  <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                    <polyline points="16 17 21 12 16 7"/>
                    <line x1="21" y1="12" x2="9" y2="12"/>
                  </svg>
                  {{ t('nav.logout') }}
                </button>
              </template>
              <template v-else>
                <RouterLink
                  to="/login"
                  class="text-sm font-medium text-gray-600 hover:text-gray-900 px-3 py-2 rounded-xl transition-colors"
                  @click="mobileMenuOpen = false"
                >
                  {{ t('nav.login') }}
                </RouterLink>
                <RouterLink
                  to="/register"
                  class="flex items-center gap-1.5 bg-brand hover:bg-brand-dark text-white text-sm font-semibold px-4 py-2 rounded-xl transition-all duration-200"
                  @click="mobileMenuOpen = false"
                >
                  {{ t('nav.getStarted') }}
                </RouterLink>
              </template>
            </div>

          </div>
        </nav>
      </div>
    </Transition>

  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { setLocale } from '@/i18n'
import { useHomeTheme } from '@/composables/useHomeTheme'

const auth      = useAuthStore()
const route     = useRoute()
const router    = useRouter()
const homeTheme = useHomeTheme()
const { t, locale } = useI18n({ useScope: 'global' })

// ── Scroll state ───────────────────────────────────────────────────
const isScrolled  = ref(false)
const SCROLL_THRESHOLD = 60

function handleScroll() {
  isScrolled.value = window.scrollY > SCROLL_THRESHOLD
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

// ── Mobile menu ────────────────────────────────────────────────────
const mobileMenuOpen = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => { mobileMenuOpen.value = false })

// ── Route helpers ──────────────────────────────────────────────────
const isHomePage = computed(() => route.name === 'home')

// ── Dynamic nav link classes ───────────────────────────────────────
const navLinkClass = computed(() => {
  if (!isHomePage.value || isScrolled.value) return 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
  return homeTheme.theme.value === 'dark'
    ? 'text-white/70 hover:text-white hover:bg-white/10'
    : 'text-gray-800 hover:text-gray-900 hover:bg-black/[0.06]'
})

// ── Auth ───────────────────────────────────────────────────────────
function handleLogout() {
  mobileMenuOpen.value = false
  auth.logout()
  router.push('/')
}

// ── Locale toggle ──────────────────────────────────────────────────
function toggleLocale() {
  setLocale(locale.value === 'en' ? 'ar' : 'en')
}
</script>
