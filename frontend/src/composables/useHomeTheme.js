import { ref, watch } from 'vue'

const KEY = 'homeTheme'
const isClient = typeof window !== 'undefined'

const theme = ref((isClient && localStorage.getItem(KEY)) || 'dark')

function sync(val) {
  if (typeof document === 'undefined') return
  if (val === 'light') {
    document.documentElement.classList.add('home-light')
  } else {
    document.documentElement.classList.remove('home-light')
  }
}

// Apply immediately on the client on module load (prevents flash). On the
// server there's no document, so this is a no-op and the persisted theme is
// re-applied after hydration.
if (isClient) {
  sync(theme.value)
  watch(theme, val => {
    localStorage.setItem(KEY, val)
    sync(val)
  })
}

export function useHomeTheme() {
  return {
    theme,
    toggle() {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
    },
  }
}
