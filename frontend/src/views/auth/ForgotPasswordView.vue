<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900">{{ t('auth.forgotPassword.title') }}</h1>
        <p class="text-gray-500 mt-1">{{ t('auth.forgotPassword.subtitle') }}</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 sm:p-8">
        <div v-if="sent" class="text-center">
          <p class="text-emerald-700 text-sm bg-emerald-50 border border-emerald-200 rounded-lg px-4 py-3">
            {{ t('auth.forgotPassword.success') }}
          </p>
        </div>

        <form v-else @submit.prevent="handleSubmit" class="space-y-5">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ error }}
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.forgotPassword.email') }}</label>
            <input
              v-model="email"
              type="email"
              required
              autocomplete="email"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :placeholder="t('auth.forgotPassword.emailPlaceholder')"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white py-2.5 px-4 rounded-lg font-medium transition-colors"
          >
            {{ loading ? t('auth.forgotPassword.sending') : t('auth.forgotPassword.send') }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          <RouterLink to="/login" class="text-emerald-700 hover:underline font-medium">
            {{ t('auth.forgotPassword.backToLogin') }}
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { authApi } from '@/api/auth'

const { t } = useI18n()

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const email = ref('')
const loading = ref(false)
const sent = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''
  if (!EMAIL_RE.test(email.value.trim())) {
    error.value = t('auth.register.invalidEmail')
    return
  }
  loading.value = true
  try {
    await authApi.forgotPassword(email.value.trim())
    sent.value = true
  } catch {
    // Backend always returns success for this endpoint (no enumeration), so
    // this only fires on network/server errors.
    error.value = t('auth.login.error')
  } finally {
    loading.value = false
  }
}
</script>
