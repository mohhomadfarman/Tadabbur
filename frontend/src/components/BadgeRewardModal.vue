<template>
  <div
    v-if="current"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-[70] p-4 backdrop-blur-sm"
    @click.self="close"
  >
    <div ref="card" class="bg-white rounded-3xl shadow-2xl max-w-sm w-full overflow-hidden text-center">
      <!-- Celebration header band -->
      <div class="bg-gradient-to-br from-[#234ecc] to-[#1a3ba8] px-6 pt-7 pb-10 relative">
        <p class="text-white/80 text-xs font-semibold tracking-wider uppercase">{{ t('badges.unlocked') }}</p>
        <div ref="medal" class="mx-auto mt-4 w-24 h-24 rounded-full bg-white shadow-lg flex items-center justify-center overflow-hidden">
          <img v-if="current.icon_url" :src="current.icon_url" :alt="current.name" class="w-full h-full object-cover" />
          <svg v-else class="w-12 h-12 text-amber-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 15a5 5 0 1 0 0-10 5 5 0 0 0 0 10z"/><path d="m8.5 13.5-1.8 7.5L12 18l5.3 3-1.8-7.5"/>
          </svg>
        </div>
      </div>

      <!-- Body -->
      <div class="px-6 pt-5 pb-6 -mt-4 bg-white rounded-t-3xl relative">
        <h2 class="text-xl font-bold text-gray-900">{{ current.name }}</h2>
        <p v-if="current.description" class="text-sm text-gray-500 mt-1.5">{{ current.description }}</p>
        <div v-if="current.reward" class="mt-4 inline-flex items-center gap-2 bg-amber-50 text-amber-700 border border-amber-200 rounded-xl px-4 py-2 text-sm font-medium">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 12v10H4V12M2 7h20v5H2zM12 22V7M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7zM12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>
          {{ current.reward }}
        </div>

        <button
          @click="close"
          class="mt-6 w-full bg-[#234ecc] hover:bg-[#1a3ba8] text-white font-semibold py-3 rounded-xl transition-colors"
        >
          {{ queue.length > 1 ? t('badges.next') : t('badges.close') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useBadgesStore } from '@/stores/badges'

const route = useRoute()
const { t } = useI18n()
const auth = useAuthStore()
const badges = useBadgesStore()
const { queue } = storeToRefs(badges)

const card = ref(null)
const medal = ref(null)
const celebratedId = ref(null)

// Don't surface on full-screen chrome (admin / launch) pages.
const current = computed(() =>
  (!route.meta.fullScreen && queue.value.length) ? queue.value[0] : null
)

function close() {
  badges.dismissCurrent()
}

// A celebratory "ta-da!" reward jingle via the Web Audio API — no asset to ship.
// A quick rising pickup (G5→C6) resolving into a bright sustained C-major chord.
function playRewardSound() {
  try {
    const Ctx = window.AudioContext || window.webkitAudioContext
    if (!Ctx) return
    const ctx = new Ctx()
    const now = ctx.currentTime

    const tone = (freq, start, dur, peak = 0.3, type = 'triangle') => {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = type
      osc.frequency.value = freq
      const t0 = now + start
      gain.gain.setValueAtTime(0.0001, t0)
      gain.gain.exponentialRampToValueAtTime(peak, t0 + 0.015)
      gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur)
      osc.connect(gain).connect(ctx.destination)
      osc.start(t0)
      osc.stop(t0 + dur + 0.05)
    }

    // Pickup: "dig-dun" — two quick rising notes.
    tone(783.99, 0.00, 0.14, 0.26)   // G5
    tone(1046.50, 0.12, 0.16, 0.30)  // C6
    // Resolve: a bright, sustained C-major chord (the triumphant "daaa").
    tone(1046.50, 0.28, 0.60, 0.30)             // C6
    tone(1318.51, 0.28, 0.60, 0.22, 'sine')     // E6
    tone(1567.98, 0.30, 0.58, 0.16, 'sine')     // G6

    setTimeout(() => ctx.close().catch(() => {}), 1400)
  } catch { /* audio unavailable — silent */ }
}

// Mobile haptic pat-pat-buzz. No-op on desktop / unsupported browsers (e.g. iOS Safari).
function celebrateHaptics() {
  try {
    if (typeof navigator !== 'undefined' && navigator.vibrate) {
      navigator.vibrate([20, 40, 20, 40, 90])
    }
  } catch { /* ignore */ }
}

async function celebrate() {
  // Confetti burst (lazy-loaded so it stays out of the main bundle / SSR).
  try {
    const confetti = (await import('canvas-confetti')).default
    confetti({ particleCount: 120, spread: 75, origin: { y: 0.5 }, zIndex: 80 })
    setTimeout(() => confetti({ particleCount: 60, spread: 100, origin: { y: 0.45 }, zIndex: 80 }), 250)
  } catch { /* confetti unavailable — skip */ }

  playRewardSound()
  celebrateHaptics()

  // GSAP entrance on the card + a little pop on the medal.
  try {
    const { default: gsap } = await import('gsap')
    await nextTick()
    if (card.value) gsap.fromTo(card.value, { scale: 0.8, opacity: 0, y: 20 }, { scale: 1, opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.7)' })
    if (medal.value) gsap.fromTo(medal.value, { scale: 0, rotate: -30 }, { scale: 1, rotate: 0, duration: 0.6, ease: 'back.out(2)', delay: 0.1 })
  } catch { /* gsap unavailable — static modal */ }
}

// Fire the celebration once per badge as it becomes the visible one.
watch(current, (b) => {
  if (b && b.id !== celebratedId.value) {
    celebratedId.value = b.id
    celebrate()
  }
}, { immediate: true })

// Fetch unseen badges once the user is logged in + profile loaded.
watch(
  () => auth.isLoggedIn && !!auth.user,
  (ready) => { if (ready) badges.fetchUnseen() },
  { immediate: true },
)
</script>
