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
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/common/AppHeader.vue'

const auth  = useAuthStore()
const route = useRoute()

const isHomePage = computed(() => route.name === 'home')

onMounted(() => {
  // Restore session from localStorage on app load
  if (auth.token) {
    auth.fetchUser().catch(() => auth.logout())
  }
})
</script>
