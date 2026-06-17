<template>
  <div id="tadabbur-app">
    <AppHeader />
    <main class="min-h-screen">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/common/AppHeader.vue'

const auth = useAuthStore()

onMounted(() => {
  // Restore session from localStorage on app load
  if (auth.token) {
    auth.fetchUser().catch(() => auth.logout())
  }
})
</script>
