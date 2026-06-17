<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900">{{ t('auth.register.title') }}</h1>
        <p class="text-gray-500 mt-1">{{ t('auth.register.subtitle') }}</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 sm:p-8">
        <form @submit.prevent="handleRegister" class="space-y-5">
          <div v-if="errors.general" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {{ errors.general }}
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ t('auth.register.fullName') }}
              <span class="text-gray-400">{{ t('auth.register.optional') }}</span>
            </label>
            <input
              v-model="form.fullName"
              type="text"
              autocomplete="name"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :placeholder="t('auth.register.namePlaceholder')"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.register.username') }}</label>
            <input
              v-model="form.username"
              type="text"
              required
              autocomplete="username"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :class="{ 'border-red-400': errors.username }"
              :placeholder="t('auth.register.usernamePlaceholder')"
            />
            <p v-if="errors.username" class="text-red-600 text-xs mt-1">{{ errors.username }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.register.email') }}</label>
            <input
              v-model="form.email"
              type="email"
              required
              autocomplete="email"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :class="{ 'border-red-400': errors.email }"
              :placeholder="t('auth.register.emailPlaceholder')"
            />
            <p v-if="errors.email" class="text-red-600 text-xs mt-1">{{ errors.email }}</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('auth.register.password') }}</label>
            <input
              v-model="form.password"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              class="w-full px-4 py-2.5 text-base border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              :placeholder="t('auth.register.passwordHint')"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-emerald-700 hover:bg-emerald-800 disabled:opacity-60 text-white py-2.5 px-4 rounded-lg font-medium transition-colors"
          >
            {{ loading ? t('auth.register.creating') : t('auth.register.create') }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          {{ t('auth.register.hasAccount') }}
          <RouterLink to="/login" class="text-emerald-700 hover:underline font-medium">
            {{ t('auth.register.signIn') }}
          </RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const { t } = useI18n()

const form = ref({ fullName: '', username: '', email: '', password: '' })
const loading = ref(false)
const errors = ref({})

async function handleRegister() {
  errors.value = {}
  loading.value = true
  try {
    await auth.register(form.value.email, form.value.username, form.value.password, form.value.fullName)
    router.push('/dashboard')
  } catch (e) {
    const data = e.response?.data || {}
    if (data.email) errors.value.email = Array.isArray(data.email) ? data.email[0] : data.email
    if (data.username) errors.value.username = Array.isArray(data.username) ? data.username[0] : data.username
    errors.value.general = data.non_field_errors?.[0] || (!data.email && !data.username ? t('auth.register.error') : '')
  } finally {
    loading.value = false
  }
}
</script>
