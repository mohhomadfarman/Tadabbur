import { createI18n } from 'vue-i18n'
import en from './en.json'
import ar from './ar.json'

// During SSG prerender there is no window/document/localStorage. Guard every
// browser access so the i18n module can be imported on the server. The static
// HTML is built in the default locale (en); the client re-applies the persisted
// locale on mount.
const isClient = typeof window !== 'undefined'

const savedLocale = (isClient && localStorage.getItem('tadabbur-locale')) || 'en'

export const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, ar },
})

function applyDocumentDir(locale) {
  if (typeof document === 'undefined') return
  document.documentElement.lang = locale
  document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr'
}

export function setLocale(locale) {
  i18n.global.locale.value = locale
  if (isClient) localStorage.setItem('tadabbur-locale', locale)
  applyDocumentDir(locale)
}

// Apply persisted locale immediately on the client (before Vue mounts).
applyDocumentDir(savedLocale)
