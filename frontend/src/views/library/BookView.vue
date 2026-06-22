<template>
  <div class="min-h-screen" style="background:#020205;">

    <!-- ── Breadcrumb ────────────────────────────────────────────────── -->
    <div class="max-w-7xl mx-auto px-4 pt-6 sm:pt-8 pb-4">
      <nav class="text-sm text-white/35 flex items-center gap-2 flex-wrap">
        <RouterLink to="/library" class="hover:text-brand-light transition-colors">Library</RouterLink>
        <span>/</span>
        <span class="text-white/60 truncate max-w-[200px] sm:max-w-xs">{{ book?.title || '…' }}</span>
      </nav>
    </div>

    <!-- ── Loading skeleton ──────────────────────────────────────────── -->
    <div v-if="loading" class="max-w-7xl mx-auto px-4 pb-20">
      <div class="animate-pulse space-y-6">
        <div class="h-8 bg-white/[0.06] rounded-xl w-2/3"></div>
        <div class="h-4 bg-white/[0.04] rounded-xl w-1/3"></div>
        <div class="h-[60vh] bg-white/[0.04] rounded-2xl mt-8"></div>
      </div>
    </div>

    <!-- ── Error ─────────────────────────────────────────────────────── -->
    <div v-else-if="error"
         class="max-w-7xl mx-auto px-4 pb-20">
      <div class="bg-red-900/20 border border-red-500/30 text-red-300 px-6 py-4 rounded-xl text-sm">
        {{ error }}
      </div>
    </div>

    <!-- ── Content ───────────────────────────────────────────────────── -->
    <template v-else-if="book">
      <div class="max-w-7xl mx-auto px-4 pb-20">

        <!-- Desktop: 2-col layout | Mobile: stacked (info first, then PDF) -->
        <div class="flex flex-col lg:flex-row gap-6 lg:gap-8 lg:items-start">

          <!-- ── Info panel ─────────────────────────────────────────── -->
          <div class="w-full lg:w-80 xl:w-96 shrink-0 order-1 lg:order-2">
            <div class="lg:sticky lg:top-28 space-y-4">

              <!-- Cover + title card -->
              <div class="rounded-2xl overflow-hidden p-5 sm:p-6"
                   style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">

                <!-- Cover image -->
                <div class="aspect-[3/4] max-w-[160px] mx-auto rounded-xl overflow-hidden mb-5"
                     style="background:rgba(255,255,255,0.06);">
                  <img v-if="book.cover_url" :src="book.cover_url" :alt="book.title"
                       class="w-full h-full object-cover" />
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <svg class="w-10 h-10 text-white/15" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                            d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                    </svg>
                  </div>
                </div>

                <!-- Category badge -->
                <span v-if="book.category"
                      class="inline-block text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-full mb-3"
                      style="background:rgba(35,78,204,0.15); color:#3d65e8; border:1px solid rgba(35,78,204,0.25);">
                  {{ book.category }}
                </span>

                <h1 class="text-white font-bold text-lg sm:text-xl leading-snug mb-1">{{ book.title }}</h1>
                <p class="text-white/45 text-sm mb-4">{{ book.author || 'Unknown Author' }}</p>

                <!-- Meta chips -->
                <div class="flex flex-wrap gap-2 mb-5">
                  <span v-if="book.page_count"
                        class="text-[11px] text-white/40 border border-white/10 rounded-lg px-2.5 py-1">
                    {{ book.page_count }} pages
                  </span>
                  <span v-if="book.file_size_mb"
                        class="text-[11px] text-white/40 border border-white/10 rounded-lg px-2.5 py-1">
                    {{ book.file_size_mb.toFixed(1) }} MB
                  </span>
                  <span v-if="book.language"
                        class="text-[11px] text-white/40 border border-white/10 rounded-lg px-2.5 py-1 uppercase">
                    {{ book.language }}
                  </span>
                </div>

                <!-- Download button -->
                <a v-if="book.pdf_url"
                   :href="book.pdf_url"
                   download
                   target="_blank"
                   rel="noopener noreferrer"
                   class="w-full flex items-center justify-center gap-2 bg-brand hover:bg-brand-dark text-white
                          font-semibold text-sm px-5 py-3 rounded-xl transition-all duration-200
                          shadow-lg shadow-brand/25 hover:shadow-brand/40 hover:-translate-y-0.5 mb-3"
                >
                  <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"/>
                  </svg>
                  Download PDF
                </a>

                <!-- Open in new tab (mobile friendly) -->
                <a v-if="book.pdf_url"
                   :href="book.pdf_url"
                   target="_blank"
                   rel="noopener noreferrer"
                   class="w-full flex items-center justify-center gap-2 text-white/50 hover:text-white
                          border border-white/10 hover:border-white/25 font-medium text-sm px-5 py-2.5
                          rounded-xl transition-all duration-200"
                >
                  <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                  Open in new tab
                </a>
              </div>

              <!-- Description -->
              <div v-if="book.description"
                   class="rounded-2xl p-5"
                   style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                <p class="text-xs font-bold uppercase tracking-widest text-white/25 mb-3">About this book</p>
                <p class="text-white/50 text-sm leading-relaxed"
                   :class="descExpanded ? '' : 'line-clamp-4'">
                  {{ book.description }}
                </p>
                <button v-if="book.description.length > 200"
                        @click="descExpanded = !descExpanded"
                        class="text-brand-light text-xs font-semibold mt-2 hover:underline">
                  {{ descExpanded ? 'Show less' : 'Read more' }}
                </button>
              </div>

              <!-- Tags -->
              <div v-if="book.tags?.length"
                   class="flex flex-wrap gap-2">
                <span v-for="tag in book.tags" :key="tag"
                      class="text-[11px] text-white/35 border border-white/08 rounded-lg px-2.5 py-1">
                  #{{ tag }}
                </span>
              </div>

            </div>
          </div>

          <!-- ── PDF / Audio viewer ──────────────────────────────────── -->
          <div class="flex-1 order-2 lg:order-1 space-y-4">

            <!-- Audio player -->
            <div v-if="book.audio_url"
                 class="rounded-2xl p-5"
                 style="background:rgba(35,78,204,0.08); border:1px solid rgba(35,78,204,0.2);">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
                     style="background:rgba(35,78,204,0.25);">
                  <svg class="w-4 h-4 text-brand-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M3 18v-6a9 9 0 0 1 18 0v6"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
                  </svg>
                </div>
                <p class="text-brand-light font-semibold text-sm">Audiobook available</p>
              </div>
              <audio
                controls
                :src="book.audio_url"
                class="w-full rounded-xl"
                style="accent-color:#234ecc;"
              >
                Your browser does not support the audio element.
              </audio>
            </div>

            <!-- PDF Viewer -->
            <div v-if="book.pdf_url"
                 class="rounded-2xl overflow-hidden"
                 style="border:1px solid rgba(255,255,255,0.07);">
              <!-- Label bar -->
              <div class="flex items-center justify-between px-4 py-2.5"
                   style="background:#0d0d12; border-bottom:1px solid rgba(255,255,255,0.06);">
                <span class="text-white/40 text-xs font-semibold">PDF Preview</span>
                <a :href="book.pdf_url" target="_blank" rel="noopener noreferrer"
                   class="text-brand-light text-xs font-semibold hover:underline flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                  Full screen
                </a>
              </div>

              <!-- iframe — hidden on mobile (too small), button shown instead -->
              <iframe
                :src="book.pdf_url + '#toolbar=1&navpanes=0'"
                class="hidden sm:block w-full"
                style="height:80vh; background:#09090f;"
                frameborder="0"
                title="PDF Preview"
              ></iframe>

              <!-- Mobile: open-in-browser button instead of iframe -->
              <div class="sm:hidden py-10 text-center px-6"
                   style="background:#09090f;">
                <svg class="w-12 h-12 text-white/15 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"/>
                </svg>
                <p class="text-white/35 text-sm mb-4">PDF preview works best on desktop.<br>Tap below to open on your phone.</p>
                <a :href="book.pdf_url" target="_blank" rel="noopener noreferrer"
                   class="inline-flex items-center gap-2 bg-brand text-white font-semibold text-sm px-6 py-3 rounded-xl">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                  </svg>
                  Open PDF
                </a>
              </div>
            </div>

            <!-- No PDF state -->
            <div v-else
                 class="rounded-2xl py-16 text-center"
                 style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06);">
              <svg class="w-12 h-12 text-white/10 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"/>
              </svg>
              <p class="text-white/25 text-sm">No PDF available for this book yet.</p>
            </div>

          </div>
        </div>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted, onServerPrefetch } from 'vue'
import { useRoute } from 'vue-router'
import { libraryApi } from '@/api/library'
import { useSsrDataStore } from '@/stores/ssrData'
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

const route = useRoute()
const ssr = useSsrDataStore()

const ssrKey = `book:${route.params.slug}`
const book        = ref(ssr.get(ssrKey))
const loading     = ref(book.value == null)
const error       = ref('')
const descExpanded = ref(false)

// useSeo wraps useHead, which must run synchronously in setup (not inside
// onMounted/after await). Reactive getter: tags fill in once the book loads.
useSeo(() => {
  const b = book.value
  if (!b) return {}
  const url = `${SEO_ORIGIN}/library/${b.slug}`
  const desc = b.description?.slice(0, 160) || 'Read this Islamic book on Tadabbur.'
  return {
    title: `${b.title} — Tadabbur Library`,
    description: desc,
    url,
    image: b.cover_url || undefined,
    jsonLd: {
      '@context': 'https://schema.org',
      '@type': 'Book',
      name: b.title,
      author: b.author ? { '@type': 'Person', name: b.author } : undefined,
      description: desc,
      url,
      inLanguage: b.language || undefined,
      numberOfPages: b.page_count || undefined,
      publisher: { '@type': 'Organization', name: 'Tadabbur', url: SEO_ORIGIN },
    },
  }
})

// Prerender the book so its content + SEO meta land in the static HTML.
onServerPrefetch(async () => {
  try {
    book.value = await libraryApi.getBook(route.params.slug)
    ssr.set(ssrKey, book.value)
  } catch {
    /* leave empty; client surfaces the error */
  } finally {
    loading.value = false
  }
})

onMounted(async () => {
  // Books aren't personalized — if it's already prerendered/hydrated, don't refetch.
  if (book.value) return
  try {
    book.value = await libraryApi.getBook(route.params.slug)
  } catch (e) {
    error.value = e.response?.status === 404 ? 'Book not found.' : 'Failed to load book.'
  } finally {
    loading.value = false
  }
})
</script>
