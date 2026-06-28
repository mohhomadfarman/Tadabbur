<template>
  <div class="px-6 py-8 max-w-2xl mx-auto">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Email Settings</h1>
      <p class="text-gray-400 text-sm mt-0.5">SMTP credentials used to send campaigns. Stored securely; the password is never shown again.</p>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <div v-if="loading" class="animate-pulse space-y-3">
      <div v-for="n in 6" :key="n" class="bg-gray-100 rounded-xl h-12" />
    </div>

    <template v-else>
      <!-- Status -->
      <div class="mb-6 flex items-center gap-2 text-sm">
        <span v-if="form.configured" class="inline-flex items-center gap-1.5 text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-full px-3 py-1 font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500" /> SMTP configured
        </span>
        <span v-else class="inline-flex items-center gap-1.5 text-amber-700 bg-amber-50 border border-amber-200 rounded-full px-3 py-1 font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-amber-500" /> Not configured — sends use the dev console backend
        </span>
      </div>

      <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-4">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">SMTP host</label>
            <input v-model="form.host" type="text" placeholder="smtp.your-provider.com"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Port</label>
            <input v-model.number="form.port" type="number"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Username</label>
          <input v-model="form.username" type="text" autocomplete="off" placeholder="SMTP username / API key id"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
          <input v-model="passwordInput" type="password" autocomplete="new-password"
            :placeholder="form.has_password ? `Saved (${form.password_hint}) — leave blank to keep` : 'SMTP password / API key'"
            class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          <button v-if="form.has_password" type="button" @click="clearPassword = !clearPassword"
            class="mt-1.5 text-xs" :class="clearPassword ? 'text-red-600 font-medium' : 'text-gray-400 hover:text-gray-600'">
            {{ clearPassword ? 'Will remove the saved password on save' : 'Remove saved password' }}
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">From address</label>
            <input v-model="form.from_email" type="text" placeholder="Tadabbur <no-reply@thetadabbur.org>"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div class="flex items-end gap-4 pb-1">
            <label class="inline-flex items-center gap-2 text-sm text-gray-700">
              <input v-model="form.use_tls" type="checkbox" class="rounded border-gray-300 text-[#234ecc] focus:ring-[#234ecc]/40" /> TLS
            </label>
            <label class="inline-flex items-center gap-2 text-sm text-gray-700">
              <input v-model="form.use_ssl" type="checkbox" class="rounded border-gray-300 text-[#234ecc] focus:ring-[#234ecc]/40" /> SSL
            </label>
          </div>
        </div>

        <p class="text-[11px] text-gray-400">Use TLS for port 587 (STARTTLS) or SSL for port 465. Leave the host blank to disable real sending in development.</p>

        <div class="flex items-center justify-end gap-3 pt-2 border-t border-gray-100">
          <span v-if="saved" class="text-sm text-emerald-600 font-medium">Saved ✓</span>
          <button :disabled="saving" @click="save"
            class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            {{ saving ? 'Saving…' : 'Save settings' }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const form = reactive({ host: '', port: 587, username: '', use_tls: true, use_ssl: false, from_email: '', has_password: false, password_hint: '', configured: false })
const passwordInput = ref('')
const clearPassword = ref(false)
const loading = ref(true)
const saving = ref(false)
const saved = ref(false)
const error = ref('')

function apply(data) {
  Object.assign(form, {
    host: data.host || '', port: data.port || 587, username: data.username || '',
    use_tls: !!data.use_tls, use_ssl: !!data.use_ssl, from_email: data.from_email || '',
    has_password: !!data.has_password, password_hint: data.password_hint || '', configured: !!data.configured,
  })
}

async function load() {
  loading.value = true
  try {
    apply(await adminApi.getEmailSettings())
  } catch {
    error.value = 'Could not load email settings. Make sure your account has Email Marketing access.'
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true; error.value = ''
  try {
    const payload = {
      host: form.host.trim(),
      port: form.port,
      username: form.username.trim(),
      use_tls: form.use_tls,
      use_ssl: form.use_ssl,
      from_email: form.from_email.trim(),
    }
    if (clearPassword.value) payload.clear_password = true
    else if (passwordInput.value) payload.password = passwordInput.value
    apply(await adminApi.updateEmailSettings(payload))
    passwordInput.value = ''
    clearPassword.value = false
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
  } catch (e) {
    error.value = e?.response?.data?.port || 'Could not save settings.'
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
