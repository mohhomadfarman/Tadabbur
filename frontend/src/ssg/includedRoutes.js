// Build-time route manifest for vite-ssg (runs in Node during the build, not in
// the browser bundle). Pulls every public URL from the production sitemap.xml so
// prerendering covers all tracks / subjects / lessons / books / videos without
// re-crawling the API.
//
// A failed or suspiciously small sitemap fetch FAILS THE BUILD: silently falling
// back to the static routes would ship a production image where every lesson,
// track, and book page is an empty SPA shell — invisible to crawlers until the
// next successful deploy. Set SSG_ALLOW_FALLBACK=1 to restore warn-and-continue
// (used by the CI compile check and local builds without network access).

const STATIC_ROUTES = ['/', '/learn', '/library', '/launch', '/privacy', '/terms']

// Never prerender auth/personalized routes (they're also absent from sitemap.xml).
const EXCLUDE_PREFIXES = ['/login', '/register', '/dashboard', '/admin']

// A real production sitemap has the static routes plus at least a few tracks
// and lessons; fewer than this means the fetch returned something broken.
const MIN_ROUTES = Number(process.env.SSG_MIN_ROUTES || 10)

const isExcluded = (p) =>
  EXCLUDE_PREFIXES.some((pre) => p === pre || p.startsWith(pre + '/'))

function failOrFallback(reason) {
  if (process.env.SSG_ALLOW_FALLBACK === '1') {
    console.warn(`[ssg] ${reason}; SSG_ALLOW_FALLBACK=1 — prerendering static routes only`)
    return STATIC_ROUTES.filter((p) => !isExcluded(p))
  }
  throw new Error(
    `[ssg] ${reason}. Refusing to build with only ${STATIC_ROUTES.length} static routes — ` +
      'that would deploy a site where no lesson/track/book pages are prerendered. ' +
      'Set SSG_ALLOW_FALLBACK=1 to build anyway (compile checks / offline dev).',
  )
}

export async function includedRoutes(_paths, _routes) {
  const origin = process.env.SSG_ORIGIN || 'https://thetadabbur.org'
  const routes = new Set(STATIC_ROUTES)

  let res
  try {
    res = await fetch(`${origin}/sitemap.xml`, {
      signal: AbortSignal.timeout(15000),
    })
  } catch (err) {
    return failOrFallback(`sitemap fetch from ${origin} failed (${err.message})`)
  }
  if (!res.ok) {
    return failOrFallback(`sitemap fetch from ${origin} returned HTTP ${res.status}`)
  }

  const xml = await res.text()
  let fromSitemap = 0
  for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) {
    try {
      routes.add(new URL(m[1].trim()).pathname)
      fromSitemap++
    } catch {
      /* skip malformed <loc> */
    }
  }
  if (fromSitemap < MIN_ROUTES) {
    return failOrFallback(
      `sitemap from ${origin} yielded only ${fromSitemap} routes (SSG_MIN_ROUTES=${MIN_ROUTES})`,
    )
  }

  console.log(`[ssg] sitemap → ${routes.size} routes from ${origin}`)
  return [...routes].filter((p) => !isExcluded(p))
}
