import { isRef, unref } from 'vue'
import { useHead } from '@unhead/vue'

const SITE_NAME = 'Tadabbur | تدبّر'
const ORIGIN = 'https://thetadabbur.org'

// Fallbacks used for any field a page doesn't supply, so every page emits a
// complete, coherent set of tags.
const DEFAULTS = {
  title: 'Tadabbur | تدبّر — Structured Islamic Learning for the Ummah',
  description:
    'Tadabbur is a free, open-source Islamic learning platform with scholar-verified curriculum, structured tracks, progress tracking, and a growing resource library. Built for the global Ummah.',
  url: `${ORIGIN}/`,
  image: `${ORIGIN}/logo-rounded.png`,
}

/**
 * Set <title>, meta tags, canonical and (optional) JSON-LD for a page via
 * @unhead/vue, so they render into the prerendered HTML server-side (visible to
 * crawlers and social scrapers that never run JS) and stay reactive on the
 * client. unhead dedupes against the static tags in index.html and removes the
 * page's tags automatically on unmount.
 *
 * Accepts a static object, a ref, or a getter that returns one. Pass a getter
 * from views whose data loads async so tags update once it arrives:
 *
 *   useSeo(() => track.value ? { title: track.value.title, ... } : {})
 *
 * Each field: { title, description, url, image, jsonLd, noindex }.
 */
export function useSeo(source = {}) {
  const resolve = () =>
    (typeof source === 'function' ? source() : isRef(source) ? unref(source) : source) || {}

  useHead(() => {
    const { title, description, url, image, jsonLd, noindex } = resolve()

    const ogTitle = title || DEFAULTS.title
    const desc = description || DEFAULTS.description
    const canonical = url || DEFAULTS.url
    const img = image || DEFAULTS.image

    const meta = [
      { name: 'description', content: desc },
      { property: 'og:title', content: ogTitle },
      { property: 'og:description', content: desc },
      { property: 'og:url', content: canonical },
      { property: 'og:image', content: img },
      { name: 'twitter:title', content: ogTitle },
      { name: 'twitter:description', content: desc },
      { name: 'twitter:image', content: img },
    ]
    if (noindex) meta.push({ name: 'robots', content: 'noindex, nofollow' })

    return {
      title: title ? `${title} — ${SITE_NAME}` : DEFAULTS.title,
      meta,
      link: [{ rel: 'canonical', href: canonical }],
      script: jsonLd
        ? [{ type: 'application/ld+json', innerHTML: JSON.stringify(jsonLd) }]
        : [],
    }
  })
}

export { ORIGIN as SEO_ORIGIN }
