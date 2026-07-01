<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md text-center">
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <p v-if="state === 'pending'" class="text-gray-500">{{ t('auth.verifyEmail.verifying') }}</p>

        <template v-else-if="state === 'success'">
          <p class="text-emerald-700 text-sm bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
            {{ t('auth.verifyEmail.success') }}
          </p>
          <RouterLink :to="auth.isLoggedIn ? '/dashboard' : '/login'" class="inline-block mt-4 text-emerald-700 hover:underline font-medium text-sm">
            {{ auth.isLoggedIn ? t('auth.verifyEmail.goToDashboard') : t('auth.verifyEmail.goToLogin') }}
          </RouterLink>
        </template>

        <template v-else-if="state === 'error'">
          <p class="text-red-700 text-sm bg-red-50 border border-red-200 rounded-lg px-4 py-3">
            {{ t('auth.verifyEmail.error') }}
          </p>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()
const { t } = useI18n()

const state = ref('pending')

onMounted(async () => {
  const token = (route.query.token || '').toString()
  if (!token) {
    state.value = 'error'
    return
  }
  try {
    await authApi.verifyEmail(token)
    state.value = 'success'
    if (auth.isLoggedIn) auth.fetchUser().catch(() => {})
  } catch {
    state.value = 'error'
  }
})
</script>
