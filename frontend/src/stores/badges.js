import { defineStore } from 'pinia'
import { ref } from 'vue'
import { badgesApi } from '@/api/badges'

// Queue of just-earned badges awaiting their celebration popup, plus the
// learner's full earned list for the dashboard.
export const useBadgesStore = defineStore('badges', () => {
  const queue = ref([])      // unseen badges to pop, one at a time
  const earned = ref([])     // all earned badges (dashboard)
  const earnedLoaded = ref(false)

  async function fetchUnseen() {
    try {
      const unseen = await badgesApi.getUnseen()
      // Append any not already queued (avoid duplicates across polls).
      const have = new Set(queue.value.map(b => b.id))
      unseen.forEach(b => { if (!have.has(b.id)) queue.value.push(b) })
    } catch { /* ignore */ }
  }

  async function fetchEarned(force = false) {
    if (earnedLoaded.value && !force) return
    try {
      earned.value = await badgesApi.getMine()
      earnedLoaded.value = true
    } catch { /* ignore */ }
  }

  async function dismissCurrent() {
    const b = queue.value[0]
    if (b) {
      badgesApi.markSeen(b.id).catch(() => {})
      queue.value.shift()
    }
  }

  function reset() {
    queue.value = []
    earned.value = []
    earnedLoaded.value = false
  }

  return { queue, earned, earnedLoaded, fetchUnseen, fetchEarned, dismissCurrent, reset }
})
