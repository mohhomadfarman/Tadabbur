import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Attaches an IntersectionObserver to a container ref.
 * Every descendant with the `.reveal` class gets `is-visible` added
 * when it enters the viewport, triggering the CSS transition.
 */
export function useScrollReveal({
  threshold  = 0.15,
  rootMargin = '0px 0px -60px 0px',
  once       = true,
} = {}) {
  const containerRef = ref(null)
  let observer = null

  onMounted(() => {
    if (!containerRef.value) return
    const targets = containerRef.value.querySelectorAll('.reveal')
    if (!targets.length) return

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
            if (once) observer.unobserve(entry.target)
          } else if (!once) {
            entry.target.classList.remove('is-visible')
          }
        })
      },
      { threshold, rootMargin },
    )

    targets.forEach((el) => observer.observe(el))
  })

  onUnmounted(() => {
    observer?.disconnect()
    observer = null
  })

  return { containerRef }
}
