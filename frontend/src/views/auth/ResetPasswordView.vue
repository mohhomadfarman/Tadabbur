<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900">{{ t('auth.resetPassword.title') }}</h1>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 sm:p-8">
        <div v-if="!token" class="text-center">
          <p class="text-red-700 text-sm bg-red-50 border border-red-200 rounded-lg px-4 py-3">
            {{ t('auth.resetPassword.invalidToken') }}
          </p>
          <RouterLink to="/forgot-password" class="inline-block mt-4 text-emerald-700 hover:underline font-medium text-sm">
            {{ t('auth.forgotPassword.title') }}
          </RouterLink>
        </div>

        <div v-else-if="success" class="text-center">
          <p class="text-emerald-700 text-sm bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
            {{ t('auth.resetPassword.success') }}
          </p>
          <RouterLink to="/login" class="inline-block mt-4 text-emerald-700 hover:underline font-medium text-sm">
            {{ t('auth.resetPassword.goToLogin') }}
          </RouterLink>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-5">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.resetPassword.password') }}</label>
            <input
              v-model="password"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :placeholder="t('auth.resetPassword.passwordHint')"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.resetPassword.confirm') }}</label>
            <input
              v-model="confirm"
              type="password"
              required
              autocomplete="new-password"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
            <p v-if="mismatch" class="text-red-600 text-xs mt-1">{{ t('auth.resetPassword.mismatch') }}</p>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white py-2.5 px-4 rounded-lg font-medium transition-colors"
          >
            {{ loading ? t('auth.resetPassword.saving') : t('auth.resetPassword.save') }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { authApi } from '@/api/auth'

const route = useRoute()
const { t } = useI18n()

const token = computed(() => (route.query.token || '').toString())
const password = ref('')
const confirm = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

const mismatch = computed(() => confirm.value.length > 0 && password.value !== confirm.value)

async function handleSubmit() {
  error.value = ''
  if (password.value.length < 8) {
    error.value = t('auth.resetPassword.passwordHint')
    return
  }
  if (password.value !== confirm.value) return

  loading.value = true
  try {
    await authApi.resetPassword(token.value, password.value)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.error || t('auth.resetPassword.invalidToken')
  } finally {
    loading.value = false
  }
}
</script>
