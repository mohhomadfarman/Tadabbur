import { defineStore } from 'pinia'
import { ref } from 'vue'
import { featuresApi } from '@/api/features'

// Effective feature-flag map for the current user. The backend resolves every
// flag's audience/allow-list and returns just booleans, so the UI only needs
// `isEnabled(key)` to gate a feature. Single source of truth: an unknown key
// resolves to false here (the backend always includes every registry key).
export const useFeaturesStore = defineStore('features', () => {
  const flags = ref({})
  const loaded = ref(false)

  async function loadFlags() {
    try {
      flags.value = await featuresApi.getEffective()
      loaded.value = true
    } catch {
      // network/error — leave whatever we had; gates stay closed for unknowns
    }
  }

  function isEnabled(key) {
    return flags.value[key] === true
  }

  function reset() {
    flags.value = {}
    loaded.value = false
  }

  return { flags, loaded, loadFlags, isEnabled, reset }
})
