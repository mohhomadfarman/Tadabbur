/**
 * Updates document.title and all meta tags in <head> for the current page.
 * Tags must already exist in index.html — this only sets their content.
 * Call at the top of <script setup> in any view.
 */
export function useSeo({ title, description, url, image } = {}) {
  const setMeta = (selector, value) => {
    const el = document.querySelector(selector)
    if (el && value) el.setAttribute('content', value)
  }

  if (title) {
    document.title = `${title} — Tadabbur | تدبّر`
    setMeta('meta[property="og:title"]',   title)
    setMeta('meta[name="twitter:title"]',  title)
  }

  if (description) {
    setMeta('meta[name="description"]',          description)
    setMeta('meta[property="og:description"]',   description)
    setMeta('meta[name="twitter:description"]',  description)
  }

  if (url) {
    const canonical = document.querySelector('link[rel="canonical"]')
    if (canonical) canonical.setAttribute('href', url)
    setMeta('meta[property="og:url"]', url)
  }

  if (image) {
    setMeta('meta[property="og:image"]',      image)
    setMeta('meta[name="twitter:image"]',     image)
  }
}
