import { createI18n } from 'vue-i18n'
import en from './en.json'
import ar from './ar.json'

const savedLocale = localStorage.getItem('tadabbur-locale') || 'en'

export const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, ar },
})

export function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('tadabbur-locale', locale)
  document.documentElement.lang = locale
  document.documentElement.dir = locale === 'ar' ? 'rtl' : 'ltr'
}

// Apply persisted locale immediately (before Vue mounts)
document.documentElement.lang = savedLocale
document.documentElement.dir = savedLocale === 'ar' ? 'rtl' : 'ltr'
