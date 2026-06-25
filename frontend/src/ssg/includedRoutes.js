// Build-time route manifest for vite-ssg (runs in Node during the build, not in
// the browser bundle). Pulls every public URL from the production sitemap.xml so
// prerendering covers all tracks / subjects / lessons / books / videos without
// re-crawling the API. If the sitemap is unreachable we fall back to the static
// routes so the build never fails on a transient network/prod issue.

const STATIC_ROUTES = ['/', '/learn', '/library', '/videos', '/privacy', '/terms']

// Never prerender auth/personalized routes (they're also absent from sitemap.xml).
const EXCLUDE_PREFIXES = ['/login', '/register', '/dashboard', '/admin']

const isExcluded = (p) =>
  EXCLUDE_PREFIXES.some((pre) => p === pre || p.startsWith(pre + '/'))

export async function includedRoutes(_paths, _routes) {
  const origin = process.env.SSG_ORIGIN || 'https://thetadabbur.org'
  const routes = new Set(STATIC_ROUTES)

  try {
    const res = await fetch(`${origin}/sitemap.xml`, {
      signal: AbortSignal.timeout(15000),
    })
    if (res.ok) {
      const xml = await res.text()
      for (const m of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) {
        try {
          routes.add(new URL(m[1].trim()).pathname)
        } catch {
          /* skip malformed <loc> */
        }
      }
      console.log(`[ssg] sitemap → ${routes.size} routes from ${origin}`)
    } else {
      console.warn(`[ssg] sitemap fetch ${res.status}; prerendering static routes only`)
    }
  } catch (err) {
    console.warn(`[ssg] sitemap fetch failed (${err.message}); prerendering static routes only`)
  }

  return [...routes].filter((p) => !isExcluded(p))
}
