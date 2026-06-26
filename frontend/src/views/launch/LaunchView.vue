<template>
  <div class="launch">
    <div class="launch__glow" aria-hidden="true"></div>
    <div class="launch__grid" aria-hidden="true"></div>

    <!-- Minimal top bar -->
    <header class="launch__bar">
      <RouterLink to="/" class="launch__brand">
        <img src="/logo-rounded.png" alt="Tadabbur" class="launch__logo" />
      </RouterLink>
      <RouterLink to="/" class="launch__back">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Back to site
      </RouterLink>
    </header>

    <main class="launch__main">
      <!-- Left: pitch + countdown -->
      <section class="launch__pitch">
        <p class="launch__eyebrow">Live launch event</p>
        <h1 class="launch__title">{{ headline }}</h1>
        <p class="launch__lead">{{ intro }}</p>

        <div class="launch__when">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
          <span>{{ eventDateLabel }}</span>
        </div>

        <div class="launch__countdown" v-if="!ended">
          <div class="cd" v-for="u in countdownUnits" :key="u.label">
            <span class="cd__num">{{ u.value }}</span>
            <span class="cd__label">{{ u.label }}</span>
          </div>
        </div>
        <p v-else class="launch__live">🔴 The event is live — check your email for the link.</p>

        <ul class="launch__points">
          <li>A guided tour of the curriculum, library and progress tracking</li>
          <li>The vision: free Islamic learning for the global Ummah</li>
          <li>Live Q&amp;A — bring your questions</li>
        </ul>
      </section>

      <!-- Right: form / thank-you -->
      <section class="launch__form-wrap">
        <div class="launch__card" v-if="!done">
          <h2 class="launch__card-title">Save your spot</h2>
          <p class="launch__card-sub">Free to attend. We'll send you the link.</p>

          <form @submit.prevent="submit" class="launch__fields" novalidate>
            <div v-if="errors.general" class="launch__error-banner">{{ errors.general }}</div>

            <div>
              <label>Full name</label>
              <input v-model="form.full_name" type="text" autocomplete="name" :class="{ bad: errors.full_name }" placeholder="Your name" />
              <p v-if="errors.full_name" class="launch__err">{{ errors.full_name }}</p>
            </div>

            <div>
              <label>Email</label>
              <input v-model="form.email" type="email" autocomplete="email" :class="{ bad: errors.email }" placeholder="you@example.com" />
              <p v-if="errors.email" class="launch__err">{{ errors.email }}</p>
            </div>

            <div>
              <label>WhatsApp number <span>(optional)</span></label>
              <input v-model="form.phone" type="tel" autocomplete="tel" placeholder="+91 1234567890" />
            </div>

            <div>
              <label>Country / City <span>(optional)</span></label>
              <input v-model="form.country" type="text" placeholder="e.g. Punbjab, India" />
            </div>

            <button type="submit" class="launch__submit" :disabled="loading">
              {{ loading ? 'Registering…' : 'Register for the launch' }}
            </button>
            <p class="launch__fineprint">We'll only use your details for this event. No spam.</p>
          </form>
        </div>

        <!-- Thank-you -->
        <div class="launch__card launch__thanks" v-else>
          <div class="launch__check" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>
          </div>
          <h2 class="launch__card-title">{{ alreadyRegistered ? "You're already in!" : "You're registered!" }}</h2>
          <p class="launch__card-sub">{{ successMessage }}</p>
          <p class="launch__thanks-when">{{ eventDateLabel }}</p>
          <RouterLink to="/" class="launch__thanks-link">Explore Tadabbur while you wait →</RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { eventsApi } from '@/api/events'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

// Page content — defaults shown until the admin-configured settings load.
// Manage these in Admin → Registrations → Event settings.
const eventAt = ref('2026-07-15T18:30:00+05:30')   // ISO 8601 with timezone offset
const headline = ref('Be there when Tadabbur goes live.')
const intro = ref('Join us for the official launch of Tadabbur — a free, structured, scholar-verified Islamic learning platform. Register below to get the live link and event reminders.')

const eventDate = computed(() => new Date(eventAt.value))
const eventDateLabel = computed(() => formatEventLabel(eventAt.value))

// Format the date in the event's OWN timezone offset, so every visitor sees the
// same wall-clock time + offset (e.g. "… 6:30 PM GMT+5:30") regardless of locale.
function formatEventLabel(iso) {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  const m = String(iso).match(/(Z)$|([+-])(\d{2}):(\d{2})$/)
  let offsetMin = 0, label = 'GMT'
  if (m && !m[1]) {
    const sign = m[2] === '-' ? -1 : 1
    const oh = parseInt(m[3], 10), om = parseInt(m[4], 10)
    offsetMin = sign * (oh * 60 + om)
    label = 'GMT' + (sign < 0 ? '-' : '+') + oh + (om ? ':' + String(om).padStart(2, '0') : '')
  }
  const wall = new Date(d.getTime() + offsetMin * 60000).toLocaleString('en-US', {
    timeZone: 'UTC', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    hour: 'numeric', minute: '2-digit',
  })
  return `${wall} ${label}`
}

useSeo({
  title: 'Live Launch — Register',
  description: 'Register for the live launch of Tadabbur, a free, scholar-verified Islamic learning platform. Get the live link and reminders.',
  url: `${SEO_ORIGIN}/launch`,
})

// ── Countdown ──────────────────────────────────────────────────────
const now = ref(Date.now())
let timer = null
onMounted(async () => {
  now.value = Date.now()
  timer = setInterval(() => { now.value = Date.now() }, 1000)
  try {
    const s = await eventsApi.getLaunchSettings()
    if (s.event_at) eventAt.value = s.event_at
    if (s.headline) headline.value = s.headline
    if (s.intro) intro.value = s.intro
  } catch { /* keep defaults */ }
})
onUnmounted(() => { if (timer) clearInterval(timer) })

const remaining = computed(() => Math.max(0, eventDate.value.getTime() - now.value))
const ended = computed(() => remaining.value <= 0)
const countdownUnits = computed(() => {
  const s = Math.floor(remaining.value / 1000)
  return [
    { label: 'Days',    value: Math.floor(s / 86400) },
    { label: 'Hours',   value: Math.floor((s % 86400) / 3600) },
    { label: 'Minutes', value: Math.floor((s % 3600) / 60) },
    { label: 'Seconds', value: s % 60 },
  ].map(u => ({ ...u, value: String(u.value).padStart(2, '0') }))
})

// ── Form ───────────────────────────────────────────────────────────
const form = reactive({ full_name: '', email: '', phone: '', country: '' })
const errors = reactive({ full_name: '', email: '', general: '' })
const loading = ref(false)
const done = ref(false)
const alreadyRegistered = ref(false)
const successMessage = ref('')

function resetErrors() { errors.full_name = ''; errors.email = ''; errors.general = '' }

async function submit() {
  resetErrors()
  if (!form.full_name.trim()) { errors.full_name = 'Please enter your name.'; return }
  if (!form.email.trim()) { errors.email = 'Please enter your email.'; return }
  loading.value = true
  try {
    const res = await eventsApi.registerForLaunch({
      full_name: form.full_name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim(),
      country: form.country.trim(),
    })
    alreadyRegistered.value = !!res.already_registered
    successMessage.value = res.detail || "You're registered! We'll be in touch with the details."
    done.value = true
  } catch (e) {
    const data = e.response?.data || {}
    if (data.full_name) errors.full_name = Array.isArray(data.full_name) ? data.full_name[0] : data.full_name
    if (data.email) errors.email = Array.isArray(data.email) ? data.email[0] : data.email
    if (!data.full_name && !data.email) errors.general = data.detail || 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.launch {
  position: relative;
  min-height: 100svh;
  background: #08070b;
  color: #f6f7fb;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}
.launch__glow {
  position: absolute; top: -20%; left: 50%; width: min(120vw, 1100px); aspect-ratio: 1;
  transform: translateX(-50%);
  background: radial-gradient(circle, rgba(35,78,204,0.32), transparent 62%);
  filter: blur(20px); pointer-events: none;
}
.launch__grid {
  position: absolute; inset: 0; pointer-events: none; opacity: 0.5;
  background-image:
    linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);
  background-size: 64px 64px;
  mask-image: radial-gradient(ellipse 70% 60% at 50% 20%, #000 30%, transparent 75%);
}

.launch__bar {
  position: relative; z-index: 2;
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.25rem clamp(1.25rem, 4vw, 2.5rem);
}
.launch__logo { height: 3rem; width: auto; border-radius: 0.6rem; }
.launch__back {
  display: inline-flex; align-items: center; gap: 0.45rem;
  font-size: 0.85rem; font-weight: 600; color: rgba(255,255,255,0.55); text-decoration: none;
  transition: color 0.2s;
}
.launch__back:hover { color: #fff; }
.launch__back svg { width: 1rem; height: 1rem; }

.launch__main {
  position: relative; z-index: 1;
  display: grid; grid-template-columns: 1.05fr 0.95fr; gap: clamp(2rem, 5vw, 4rem);
  align-items: center;
  max-width: 1200px; margin-inline: auto;
  padding: clamp(1.5rem, 4vw, 3rem) clamp(1.25rem, 4vw, 2.5rem) 4rem;
  min-height: calc(100svh - 6rem);
}

.launch__eyebrow {
  display: inline-block; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.2em;
  text-transform: uppercase; color: #5b7cf0; margin-bottom: 1rem;
}
.launch__title {
  font-size: clamp(2.25rem, 5vw, 3.75rem); font-weight: 800; line-height: 1.05;
  letter-spacing: -0.02em; margin-bottom: 1.25rem;
}
.launch__title span { color: #5b7cf0; }
.launch__lead { font-size: clamp(1rem, 1.4vw, 1.15rem); line-height: 1.7; color: rgba(255,255,255,0.62); max-width: 46ch; }

.launch__when {
  display: inline-flex; align-items: center; gap: 0.6rem; margin-top: 1.75rem;
  font-weight: 600; color: #f6f7fb;
  background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
  padding: 0.6rem 1rem; border-radius: 0.75rem; font-size: 0.95rem;
}
.launch__when svg { width: 1.15rem; height: 1.15rem; color: #5b7cf0; }

.launch__countdown { display: flex; gap: 0.75rem; margin-top: 1.5rem; }
.cd {
  display: flex; flex-direction: column; align-items: center; min-width: 4rem;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 0.85rem; padding: 0.85rem 0.5rem;
}
.cd__num { font-size: clamp(1.5rem, 3vw, 2rem); font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.cd__label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-top: 0.45rem; }
.launch__live { margin-top: 1.5rem; font-weight: 600; color: #fca5a5; }

.launch__points { list-style: none; margin: 2rem 0 0; padding: 0; display: grid; gap: 0.7rem; }
.launch__points li { position: relative; padding-left: 1.6rem; font-size: 0.95rem; color: rgba(255,255,255,0.7); }
.launch__points li::before {
  content: ""; position: absolute; left: 0; top: 0.55em; width: 0.5rem; height: 0.5rem;
  border-radius: 999px; background: #234ecc;
}

/* Form card */
.launch__card {
  background: #fff; color: #111827; border-radius: 1.5rem; padding: clamp(1.5rem, 3vw, 2.25rem);
  box-shadow: 0 30px 60px -20px rgba(0,0,0,0.6);
}
.launch__card-title { font-size: 1.4rem; font-weight: 800; }
.launch__card-sub { color: #6b7280; font-size: 0.92rem; margin-top: 0.25rem; }
.launch__fields { margin-top: 1.5rem; display: grid; gap: 1.1rem; }
.launch__fields label { display: block; font-size: 0.85rem; font-weight: 600; color: #374151; margin-bottom: 0.35rem; }
.launch__fields label span { color: #9ca3af; font-weight: 400; }
.launch__fields input {
  width: 100%; padding: 0.7rem 0.9rem; font-size: 1rem; color: #111827;
  border: 1px solid #e5e7eb; border-radius: 0.7rem; transition: border-color 0.15s, box-shadow 0.15s;
}
.launch__fields input:focus { outline: none; border-color: #234ecc; box-shadow: 0 0 0 3px rgba(35,78,204,0.15); }
.launch__fields input.bad { border-color: #f87171; }
.launch__err { color: #dc2626; font-size: 0.78rem; margin-top: 0.3rem; }
.launch__error-banner { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; font-size: 0.85rem; padding: 0.7rem 0.9rem; border-radius: 0.6rem; }
.launch__submit {
  width: 100%; padding: 0.85rem 1rem; font-size: 1rem; font-weight: 700; color: #fff;
  background: #234ecc; border: none; border-radius: 0.8rem; cursor: pointer; transition: background 0.2s, transform 0.15s;
}
.launch__submit:hover:not(:disabled) { background: #1a3ba8; transform: translateY(-1px); }
.launch__submit:disabled { opacity: 0.6; cursor: default; }
.launch__fineprint { text-align: center; font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem; }

/* Thank-you */
.launch__thanks { text-align: center; }
.launch__check {
  width: 3.5rem; height: 3.5rem; margin: 0 auto 1.25rem; border-radius: 999px;
  background: #dcfce7; color: #16a34a; display: flex; align-items: center; justify-content: center;
}
.launch__check svg { width: 1.75rem; height: 1.75rem; }
.launch__thanks-when { margin-top: 1rem; font-weight: 600; color: #234ecc; }
.launch__thanks-link { display: inline-block; margin-top: 1.5rem; color: #234ecc; font-weight: 600; text-decoration: none; }
.launch__thanks-link:hover { text-decoration: underline; }

@media (max-width: 860px) {
  .launch__main { grid-template-columns: 1fr; padding-top: 1rem; }
  .launch__countdown { flex-wrap: wrap; }
}
</style>
