<template>
  <div class="min-h-screen" style="background:#020205;">

    <!-- ── Page header ──────────────────────────────────────────────── -->
    <div class="max-w-7xl mx-auto px-4 pt-8 pb-6 sm:pt-12 sm:pb-8">
      <p class="section-eyebrow text-brand-light mb-4">
        <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
        Videos
      </p>
      <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight mb-3">
        From Our Channel
      </h1>
      <p class="text-white/40 text-base sm:text-lg max-w-xl">
        Lectures, lessons, and talks — all in one place.
      </p>
    </div>

    <!-- ── Video grid ────────────────────────────────────────────────── -->
    <div class="max-w-7xl mx-auto px-4 pb-20">

      <!-- Loading -->
      <div v-if="loading && videos.length === 0"
           class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div v-for="n in 6" :key="n"
             class="rounded-2xl overflow-hidden animate-pulse"
             style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);">
          <div class="aspect-video bg-white/[0.06]"></div>
          <div class="p-4 space-y-2">
            <div class="h-3 bg-white/[0.06] rounded-full w-full"></div>
            <div class="h-3 bg-white/[0.04] rounded-full w-3/4"></div>
          </div>
        </div>
      </div>

      <!-- Not configured -->
      <div v-else-if="notConfigured"
           class="text-center py-24 px-4">
        <div class="mb-4 flex justify-center">
          <svg class="w-16 h-16 text-white/20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            <path d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z"/>
          </svg>
        </div>
        <h2 class="text-white font-bold text-xl mb-2">YouTube not connected yet</h2>
        <p class="text-white/35 text-sm max-w-sm mx-auto">
          Add <code class="text-brand-light">YOUTUBE_API_KEY</code> and
          <code class="text-brand-light">YOUTUBE_CHANNEL_ID</code> to your <code>.env</code> file to enable this page.
        </p>
      </div>

      <!-- Error -->
      <div v-else-if="error"
           class="bg-red-900/20 border border-red-500/30 text-red-300 px-6 py-4 rounded-xl text-sm">
        {{ error }}
      </div>

      <!-- Empty -->
      <div v-else-if="videos.length === 0" class="text-center py-24">
        <div class="mb-4 flex justify-center">
          <svg class="w-16 h-16 text-white/20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            <path d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z"/>
          </svg>
        </div>
        <p class="text-white/40 text-lg">No videos found.</p>
      </div>

      <!-- Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <RouterLink
          v-for="video in videos"
          :key="video.id"
          :to="{ name: 'video', params: { id: video.id } }"
          class="group flex flex-col rounded-2xl overflow-hidden transition-all duration-200
                 hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/40"
          style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
        >
          <!-- Thumbnail -->
          <div class="relative aspect-video overflow-hidden"
               style="background:#09090f;">
            <img
              v-if="video.thumbnail"
              :src="video.thumbnail"
              :alt="video.title"
              class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              loading="lazy"
            />
            <div v-else class="w-full h-full flex items-center justify-center">
              <svg class="w-10 h-10 text-white/10" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
            </div>

            <!-- Play overlay -->
            <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                 style="background:rgba(0,0,0,0.35);">
              <div class="w-12 h-12 rounded-full flex items-center justify-center backdrop-blur-sm"
                   style="background:rgba(35,78,204,0.85);">
                <svg class="w-5 h-5 text-white ms-0.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>

            <!-- Duration badge placeholder / published date -->
            <div class="absolute bottom-2 end-2 bg-black/70 backdrop-blur-sm rounded-md px-2 py-0.5">
              <span class="text-white text-[10px] font-medium">{{ formatDate(video.published_at) }}</span>
            </div>
          </div>

          <!-- Info -->
          <div class="p-4 flex flex-col flex-1">
            <h3 class="text-white text-sm font-semibold leading-snug line-clamp-2 mb-2
                       group-hover:text-brand-light transition-colors duration-200">
              {{ video.title }}
            </h3>
            <p v-if="video.description"
               class="text-white/30 text-xs leading-relaxed line-clamp-2 mb-3">
              {{ video.description }}
            </p>
            <div class="mt-auto flex items-center gap-2">
              <svg class="w-3 h-3 text-white/20 shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
              </svg>
              <span class="text-white/25 text-[11px]">{{ video.channel_title }}</span>
            </div>
          </div>
        </RouterLink>
      </div>

      <!-- Load more / pagination -->
      <div v-if="nextPageToken && !loading"
           class="mt-10 text-center">
        <button
          @click="loadMore"
          class="inline-flex items-center gap-2 border border-white/15 hover:border-white/30
                 text-white/60 hover:text-white font-semibold text-sm px-6 py-3 rounded-xl
                 transition-all duration-200"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
          Load more videos
        </button>
      </div>

      <!-- Load more skeleton -->
      <div v-if="loading && videos.length > 0"
           class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div v-for="n in 3" :key="n"
             class="rounded-2xl overflow-hidden animate-pulse"
             style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);">
          <div class="aspect-video bg-white/[0.06]"></div>
          <div class="p-4 space-y-2">
            <div class="h-3 bg-white/[0.06] rounded-full w-full"></div>
            <div class="h-3 bg-white/[0.04] rounded-full w-3/4"></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { videosApi } from '@/api/videos'
import { useSeo } from '@/composables/useSeo'

useSeo({
  title: 'Videos — Tadabbur',
  description: 'Watch Islamic lectures, lessons, and talks from our YouTube channel.',
})

const videos        = ref([])
const loading       = ref(true)
const error         = ref('')
const notConfigured = ref(false)
const nextPageToken = ref(null)

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', { year: 'numeric', month: 'short', day: 'numeric' })
}

async function fetchPage(pageToken = '') {
  loading.value = true
  error.value   = ''
  try {
    const data = await videosApi.getVideos(pageToken)
    if (pageToken) {
      videos.value.push(...data.results)
    } else {
      videos.value = data.results
    }
    nextPageToken.value = data.next_page_token || null
  } catch (e) {
    if (e.response?.status === 503) {
      notConfigured.value = true
    } else {
      error.value = 'Failed to load videos. Please try again later.'
    }
  } finally {
    loading.value = false
  }
}

function loadMore() {
  if (nextPageToken.value) fetchPage(nextPageToken.value)
}

onMounted(() => fetchPage())
</script>
