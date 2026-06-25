<template>
  <div class="px-6 py-8 max-w-4xl mx-auto">

    <!-- Header -->
    <div class="flex items-start justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Roles &amp; Permissions</h1>
        <p class="text-gray-400 text-sm mt-0.5">Create roles and grant access to admin sections.</p>
      </div>
      <button @click="openCreate"
        class="inline-flex items-center gap-2 bg-[#234ecc] hover:bg-[#1a3ba8] text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors shadow-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"/></svg>
        New role
      </button>
    </div>

    <div v-if="actionError" class="bg-red-50 border border-red-200 text-red-700 px-5 py-3 rounded-xl text-sm mb-6 flex items-start justify-between gap-3">
      <span>{{ actionError }}</span>
      <button @click="actionError = ''" class="text-red-400 hover:text-red-600 shrink-0">✕</button>
    </div>
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm mb-6">{{ error }}</div>

    <div v-if="loading" class="space-y-3 animate-pulse">
      <div v-for="n in 4" :key="n" class="bg-gray-100 rounded-2xl h-24" />
    </div>

    <!-- Role list -->
    <div v-else class="space-y-3">
      <div v-for="r in roles" :key="r.id" class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-gray-900 capitalize">{{ r.label || r.name }}</h3>
              <span v-if="r.is_system" class="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full bg-gray-100 text-gray-500">Built-in</span>
              <span class="text-xs text-gray-400">{{ r.user_count }} user{{ r.user_count === 1 ? '' : 's' }}</span>
            </div>
            <p v-if="r.description" class="text-sm text-gray-500 mt-1">{{ r.description }}</p>
            <div class="flex flex-wrap gap-1.5 mt-3">
              <span v-if="r.sections.length === 0" class="text-xs text-gray-400">No access</span>
              <span v-for="s in r.sections" :key="s" class="text-[11px] font-medium px-2 py-0.5 rounded-full bg-[#234ecc]/8 text-[#234ecc]">
                {{ sectionLabel(s) }}
              </span>
            </div>
          </div>
          <div v-if="!r.is_system" class="flex items-center gap-1 shrink-0">
            <button @click="openEdit(r)" title="Edit" class="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-[#234ecc] hover:bg-[#234ecc]/8 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            </button>
            <button @click="deleteTarget = r" title="Delete" class="w-8 h-8 rounded-lg flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
          <span v-else class="text-gray-300 shrink-0" title="Built-in roles are managed by the system">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </span>
        </div>
      </div>
    </div>

    <!-- Editor modal -->
    <div v-if="editing" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="editing = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
        <h3 class="font-bold text-gray-900 mb-4">{{ editing.id ? 'Edit role' : 'New role' }}</h3>

        <div class="space-y-4">
          <div v-if="!editing.id">
            <label class="block text-xs font-medium text-gray-500 mb-1">Name (lowercase, unique)</label>
            <input v-model="editing.name" type="text" placeholder="e.g. editor"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Label</label>
            <input v-model="editing.label" type="text" placeholder="e.g. Content Editor"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-1">Description</label>
            <input v-model="editing.description" type="text" placeholder="What can this role do?"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40" />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-500 mb-2">Section access</label>
            <div class="grid grid-cols-2 gap-2">
              <label v-for="s in sections" :key="s.key" class="flex items-center gap-2 text-sm text-gray-700 border border-gray-200 rounded-lg px-3 py-2 cursor-pointer hover:bg-gray-50">
                <input type="checkbox" :value="s.key" v-model="editing.sections" class="accent-[#234ecc]" />
                {{ s.label }}
              </label>
            </div>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button @click="editing = null" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="saving || (!editing.id && !validName)" @click="save"
            class="flex-1 px-4 py-2.5 bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Saving…' : (editing.id ? 'Save changes' : 'Create role') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete modal -->
    <div v-if="deleteTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete role?</h3>
        <p class="text-sm text-gray-500 mb-5">"<strong>{{ deleteTarget.label || deleteTarget.name }}</strong>" will be removed. Users must be reassigned first.</p>
        <div class="flex gap-3">
          <button @click="deleteTarget = null" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="saving" @click="doDelete" class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ saving ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/api/admin'

const roles = ref([])
const sections = ref([])
const loading = ref(true)
const error = ref('')
const actionError = ref('')
const saving = ref(false)

const editing = ref(null)        // { id?, name, label, description, sections: [] }
const deleteTarget = ref(null)

const validName = computed(() => /^[a-z0-9][a-z0-9_-]{1,49}$/.test((editing.value?.name || '').trim()))

function sectionLabel(key) {
  return sections.value.find(s => s.key === key)?.label || key
}

function openCreate() {
  editing.value = { name: '', label: '', description: '', sections: [] }
}
function openEdit(r) {
  editing.value = { id: r.id, name: r.name, label: r.label, description: r.description, sections: [...r.sections] }
}

function apiError(e, fallback) {
  return e?.response?.data?.name || e?.response?.data?.detail || fallback
}

async function save() {
  saving.value = true
  try {
    const payload = {
      label: editing.value.label,
      description: editing.value.description,
      sections: editing.value.sections,
    }
    if (editing.value.id) {
      const updated = await adminApi.updateRole(editing.value.id, payload)
      const i = roles.value.findIndex(r => r.id === updated.id)
      if (i !== -1) roles.value[i] = updated
    } else {
      const created = await adminApi.createRole({ name: editing.value.name.trim().toLowerCase(), ...payload })
      roles.value.push(created)
    }
    editing.value = null
  } catch (e) {
    actionError.value = apiError(e, 'Could not save role.')
  } finally {
    saving.value = false
  }
}

async function doDelete() {
  saving.value = true
  try {
    await adminApi.deleteRole(deleteTarget.value.id)
    roles.value = roles.value.filter(r => r.id !== deleteTarget.value.id)
    deleteTarget.value = null
  } catch (e) {
    actionError.value = apiError(e, 'Could not delete role.')
    deleteTarget.value = null
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    sections.value = await adminApi.listSections()
    roles.value = await adminApi.listRoles()
  } catch {
    error.value = 'Could not load roles. Make sure your account has Roles access.'
  } finally {
    loading.value = false
  }
})
</script>
