import { ref, watch } from 'vue'

const KEY = 'homeTheme'
const theme = ref(localStorage.getItem(KEY) || 'dark')

function sync(val) {
  if (val === 'light') {
    document.documentElement.classList.add('home-light')
  } else {
    document.documentElement.classList.remove('home-light')
  }
}

// Apply immediately on module load (prevents flash)
sync(theme.value)

watch(theme, val => {
  localStorage.setItem(KEY, val)
  sync(val)
})

export function useHomeTheme() {
  return {
    theme,
    toggle() {
      theme.value = theme.value === 'dark' ? 'light' : 'dark'
    },
  }
}
