<template>
  <div class="min-h-screen" style="background:#020205;">

    <!-- ── Breadcrumb ────────────────────────────────────────────────── -->
    <div class="max-w-5xl mx-auto px-4 pt-6 sm:pt-8 pb-4">
      <nav class="text-sm text-white/35 flex items-center gap-2">
        <RouterLink to="/videos" class="hover:text-brand-light transition-colors">Videos</RouterLink>
        <span>/</span>
        <span class="text-white/55 truncate max-w-[200px] sm:max-w-md">{{ video?.title || '…' }}</span>
      </nav>
    </div>

    <!-- ── Loading ───────────────────────────────────────────────────── -->
    <div v-if="loading" class="max-w-5xl mx-auto px-4 pb-20 space-y-4 animate-pulse">
      <div class="aspect-video rounded-2xl bg-white/[0.06]"></div>
      <div class="h-6 bg-white/[0.06] rounded-xl w-2/3"></div>
      <div class="h-4 bg-white/[0.04] rounded-xl w-1/3"></div>
    </div>

    <!-- ── Error ─────────────────────────────────────────────────────── -->
    <div v-else-if="error"
         class="max-w-5xl mx-auto px-4 pb-20">
      <div class="bg-red-900/20 border border-red-500/30 text-red-300 px-6 py-4 rounded-xl text-sm">
        {{ error }}
      </div>
    </div>

    <!-- ── Content ───────────────────────────────────────────────────── -->
    <template v-else-if="video">
      <div class="max-w-5xl mx-auto px-4 pb-20">

        <!-- Embed -->
        <div class="rounded-2xl overflow-hidden shadow-2xl shadow-black/60 mb-6"
             style="border:1px solid rgba(255,255,255,0.08); background:#09090f;">
          <div class="aspect-video">
            <iframe
              :src="video.embed_url"
              class="w-full h-full"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowfullscreen
              :title="video.title"
            ></iframe>
          </div>
        </div>

        <!-- Title + meta -->
        <div class="mb-6">
          <h1 class="text-white text-xl sm:text-2xl lg:text-3xl font-bold leading-snug mb-3">
            {{ video.title }}
          </h1>
          <div class="flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-white/35">
            <span class="flex items-center gap-1.5">
              <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/>
              </svg>
              {{ video.channel_title }}
            </span>
            <span v-if="video.published_at">{{ formatDate(video.published_at) }}</span>
            <span v-if="video.view_count !== '0'"
                  class="flex items-center gap-1.5">
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              {{ Number(video.view_count).toLocaleString() }} views
            </span>
            <a
              :href="`https://www.youtube.com/watch?v=${video.id}`"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center gap-1.5 text-brand-light hover:underline"
            >
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M10 6H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
              Watch on YouTube
            </a>
          </div>
        </div>

        <!-- Description -->
        <div v-if="video.description"
             class="rounded-2xl p-5 sm:p-6"
             style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
          <p class="text-xs font-bold uppercase tracking-widest text-white/25 mb-4">Description</p>
          <p
            class="text-white/50 text-sm leading-relaxed whitespace-pre-line"
            :class="descExpanded ? '' : 'line-clamp-6'"
          >{{ video.description }}</p>
          <button
            v-if="video.description.length > 400"
            @click="descExpanded = !descExpanded"
            class="text-brand-light text-xs font-semibold mt-3 hover:underline"
          >
            {{ descExpanded ? 'Show less' : 'Show more' }}
          </button>
        </div>

        <!-- Back link -->
        <div class="mt-10 pt-8 border-t" style="border-color:rgba(255,255,255,0.06);">
          <RouterLink
            to="/videos"
            class="inline-flex items-center gap-2 text-white/40 hover:text-white transition-colors text-sm font-medium"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
            Back to Videos
          </RouterLink>
        </div>

      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { videosApi } from '@/api/videos'
import { useSeo } from '@/composables/useSeo'

const route       = useRoute()
const video       = ref(null)
const loading     = ref(true)
const error       = ref('')
const descExpanded = ref(false)

// useSeo wraps useHead, which must run synchronously in setup (not inside
// loadVideo/after await). Reactive getter: tags fill in once the video loads.
useSeo(() => {
  const v = video.value
  if (!v) return {}
  return {
    title: `${v.title} — Tadabbur Videos`,
    description: v.description?.slice(0, 160) || 'Watch this Islamic video on Tadabbur.',
  }
})

function formatDate(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' })
}

async function loadVideo(id) {
  loading.value  = true
  error.value    = ''
  video.value    = null
  descExpanded.value = false
  try {
    video.value = await videosApi.getVideo(id)
  } catch (e) {
    error.value = e.response?.status === 404 ? 'Video not found.' : 'Failed to load video.'
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id, id => { if (id) loadVideo(id) })
onMounted(() => loadVideo(route.params.id))
</script>
