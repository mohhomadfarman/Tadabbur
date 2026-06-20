import { onBeforeUnmount, watchEffect, isRef, unref } from 'vue'

const SITE_NAME = 'Tadabbur | تدبّر'
const ORIGIN = 'https://thetadabbur.org'

// Defaults restored when a view that set SEO is unmounted, so tags never leak
// from one route to the next (important for the prerender + crawler path).
const DEFAULTS = {
  title: 'Tadabbur | تدبّر — Structured Islamic Learning for the Ummah',
  description:
    'Tadabbur is a free, open-source Islamic learning platform with scholar-verified curriculum, structured tracks, progress tracking, and a growing resource library. Built for the global Ummah.',
  url: `${ORIGIN}/`,
  image: `${ORIGIN}/logo-rounded.png`,
}

/** Find an existing tag or create it in <head>, keyed by a CSS selector. */
function ensureTag(selector, create) {
  let el = document.head.querySelector(selector)
  if (!el) {
    el = create()
    document.head.appendChild(el)
  }
  return el
}

function setMeta(attr, key, value) {
  if (value == null) return
  const el = ensureTag(`meta[${attr}="${key}"]`, () => {
    const m = document.createElement('meta')
    m.setAttribute(attr, key)
    return m
  })
  el.setAttribute('content', value)
}

function setCanonical(href) {
  if (!href) return
  const el = ensureTag('link[rel="canonical"]', () => {
    const l = document.createElement('link')
    l.setAttribute('rel', 'canonical')
    return l
  })
  el.setAttribute('href', href)
}

function setJsonLd(data) {
  // Replace any previously-injected dynamic block (one per page is enough).
  const existing = document.head.querySelector('script[data-dynamic-jsonld]')
  if (existing) existing.remove()
  if (!data) return
  const script = document.createElement('script')
  script.type = 'application/ld+json'
  script.setAttribute('data-dynamic-jsonld', '')
  script.textContent = JSON.stringify(data)
  document.head.appendChild(script)
}

function apply({ title, description, url, image }) {
  if (title) {
    document.title = `${title} — ${SITE_NAME}`
    setMeta('property', 'og:title', title)
    setMeta('name', 'twitter:title', title)
  }
  if (description) {
    setMeta('name', 'description', description)
    setMeta('property', 'og:description', description)
    setMeta('name', 'twitter:description', description)
  }
  if (url) {
    setCanonical(url)
    setMeta('property', 'og:url', url)
  }
  if (image) {
    setMeta('property', 'og:image', image)
    setMeta('name', 'twitter:image', image)
  }
}

/**
 * Set document.title, meta tags, canonical and (optional) JSON-LD for a page.
 * Creates tags that don't yet exist in index.html. Restores defaults on unmount.
 *
 * Accepts either a static object or a getter/ref that returns one — pass a
 * getter from views whose data loads async so tags update once it arrives:
 *
 *   useSeo(() => track.value ? { title: track.value.title, ... } : {})
 *
 * Each field: { title, description, url, image, jsonLd }.
 */
export function useSeo(source = {}) {
  const resolve = () =>
    typeof source === 'function' ? source() : (isRef(source) ? unref(source) : source)

  const render = () => {
    const { title, description, url, image, jsonLd } = resolve() || {}
    apply({ title, description, url, image })
    setJsonLd(jsonLd)
  }

  // Reactive when given a getter/ref; otherwise applies once.
  if (typeof source === 'function' || isRef(source)) {
    watchEffect(render)
  } else {
    render()
  }

  // Restore defaults on unmount so tags don't leak across SPA navigation.
  try {
    onBeforeUnmount(() => {
      apply(DEFAULTS)
      document.title = DEFAULTS.title
      setJsonLd(null)
    })
  } catch {
    // called outside a component lifecycle — no cleanup needed
  }
}

export { ORIGIN as SEO_ORIGIN }
