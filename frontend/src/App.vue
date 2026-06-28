<template>
  <div id="tadabbur-app">
    <AppHeader v-if="!route.meta.fullScreen" />
    <!-- Home page: hero sits behind the transparent header (no padding needed).
         Admin pages (fullScreen): own their own chrome entirely, no header padding.
         All other pages: add padding so content isn't hidden under the fixed header. -->
    <main
      class="min-h-screen"
      :class="(isHomePage || route.meta.fullScreen) ? '' : 'pt-24'"
    >
      <RouterView />
    </main>

    <!-- Global admin-authored pop-up modals (logged-in users, normal pages) -->
    <AnnouncementModal />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '@unhead/vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/common/AppHeader.vue'
import AnnouncementModal from '@/components/AnnouncementModal.vue'

const auth  = useAuthStore()
const route = useRoute()

const isHomePage = computed(() => route.name === 'home')

// Keep auth/personalized routes out of search indexes (they're also excluded
// from prerender + sitemap). Overrides the index.html default robots tag.
useHead(() => (route.meta.noindex ? { meta: [{ name: 'robots', content: 'noindex, nofollow' }] } : {}))

onMounted(() => {
  // Restore session from localStorage on app load
  if (auth.token) {
    auth.fetchUser().catch(() => auth.logout())
  }
})
</script>
