<template>
  <div class="home-page overflow-hidden">

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 1 — HERO                                              -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section
      data-hero-section
      class="relative min-h-[100dvh] flex flex-col justify-center bg-[#020205] overflow-hidden pt-28 pb-20 px-4"
    >
      <!-- Background grid -->
      <div
        class="absolute inset-0 pointer-events-none"
        style="background-image: linear-gradient(rgba(35,78,204,0.04) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(35,78,204,0.04) 1px, transparent 1px);
               background-size: 64px 64px;"
        aria-hidden="true"
      ></div>

      <!-- Radial glow behind mockup -->
      <div
        data-hero-glow
        class="absolute right-[-5%] top-[10%] w-[700px] h-[700px] pointer-events-none"
        style="background: radial-gradient(ellipse at center, rgba(35,78,204,0.18) 0%, transparent 65%); border-radius: 50%;"
        aria-hidden="true"
      ></div>

      <!-- Secondary glow left -->
      <div
        class="absolute left-[-10%] bottom-0 w-[400px] h-[400px] pointer-events-none"
        style="background: radial-gradient(ellipse at center, rgba(35,78,204,0.08) 0%, transparent 70%); border-radius: 50%;"
        aria-hidden="true"
      ></div>

      <!-- Content grid -->
      <div class="relative z-10 max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-8 items-center">

        <!-- ── Left: copy ───────────────────────────────────────── -->
        <div class="max-w-xl">

          <!-- Arabic badge -->
          <div
            data-h-badge
            class="inline-flex items-center gap-2.5 bg-white/[0.04] border border-white/[0.1] rounded-full px-4 py-2 mb-8"
          >
            <span class="w-1.5 h-1.5 rounded-full bg-brand-light animate-pulse"></span>
            <p class="arabic-text text-base text-brand-light leading-none" style="line-height:1.2;">
              وَقُل رَّبِّ زِدْنِي عِلْمًا
            </p>
            <span class="text-white/25 text-xs font-medium hidden sm:inline">Quran 20:114</span>
          </div>

          <!-- Headline -->
          <h1 class="font-black tracking-tight leading-[0.95] text-white mb-6" style="font-size: clamp(2.8rem, 6vw, 5rem);">
            <span data-h-line class="block">Structured</span>
            <span data-h-line class="block" style="background: linear-gradient(135deg, #ffffff 30%, #3d65e8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Islamic</span>
            <span data-h-line class="block">Learning.</span>
          </h1>

          <!-- Sub -->
          <p
            data-h-sub
            class="text-white/50 leading-relaxed mb-10 max-w-md"
            style="font-size: clamp(1rem, 1.8vw, 1.2rem);"
          >
            {{ t('home.heroSub') }}
          </p>

          <!-- CTAs -->
          <div class="flex flex-col sm:flex-row gap-3">
            <RouterLink
              data-h-cta
              to="/learn"
              class="inline-flex items-center justify-center gap-2 bg-brand hover:bg-brand-dark text-white
                     px-6 py-3.5 rounded-xl font-semibold text-base transition-all duration-200
                     shadow-lg shadow-brand/30 hover:shadow-brand/50 hover:-translate-y-0.5"
            >
              <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
              {{ t('home.heroCta1') }}
            </RouterLink>
            <a
              data-h-cta
              href="https://github.com/mohhomadfarman/Tadabbur"
              target="_blank" rel="noopener noreferrer"
              class="inline-flex items-center justify-center gap-2 border border-white/15 hover:border-white/35 hover:bg-white/5
                     text-white/70 hover:text-white px-6 py-3.5 rounded-xl font-semibold text-base transition-all duration-200"
            >
              <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
              {{ t('home.heroCta2') }}
            </a>
          </div>

        </div>

        <!-- ── Right: app mockup ────────────────────────────────── -->
        <div data-h-mockup class="relative">
          <!-- Glow behind frame -->
          <div class="absolute -inset-4 sm:-inset-8 rounded-3xl pointer-events-none"
               style="background: radial-gradient(ellipse at 60% 40%, rgba(35,78,204,0.2) 0%, transparent 70%);"
               aria-hidden="true"></div>

          <!-- Browser frame -->
          <div class="relative rounded-2xl overflow-hidden shadow-2xl shadow-black/60"
               style="border: 1px solid rgba(255,255,255,0.08); background: #0d0d12;">

            <!-- Chrome bar -->
            <div class="flex items-center gap-3 px-4 py-2.5 border-b"
                 style="background:#131318; border-color:rgba(255,255,255,0.06);">
              <div class="flex gap-1.5 shrink-0">
                <span class="w-3 h-3 rounded-full" style="background:#ff5f57;"></span>
                <span class="w-3 h-3 rounded-full" style="background:#febc2e;"></span>
                <span class="w-3 h-3 rounded-full" style="background:#28c840;"></span>
              </div>
              <div class="flex-1 rounded-md px-3 py-1 text-[11px] font-mono"
                   style="background:#0a0a0f; color:rgba(255,255,255,0.25);">
                tadabbur.org/learn
              </div>
              <div class="w-5 shrink-0"></div>
            </div>

            <!-- App header -->
            <div class="flex items-center justify-between px-4 py-2.5 border-b"
                 style="background:#0e0e14; border-color:rgba(255,255,255,0.05);">
              <span class="text-white text-sm font-bold">Tadabbur</span>
              <div class="hidden sm:flex gap-5 text-xs" style="color:rgba(255,255,255,0.35);">
                <span style="color:rgba(255,255,255,0.75);">Learn</span>
                <span>Dashboard</span>
              </div>
              <div class="text-xs text-white font-semibold px-2.5 py-1 rounded-lg"
                   style="background:#234ecc;">Start Free</div>
            </div>

            <!-- App body -->
            <div class="p-4" style="background:#09090f;">

              <!-- Page heading -->
              <div class="flex items-center justify-between mb-3">
                <p class="text-xs font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.5);">
                  Islamic Curriculum
                </p>
                <p class="text-[10px]" style="color:rgba(255,255,255,0.2);">3 tracks available</p>
              </div>

              <!-- Track cards -->
              <div class="grid grid-cols-3 gap-2 mb-3">

                <div data-hero-track-card class="rounded-xl p-3" style="background:rgba(35,78,204,0.1); border:1px solid rgba(35,78,204,0.25);">
                  <div class="mb-1.5">
                    <svg class="w-4 h-4 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                  </div>
                  <p class="text-xs font-semibold leading-tight mb-0.5" style="color:rgba(255,255,255,0.9);">Quran Sciences</p>
                  <p class="text-[10px] mb-2" style="color:rgba(255,255,255,0.3);">12 subjects</p>
                  <div class="w-full rounded-full h-1" style="background:rgba(255,255,255,0.06);">
                    <div data-hero-progress class="h-1 rounded-full" style="width:0%;background:#234ecc;"></div>
                  </div>
                </div>

                <div data-hero-track-card class="rounded-xl p-3" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                  <div class="mb-1.5">
                    <svg class="w-4 h-4 text-yellow-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0012 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 01-2.031.352 5.988 5.988 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0l2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 01-2.031.352 5.989 5.989 0 01-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971z"/></svg>
                  </div>
                  <p class="text-xs font-semibold leading-tight mb-0.5" style="color:rgba(255,255,255,0.9);">Islamic Fiqh</p>
                  <p class="text-[10px] mb-2" style="color:rgba(255,255,255,0.3);">8 subjects</p>
                  <div class="w-full rounded-full h-1" style="background:rgba(255,255,255,0.06);"></div>
                </div>

                <div data-hero-track-card class="rounded-xl p-3" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                  <div class="mb-1.5">
                    <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"/></svg>
                  </div>
                  <p class="text-xs font-semibold leading-tight mb-0.5" style="color:rgba(255,255,255,0.9);">Aqeedah</p>
                  <p class="text-[10px] mb-2" style="color:rgba(255,255,255,0.3);">6 subjects</p>
                  <div class="w-full rounded-full h-1" style="background:rgba(255,255,255,0.06);"></div>
                </div>

              </div>

              <!-- Recent lesson -->
              <div data-hero-lesson-row class="rounded-xl p-3" style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.04);">
                <p class="text-[10px] uppercase tracking-wider font-medium mb-2" style="color:rgba(255,255,255,0.25);">
                  Continue Learning
                </p>
                <div class="flex items-center gap-2.5">
                  <div class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0"
                       style="background:rgba(35,78,204,0.2); color:#3d65e8;">3</div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs font-medium truncate" style="color:rgba(255,255,255,0.8);">Sources of Islamic Law</p>
                    <p class="text-[10px]" style="color:rgba(255,255,255,0.25);">Lesson 3 of 12 · 15 min</p>
                  </div>
                  <div class="w-5 h-5 rounded-full shrink-0 flex items-center justify-center"
                       style="background:rgba(35,78,204,0.2);">
                    <svg class="w-2.5 h-2.5" style="color:#3d65e8;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"/>
                    </svg>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Floating badge -->
          <div data-hero-badge-success class="absolute -bottom-4 -left-4 sm:-bottom-5 sm:-left-6 bg-emerald-900/80 backdrop-blur-sm border border-emerald-500/30 rounded-xl px-3 py-2 shadow-xl hidden sm:block">
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shrink-0"></div>
              <p class="text-emerald-300 text-xs font-medium">Lesson completed</p>
            </div>
          </div>

          <!-- Floating streak badge -->
          <div data-hero-badge-streak class="absolute -top-3 -right-3 sm:-top-4 sm:-right-4 bg-[#1a1a20] border border-white/10 rounded-xl px-3 py-2 shadow-xl hidden sm:block">
            <div class="flex items-center gap-1.5">
              <svg class="w-4 h-4 text-orange-400" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248ZM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1A5.99 5.99 0 0112 12.75a.75.75 0 01.75.75v.008l-.001.008a3.75 3.75 0 013.001 2.734Z" clip-rule="evenodd"/>
              </svg>
              <div>
                <p class="text-white text-xs font-bold leading-none">12 day</p>
                <p class="text-white/40 text-[10px] mt-0.5">streak</p>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Scroll hint -->
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-40">
        <span class="text-[10px] tracking-[0.2em] uppercase text-white font-medium">{{ t('home.heroScrollHint') }}</span>
        <svg class="w-4 h-4 text-white bounce-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 2 — STATS BAR                                         -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section
      data-stats-section
      class="border-y"
      style="background:#040408; border-color:rgba(255,255,255,0.06);"
    >
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4">
          <div
            v-for="(item, i) in heroStats"
            :key="item.label"
            data-stat-item
            class="py-7 px-6 text-center border-b md:border-b-0"
            style="border-color:rgba(255,255,255,0.06);"
            :class="[i % 2 === 0 ? 'border-r' : '', i < heroStats.length - 1 ? 'md:border-r' : '']"
          >
            <p class="text-2xl sm:text-3xl font-black text-white mb-1">{{ item.value }}</p>
            <p class="text-[11px] font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.35);">{{ item.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 3 — BENTO FEATURES                                    -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section class="py-24 sm:py-32 px-4" style="background:#020205;">
      <div class="max-w-7xl mx-auto">

        <!-- Section header -->
        <div class="text-center mb-14 max-w-2xl mx-auto">
          <p data-reveal class="section-eyebrow text-brand-light mb-4">
            <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
            {{ t('home.diffBadge') }}
            <span class="w-4 h-px bg-brand-light inline-block align-middle ms-2"></span>
          </p>
          <h2 data-reveal class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white leading-tight mb-4">
            {{ t('home.diffTitle') }}
          </h2>
          <p data-reveal class="text-white/40 text-lg">{{ t('home.diffSub') }}</p>
        </div>

        <!-- Bento grid -->
        <div data-bento-grid class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-3 sm:gap-4">

          <!-- Card 1: Structured Curriculum (large) -->
          <div
            data-bento-card
            class="bento-card lg:col-span-7 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(35,78,204,0.15);">
              <svg class="w-6 h-6" style="color:#3d65e8;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
            </div>
            <h3 class="text-white text-xl font-bold mb-2">{{ t('home.diff1Title') }}</h3>
            <p class="text-white/40 text-sm leading-relaxed mb-6">{{ t('home.diff1Desc') }}</p>
            <!-- Hierarchy tree visual -->
            <div class="mt-auto rounded-xl p-4 space-y-2" style="background:rgba(0,0,0,0.3); border:1px solid rgba(255,255,255,0.05);">
              <div class="flex items-center gap-2">
                <div class="w-5 h-5 rounded flex items-center justify-center shrink-0" style="background:rgba(35,78,204,0.3);"><svg class="w-3 h-3 text-brand-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20"/></svg></div>
                <span class="text-xs text-white/60 font-medium">Track: Quran Sciences</span>
              </div>
              <div class="flex items-center gap-2 ms-5">
                <div class="w-1 h-1 rounded-full shrink-0" style="background:rgba(255,255,255,0.2);"></div>
                <span class="text-xs text-white/35">Subject: Usul al-Tafsir</span>
              </div>
              <div class="flex items-center gap-2 ms-10">
                <div class="w-4 h-4 rounded flex items-center justify-center shrink-0" style="background:rgba(35,78,204,0.2);"><svg class="w-2.5 h-2.5 text-brand-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg></div>
                <span class="text-xs text-white/25">Lesson 1: Introduction</span>
              </div>
              <div class="flex items-center gap-2 ms-10">
                <div class="w-4 h-4 rounded flex items-center justify-center shrink-0" style="background:rgba(255,255,255,0.04);"><svg class="w-2.5 h-2.5 text-white/20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg></div>
                <span class="text-xs text-white/20">Lesson 2: Sources</span>
              </div>
            </div>
          </div>

          <!-- Card 2: Scholar Verified (narrow) -->
          <div
            data-bento-card
            class="bento-card lg:col-span-5 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(5,150,105,0.15);">
              <svg class="w-6 h-6" style="color:#10b981;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>
            </div>
            <h3 class="text-white text-xl font-bold mb-2">{{ t('home.diff2Title') }}</h3>
            <p class="text-white/40 text-sm leading-relaxed mb-6">{{ t('home.diff2Desc') }}</p>
            <!-- Trust badges -->
            <div class="mt-auto space-y-2">
              <div class="flex items-center gap-2.5 rounded-lg px-3 py-2.5" style="background:rgba(5,150,105,0.08); border:1px solid rgba(5,150,105,0.15);">
                <div class="w-2 h-2 rounded-full bg-emerald-400 shrink-0"></div>
                <span class="text-xs text-emerald-300/80 font-medium">Scholar-reviewed content</span>
              </div>
              <div class="flex items-center gap-2.5 rounded-lg px-3 py-2.5" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                <div class="w-2 h-2 rounded-full shrink-0" style="background:rgba(255,255,255,0.2);"></div>
                <span class="text-xs text-white/30 font-medium">Source citations included</span>
              </div>
              <div class="flex items-center gap-2.5 rounded-lg px-3 py-2.5" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                <div class="w-2 h-2 rounded-full shrink-0" style="background:rgba(255,255,255,0.2);"></div>
                <span class="text-xs text-white/30 font-medium">No unverified opinions</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Active Learning (narrow) -->
          <div
            data-bento-card
            class="bento-card lg:col-span-5 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(124,58,237,0.15);">
              <svg class="w-6 h-6" style="color:#a78bfa;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
            </div>
            <h3 class="text-white text-xl font-bold mb-2">{{ t('home.diff3Title') }}</h3>
            <p class="text-white/40 text-sm leading-relaxed mb-6">{{ t('home.diff3Desc') }}</p>
            <!-- Mini quiz mockup -->
            <div class="mt-auto rounded-xl overflow-hidden" style="border:1px solid rgba(255,255,255,0.07);">
              <div class="px-4 py-3" style="background:rgba(0,0,0,0.3);">
                <p class="text-[10px] uppercase tracking-widest text-white/30 font-semibold mb-1">Quick Check</p>
                <p class="text-xs text-white/60 leading-snug">What are the four main sources of Islamic law?</p>
              </div>
              <div class="p-3 space-y-1.5" style="background:rgba(0,0,0,0.15);">
                <div class="flex items-center gap-2 rounded-lg px-3 py-2" style="background:rgba(5,150,105,0.12); border:1px solid rgba(5,150,105,0.3);">
                  <span class="text-[10px] font-bold text-emerald-400">A.</span>
                  <span class="text-[10px] text-emerald-300">Quran, Sunnah, Ijma, Qiyas</span>
                  <svg class="w-3 h-3 text-emerald-400 ms-auto shrink-0" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                </div>
                <div class="flex items-center gap-2 rounded-lg px-3 py-2" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05);">
                  <span class="text-[10px] font-bold text-white/25">B.</span>
                  <span class="text-[10px] text-white/25">Quran, Hadith, Fatwa, Ijtihad</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 4: Arabic + RTL (large) -->
          <div
            data-bento-card
            class="bento-card lg:col-span-7 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(35,78,204,0.15);">
              <svg class="w-6 h-6" style="color:#3d65e8;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
            </div>
            <div class="flex items-start justify-between gap-4 mb-2">
              <h3 class="text-white text-xl font-bold">Arabic & RTL Support</h3>
              <div class="flex gap-1.5 shrink-0">
                <span class="text-xs px-2 py-0.5 rounded-full" style="background:rgba(35,78,204,0.15); color:#3d65e8; border:1px solid rgba(35,78,204,0.25);">EN</span>
                <span class="text-xs px-2 py-0.5 rounded-full" style="background:rgba(35,78,204,0.25); color:#ffffff; border:1px solid rgba(35,78,204,0.4);">AR</span>
              </div>
            </div>
            <p class="text-white/40 text-sm leading-relaxed mb-6">
              Full Arabic Quranic text rendering, RTL UI, and bilingual translations — automatically switching with your language preference.
            </p>
            <!-- Arabic verse preview -->
            <div class="mt-auto rounded-xl p-4" style="background:rgba(5,150,105,0.06); border:1px solid rgba(5,150,105,0.15);">
              <p class="arabic-text text-2xl sm:text-3xl leading-loose mb-3" style="color:rgba(255,255,255,0.85);">
                وَقُل رَّبِّ زِدْنِي عِلْمًا
              </p>
              <p class="text-sm text-white/40 italic">"My Lord, increase me in knowledge."</p>
              <p class="text-xs mt-1" style="color:rgba(5,150,105,0.7);">Surah Ta-Ha 20:114</p>
            </div>
          </div>

          <!-- Card 5: Progress Tracking -->
          <div
            data-bento-card
            class="bento-card lg:col-span-6 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(35,78,204,0.15);">
              <svg class="w-6 h-6" style="color:#3d65e8;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
            </div>
            <h3 class="text-white text-xl font-bold mb-2">Progress Tracking</h3>
            <p class="text-white/40 text-sm leading-relaxed mb-6">
              Streaks, completion badges, and per-subject progress bars keep you accountable.
            </p>
            <!-- Progress bars mockup -->
            <div class="mt-auto space-y-3">
              <div>
                <div class="flex justify-between mb-1.5">
                  <span class="text-[11px] text-white/40">Quran Sciences</span>
                  <span class="text-[11px] font-bold" style="color:#3d65e8;">34%</span>
                </div>
                <div class="w-full rounded-full h-1.5" style="background:rgba(255,255,255,0.06);">
                  <div class="h-1.5 rounded-full" style="width:34%; background:linear-gradient(90deg, #234ecc, #3d65e8);"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1.5">
                  <span class="text-[11px] text-white/40">Islamic Fiqh</span>
                  <span class="text-[11px] font-bold text-white/30">12%</span>
                </div>
                <div class="w-full rounded-full h-1.5" style="background:rgba(255,255,255,0.06);">
                  <div class="h-1.5 rounded-full" style="width:12%; background:rgba(35,78,204,0.5);"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1.5">
                  <span class="text-[11px] text-white/40">Seerah</span>
                  <span class="text-[11px] font-bold text-white/20">0%</span>
                </div>
                <div class="w-full rounded-full h-1.5" style="background:rgba(255,255,255,0.06);"></div>
              </div>
            </div>
          </div>

          <!-- Card 6: Free + Open Source -->
          <div
            data-bento-card
            class="bento-card lg:col-span-6 rounded-2xl p-6 sm:p-7 flex flex-col"
            style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
          >
            <div class="icon-circle mb-5" style="background:rgba(35,78,204,0.15);">
              <svg class="w-6 h-6" style="color:#3d65e8;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>
            </div>
            <h3 class="text-white text-xl font-bold mb-2">{{ t('home.diff4Title') }}</h3>
            <p class="text-white/40 text-sm leading-relaxed mb-6">{{ t('home.diff4Desc') }}</p>
            <!-- Badges -->
            <div class="mt-auto flex flex-wrap gap-2">
              <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full" style="background:rgba(35,78,204,0.12); color:#3d65e8; border:1px solid rgba(35,78,204,0.25);">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
                Open Source
              </span>
              <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full text-white/40" style="border:1px solid rgba(255,255,255,0.08);">
                No Paywalls
              </span>
              <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full text-white/40" style="border:1px solid rgba(255,255,255,0.08);">
                No Ads
              </span>
              <span class="inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full text-white/40" style="border:1px solid rgba(255,255,255,0.08);">
                Free Forever
              </span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 4 — LESSON READER SHOWCASE                            -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section data-reader-section class="py-24 sm:py-32 px-4" style="background:#040408;">
      <div class="max-w-6xl mx-auto">

        <!-- Header -->
        <div class="text-center mb-14">
          <p data-reveal class="section-eyebrow text-brand-light mb-4">
            <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
            The Experience
            <span class="w-4 h-px bg-brand-light inline-block align-middle ms-2"></span>
          </p>
          <h2 data-reveal class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white leading-tight mb-4">
            Designed for deep reading.
          </h2>
          <p data-reveal class="text-white/40 text-lg max-w-xl mx-auto">
            Every lesson is crafted to help you read slowly, understand deeply, and retain what matters.
          </p>
        </div>

        <!-- Lesson reader mockup -->
        <div data-reveal class="relative mx-auto max-w-2xl">
          <div class="absolute -inset-6 sm:-inset-10 rounded-3xl pointer-events-none"
               style="background: radial-gradient(ellipse at center, rgba(35,78,204,0.12) 0%, transparent 65%);"
               aria-hidden="true"></div>

          <div class="relative rounded-2xl overflow-hidden shadow-2xl shadow-black/70"
               style="border:1px solid rgba(255,255,255,0.08); background:#0a0a0f;">

            <!-- Progress bar -->
            <div class="h-1" style="background:rgba(255,255,255,0.04);">
              <div data-reader-progress class="h-full" style="width:0%; background:linear-gradient(90deg,#234ecc,#3d65e8);"></div>
            </div>

            <!-- Lesson header -->
            <div class="px-6 pt-6 pb-4 border-b" style="border-color:rgba(255,255,255,0.06);">
              <p class="text-[10px] uppercase tracking-widest font-semibold mb-3" style="color:rgba(255,255,255,0.3);">
                Quran Sciences · Lesson 3 of 12
              </p>
              <h3 class="text-white text-lg sm:text-xl font-bold leading-snug">Sources of Islamic Law</h3>
              <p class="text-xs mt-1.5 flex items-center gap-3" style="color:rgba(255,255,255,0.3);">
                <span>15 min read</span>
                <span>·</span>
                <span style="color:#10b981;" class="inline-flex items-center gap-1">
                  <svg class="w-3 h-3 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12.75l6 6 9-13.5"/></svg>
                  Verified by scholar
                </span>
              </p>
            </div>

            <!-- Content -->
            <div class="p-6 space-y-5">

              <!-- Text paragraph (skeleton lines) -->
              <div class="space-y-2">
                <div data-reader-line class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.06); width:100%;"></div>
                <div data-reader-line class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.06); width:92%;"></div>
                <div data-reader-line class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.06); width:78%;"></div>
              </div>

              <!-- Verse block -->
              <div data-reader-verse class="rounded-r-2xl ps-5 py-4 pe-4" style="border-left: 4px solid #10b981; background:rgba(5,150,105,0.08);">
                <p class="arabic-text text-xl sm:text-2xl leading-loose mb-2" style="color:rgba(255,255,255,0.8);">
                  وَمَا آتَاكُمُ الرَّسُولُ فَخُذُوهُ
                </p>
                <p class="text-xs italic" style="color:rgba(16,185,129,0.7);">"Whatever the Messenger gives you, take it." — Al-Hashr 59:7</p>
              </div>

              <!-- More text -->
              <div class="space-y-2">
                <div data-reader-line class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.05); width:100%;"></div>
                <div data-reader-line class="h-2.5 rounded-full" style="background:rgba(255,255,255,0.05); width:88%;"></div>
              </div>

              <!-- Quiz element -->
              <div data-reader-quiz class="rounded-xl overflow-hidden" style="border:1px solid rgba(255,255,255,0.07);">
                <div class="px-4 py-3" style="background:rgba(255,255,255,0.03);">
                  <p class="text-[10px] uppercase tracking-widest text-white/30 font-semibold mb-1">Quick Check</p>
                  <p class="text-xs text-white/50">Which is considered the second source of Islamic law?</p>
                </div>
                <div class="grid grid-cols-2 gap-1.5 p-3" style="background:rgba(0,0,0,0.2);">
                  <div class="text-[10px] px-2.5 py-2 rounded-lg text-white/25" style="border:1px solid rgba(255,255,255,0.05);">Ijma</div>
                  <div
                    class="text-[10px] px-2.5 py-2 rounded-lg flex items-center justify-center gap-1 transition-all duration-500"
                    :class="quizAnswered ? 'text-emerald-300' : 'text-white/25'"
                    :style="quizAnswered
                      ? 'border:1px solid rgba(5,150,105,0.3); background:rgba(5,150,105,0.1);'
                      : 'border:1px solid rgba(255,255,255,0.05);'"
                  >
                    Sunnah
                    <svg v-if="quizAnswered" class="w-2.5 h-2.5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 12.75l6 6 9-13.5"/></svg>
                  </div>
                  <div class="text-[10px] px-2.5 py-2 rounded-lg text-white/25" style="border:1px solid rgba(255,255,255,0.05);">Qiyas</div>
                  <div class="text-[10px] px-2.5 py-2 rounded-lg text-white/25" style="border:1px solid rgba(255,255,255,0.05);">Istihsan</div>
                </div>
              </div>

            </div>

            <!-- Bottom nav -->
            <div class="px-6 py-4 border-t grid grid-cols-2 gap-3" style="border-color:rgba(255,255,255,0.06);">
              <div class="rounded-xl p-3 text-center" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06);">
                <p class="text-[10px] text-white/25">← Previous</p>
                <p class="text-xs text-white/40 mt-0.5 truncate">History of Tafsir</p>
              </div>
              <div class="rounded-xl p-3 text-center" style="background:rgba(35,78,204,0.15); border:1px solid rgba(35,78,204,0.25);">
                <p class="text-[10px] text-brand-light">Next →</p>
                <p class="text-xs text-white/60 mt-0.5 truncate">Ijma & Qiyas</p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 5 — THE PROBLEM                                       -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28 px-4" style="background:#020205;">
      <div class="max-w-6xl mx-auto">

        <!-- Top: stat + headline -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-20 items-start mb-12">
          <div data-reveal>
            <p class="section-eyebrow text-brand-light mb-6">
              <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
              {{ t('home.problemBadge') }}
            </p>
            <p class="font-black leading-none text-white tracking-tighter mb-4" style="font-size:clamp(3.5rem,8vw,6rem);">
              1.8<span class="text-brand-light">B</span>
            </p>
            <p class="text-white/35 leading-relaxed max-w-xs" style="font-size:1rem;">
              Muslims worldwide. Zero platforms actually worth their time.
            </p>
            <div class="mt-8 w-12 h-px bg-brand"></div>
          </div>

          <div data-reveal class="lg:pt-4">
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight text-white mb-5">
              {{ t('home.problemTitle') }}
            </h2>
            <p class="text-white/35 leading-relaxed">{{ t('home.problemSub') }}</p>
          </div>
        </div>

        <!-- Pain points -->
        <div class="space-y-3">
          <div
            v-for="(pain, i) in painPoints"
            :key="pain.key"
            data-reveal
            class="group flex items-start gap-4 sm:gap-6 rounded-2xl p-5 sm:p-6 transition-all duration-300"
            style="background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.06);"
            :style="{ transitionDelay: (i * 0.05) + 's' }"
          >
            <div class="icon-circle shrink-0" style="background:rgba(239,68,68,0.1);">
              <svg class="w-5 h-5 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" v-html="pain.iconPath"></svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-white text-base sm:text-lg mb-1">{{ t(`home.${pain.key}Title`) }}</h3>
              <p class="text-white/40 leading-relaxed text-sm sm:text-base">{{ t(`home.${pain.key}Desc`) }}</p>
            </div>
            <span class="shrink-0 font-black text-2xl sm:text-4xl xl:text-5xl select-none" style="color:rgba(239,68,68,0.12);">
              {{ String(i + 1).padStart(2, '0') }}
            </span>
          </div>
        </div>

      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 6 — ROADMAP                                           -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28 px-4" style="background:#040408;">
      <div class="max-w-6xl mx-auto">

        <div class="text-center mb-14">
          <p data-reveal class="section-eyebrow text-brand-light mb-4">
            <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
            {{ t('home.roadmapBadge') }}
          </p>
          <h2 data-reveal class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white leading-tight mb-4">
            {{ t('home.roadmapTitle') }}
          </h2>
          <p data-reveal class="text-white/40 text-lg">{{ t('home.roadmapSub') }}</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(phase, i) in phases"
            :key="phase.key"
            data-reveal
            class="relative rounded-2xl p-6 transition-all duration-300"
            :style="phase.current
              ? 'background:rgba(35,78,204,0.08); border:1px solid rgba(35,78,204,0.3); box-shadow: 0 0 40px rgba(35,78,204,0.08);'
              : 'background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);'"
          >
            <div class="flex items-center justify-between mb-5">
              <span
                class="text-[10px] font-bold uppercase tracking-widest px-3 py-1.5 rounded-full"
                :style="phase.current
                  ? 'background:#234ecc; color:#fff;'
                  : 'background:rgba(255,255,255,0.06); color:rgba(255,255,255,0.3);'"
              >
                {{ phase.current ? t('home.roadmapCurrentBadge') : t('home.roadmapPlannedBadge') }}
              </span>
              <span class="text-2xl font-black select-none" style="color:rgba(255,255,255,0.06);">{{ String(i + 1).padStart(2, '0') }}</span>
            </div>
            <div class="icon-circle mb-4" :style="phase.current ? 'background:rgba(35,78,204,0.2);' : 'background:rgba(255,255,255,0.04);'">
              <svg class="w-5 h-5" :style="phase.current ? 'color:#3d65e8;' : 'color:rgba(255,255,255,0.2);'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" v-html="phase.iconPath"></svg>
            </div>
            <h3 class="font-bold text-lg mb-2" :style="phase.current ? 'color:#3d65e8;' : 'color:rgba(255,255,255,0.7);'">
              {{ t(`home.${phase.key}Title`) }}
            </h3>
            <p class="text-sm leading-relaxed" style="color:rgba(255,255,255,0.35);">{{ t(`home.${phase.key}Desc`) }}</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 7 — WHO IT'S FOR                                      -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28 px-4" style="background:#020205;">
      <div class="max-w-6xl mx-auto">

        <div class="text-center mb-14">
          <p data-reveal class="section-eyebrow text-brand-light mb-4">
            <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
            {{ t('home.audienceBadge') }}
          </p>
          <h2 data-reveal class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-white leading-tight">
            {{ t('home.audienceTitle') }}
          </h2>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(item, i) in audience"
            :key="item.key"
            data-reveal
            class="group relative rounded-2xl p-6 sm:p-7 overflow-hidden transition-all duration-300 hover:-translate-y-1"
            style="background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07);"
          >
            <div
              class="absolute left-0 top-0 bottom-0 w-0.5 rounded-full transition-all duration-300"
              :style="`background:${item.accent};`"
            ></div>
            <div class="icon-circle mb-5 ms-2" :style="`background:${item.bgColor};`">
              <svg class="w-5 h-5" :style="`color:${item.accent};`" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" v-html="item.iconPath"></svg>
            </div>
            <h3 class="font-bold text-base sm:text-lg mb-2 ms-2 transition-colors duration-200" :style="`color:${item.accent};`">
              {{ t(`home.${item.key}Title`) }}
            </h3>
            <p class="text-sm leading-relaxed ms-2" style="color:rgba(255,255,255,0.35);">{{ t(`home.${item.key}Desc`) }}</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 8 — OPEN SOURCE                                       -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section class="py-20 sm:py-28 px-4 relative overflow-hidden" style="background:#040408;">

      <!-- Decorative Arabic -->
      <div class="absolute inset-0 flex items-center justify-end pe-8 pointer-events-none select-none" aria-hidden="true">
        <span class="arabic-text font-bold float-arabic-slow" style="font-size:clamp(4rem,20vw,18rem); color:rgba(255,255,255,0.018);">علم</span>
      </div>

      <div class="relative z-10 max-w-6xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center">

          <!-- Left: mission -->
          <div>
            <p data-reveal class="section-eyebrow text-brand-light mb-6">
              <span class="w-4 h-px bg-brand-light inline-block align-middle me-2"></span>
              {{ t('home.openSourceBadge') }}
            </p>
            <h2 data-reveal class="text-3xl sm:text-4xl lg:text-5xl font-black leading-tight text-white mb-6">
              {{ t('home.openSourceTitle') }}
            </h2>
            <p data-reveal class="text-white/40 leading-relaxed mb-10">{{ t('home.openSourceSub') }}</p>
            <div data-reveal class="flex flex-col sm:flex-row gap-3">
              <a
                href="https://github.com/mohhomadfarman/Tadabbur"
                target="_blank" rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-2.5 bg-brand hover:bg-brand-dark text-white px-6 py-3.5 rounded-xl font-semibold transition-all duration-200 shadow-lg shadow-brand/30 hover:-translate-y-0.5"
              >
                <svg class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
                {{ t('home.ctaGithub') }}
              </a>
              <RouterLink
                to="/learn"
                class="inline-flex items-center justify-center border text-white/60 hover:text-white px-6 py-3.5 rounded-xl font-semibold transition-all duration-200"
                style="border-color:rgba(255,255,255,0.15);"
              >
                {{ t('home.ctaDocs') }}
              </RouterLink>
            </div>
          </div>

          <!-- Right: stats -->
          <div data-reveal class="space-y-3">
            <div
              v-for="stat in stats"
              :key="stat.labelKey"
              class="flex items-center gap-5 rounded-2xl px-5 py-5 transition-all duration-200"
              style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);"
            >
              <div class="icon-circle shrink-0" style="background:rgba(35,78,204,0.12);">
                <svg class="w-5 h-5 text-brand-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" v-html="stat.iconPath"></svg>
              </div>
              <div>
                <p class="text-2xl sm:text-3xl font-black text-white leading-none mb-1">{{ stat.value }}</p>
                <p class="text-[11px] font-semibold uppercase tracking-widest" style="color:rgba(255,255,255,0.3);">{{ t(`home.${stat.labelKey}`) }}</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- SECTION 9 — FINAL CTA                                         -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <section
      class="relative py-24 sm:py-36 px-4 overflow-hidden text-white"
      style="background: linear-gradient(135deg, #0a0f2e 0%, #162060 40%, #1a3ba8 70%, #234ecc 100%);"
    >
      <!-- Grid pattern -->
      <div class="absolute inset-0 pointer-events-none" style="background-image:linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px); background-size:40px 40px;" aria-hidden="true"></div>
      <!-- Glow -->
      <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px] pointer-events-none blur-3xl" style="background:radial-gradient(ellipse, rgba(61,101,232,0.5) 0%, transparent 70%);" aria-hidden="true"></div>

      <div class="relative z-10 max-w-2xl mx-auto text-center">

        <div data-reveal class="mb-8">
          <p class="arabic-center text-3xl sm:text-4xl text-white/70 mb-2">{{ t('home.finalDecorVerse') }}</p>
          <p class="text-white/30 text-sm">{{ t('home.finalVerseRef') }}</p>
        </div>

        <h2 data-reveal class="text-4xl sm:text-5xl lg:text-6xl font-black leading-tight mb-4 tracking-tight">
          {{ t('home.finalTitle') }}
          <span class="text-white/85 italic">{{ t('home.finalTitleAccent') }}</span>
        </h2>

        <p data-reveal class="text-white/55 text-lg leading-relaxed max-w-lg mx-auto mb-12">
          {{ t('home.finalSub') }}
        </p>

        <div data-reveal class="flex flex-col sm:flex-row gap-4 justify-center">
          <RouterLink
            v-if="!auth.isLoggedIn"
            to="/register"
            class="bg-white hover:bg-gray-50 text-brand px-8 py-4 rounded-xl font-bold text-lg transition-all duration-200 shadow-lg hover:-translate-y-0.5 hover:shadow-xl"
          >
            {{ t('home.finalCta1') }}
          </RouterLink>
          <RouterLink
            to="/learn"
            :class="auth.isLoggedIn
              ? 'bg-white hover:bg-gray-50 text-brand shadow-lg hover:shadow-xl'
              : 'border border-white/25 hover:border-white/50 hover:bg-white/8 text-white/80 hover:text-white'"
            class="px-8 py-4 rounded-xl font-bold text-lg transition-all duration-200 hover:-translate-y-0.5"
          >
            {{ t('home.finalCta2') }}
          </RouterLink>
        </div>

      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════════ -->
    <!-- FOOTER                                                        -->
    <!-- ══════════════════════════════════════════════════════════════ -->
    <footer style="background:#020205; border-top:1px solid rgba(255,255,255,0.06);">
      <div class="max-w-7xl mx-auto px-4 py-12">

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">

          <!-- Brand column -->
          <div class="sm:col-span-2 lg:col-span-1">
            <div class="flex items-center mb-4">
              <img src="/logo-rounded.png" alt="Tadabbur" class="h-14 w-auto rounded-lg" />
            </div>
            <p class="text-sm leading-relaxed mb-5" style="color:rgba(255,255,255,0.3);">
              Structured Islamic learning for the global Ummah. Free forever.
            </p>
            <a
              href="https://github.com/mohhomadfarman/Tadabbur"
              target="_blank" rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-xs font-semibold px-3 py-2 rounded-lg transition-all duration-200"
              style="color:rgba(255,255,255,0.4); border:1px solid rgba(255,255,255,0.08);"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
              Open Source
            </a>
          </div>

          <!-- Platform links -->
          <div>
            <p class="text-xs font-bold uppercase tracking-widest mb-5" style="color:rgba(255,255,255,0.25);">Platform</p>
            <ul class="space-y-3">
              <li v-for="link in footerPlatform" :key="link.label">
                <RouterLink :to="link.to" class="text-sm transition-colors duration-200" style="color:rgba(255,255,255,0.4);" @mouseover="$event.target.style.color='rgba(255,255,255,0.8)'" @mouseleave="$event.target.style.color='rgba(255,255,255,0.4)'">
                  {{ link.label }}
                </RouterLink>
              </li>
            </ul>
          </div>

          <!-- Community links -->
          <div>
            <p class="text-xs font-bold uppercase tracking-widest mb-5" style="color:rgba(255,255,255,0.25);">Community</p>
            <ul class="space-y-3">
              <li v-for="link in footerCommunity" :key="link.label">
                <a :href="link.href" target="_blank" rel="noopener noreferrer" class="text-sm transition-colors duration-200" style="color:rgba(255,255,255,0.4);">{{ link.label }}</a>
              </li>
            </ul>
          </div>

          <!-- Legal links -->
          <div>
            <p class="text-xs font-bold uppercase tracking-widest mb-5" style="color:rgba(255,255,255,0.25);">Legal</p>
            <ul class="space-y-3">
              <li v-for="link in footerLegal" :key="link.label">
                <RouterLink
                  v-if="link.to"
                  :to="link.to"
                  class="text-sm transition-colors duration-200"
                  style="color:rgba(255,255,255,0.4);"
                  @mouseover="$event.target.style.color='rgba(255,255,255,0.8)'"
                  @mouseleave="$event.target.style.color='rgba(255,255,255,0.4)'"
                >{{ link.label }}</RouterLink>
                <a
                  v-else
                  :href="link.href"
                  target="_blank" rel="noopener noreferrer"
                  class="text-sm transition-colors duration-200"
                  style="color:rgba(255,255,255,0.4);"
                >{{ link.label }}</a>
              </li>
            </ul>
          </div>

        </div>

        <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8" style="border-top:1px solid rgba(255,255,255,0.06);">
          <p class="text-xs" style="color:rgba(255,255,255,0.2);">
            © {{ new Date().getFullYear() }} Tadabbur. Built with
            <svg style="color:#f87171;" class="w-3.5 h-3.5 inline shrink-0" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z"/></svg>
            for the Ummah.
          </p>
          <p class="arabic-text text-sm" style="color:rgba(255,255,255,0.2); line-height:1.4;">Developed By <a href="http://shapesky.net" target="_blank" rel="noopener ">shapesky.net</a></p>
        </div>

      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useSeo } from '@/composables/useSeo'

const quizAnswered = ref(false)

const { t } = useI18n()
const auth = useAuthStore()

useSeo({
  title:       'Tadabbur — Structured Islamic Learning for the Ummah',
  description: 'A rigorous, scholar-verified Islamic curriculum. Structured tracks from beginner to advanced. Free forever. Built for the Ummah.',
  url:         'https://tadabbur.org/',
})

// ── GSAP + Lenis refs ──────────────────────────────────────────────
let gsapCtx = null
let lenis   = null

// ── Static data ────────────────────────────────────────────────────

const heroStats = [
  { value: '1.8B', label: 'Muslims Worldwide' },
  { value: '6',    label: 'Learning Tracks'   },
  { value: '100%', label: 'Free Forever'       },
  { value: '∞',    label: 'Open Source'        },
]

const painPoints = [
  {
    key: 'pain1',
    iconPath: `<rect x="2" y="2" width="6" height="6" rx="1"/><rect x="16" y="2" width="6" height="6" rx="1"/><rect x="9" y="9" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/>`,
  },
  {
    key: 'pain2',
    iconPath: `<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>`,
  },
  {
    key: 'pain3',
    iconPath: `<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>`,
  },
]

const phases = [
  { key: 'phase1', current: true,  iconPath: `<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>` },
  { key: 'phase2', current: false, iconPath: `<circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>` },
  { key: 'phase3', current: false, iconPath: `<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>` },
  { key: 'phase4', current: false, iconPath: `<rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/>` },
  { key: 'phase5', current: false, iconPath: `<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>` },
  { key: 'phase6', current: false, iconPath: `<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>` },
]

const audience = [
  { key: 'audience1', accent: '#059669', bgColor: 'rgba(5,150,105,0.1)',  iconPath: `<path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2c-2.76 4-2.76 16 0 20"/><path d="M2 12h20"/>` },
  { key: 'audience2', accent: '#2563eb', bgColor: 'rgba(37,99,235,0.1)',  iconPath: `<circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>` },
  { key: 'audience3', accent: '#7c3aed', bgColor: 'rgba(124,58,237,0.1)', iconPath: `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>` },
  { key: 'audience4', accent: '#b45309', bgColor: 'rgba(180,83,9,0.1)',   iconPath: `<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>` },
  { key: 'audience5', accent: '#475569', bgColor: 'rgba(71,85,105,0.1)',  iconPath: `<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>` },
]

const stats = [
  { labelKey: 'statStars',        value: '0', iconPath: `<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>` },
  { labelKey: 'statContributors', value: '1', iconPath: `<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>` },
  { labelKey: 'statLanguages',    value: '2', iconPath: `<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>` },
]

const footerPlatform = [
  { label: 'Start Learning', to: '/learn' },
  { label: 'Library',        to: '/library' },
  { label: 'Videos',         to: '/videos' },
  { label: 'Dashboard',      to: '/dashboard' },
  { label: 'Register',       to: '/register' },
  { label: 'Login',          to: '/login' },
]

const footerCommunity = [
  { label: 'GitHub',      href: 'https://github.com/mohhomadfarman/Tadabbur' },
  { label: 'Contribute',  href: 'https://github.com/mohhomadfarman/Tadabbur/blob/main/CONTRIBUTING.md' },
  { label: 'Report a Bug',href: 'https://github.com/mohhomadfarman/Tadabbur/issues' },
]

const footerLegal = [
  { label: 'Privacy Policy',      to: '/privacy' },
  { label: 'Terms & Conditions',  to: '/terms' },
  { label: 'MIT License',         href: 'https://github.com/mohhomadfarman/Tadabbur/blob/main/LICENSE' },
]

// ── Lifecycle ──────────────────────────────────────────────────────
onMounted(async () => {
  // Dynamic imports — don't block initial render
  const [{ gsap }, { ScrollTrigger }, { default: Lenis }] = await Promise.all([
    import('gsap'),
    import('gsap/ScrollTrigger'),
    import('lenis'),
  ])

  gsap.registerPlugin(ScrollTrigger)

  // ── Lenis smooth scroll ──────────────────────────────────────────
  lenis = new Lenis({
    duration: 1.2,
    easing: t => 1 - Math.pow(1 - t, 4),
    smoothWheel: true,
  })

  lenis.on('scroll', ScrollTrigger.update)
  gsap.ticker.add(time => lenis.raf(time * 1000))
  gsap.ticker.lagSmoothing(0)

  // ── GSAP animations ──────────────────────────────────────────────
  gsapCtx = gsap.context(() => {

    // Hero entrance timeline
    const heroTL = gsap.timeline({ delay: 0.15 })
    heroTL
      .from('[data-h-badge]',  { y: -24, opacity: 0, duration: 0.55, ease: 'power2.out' })
      .from('[data-h-line]',   { y: 60, opacity: 0, stagger: 0.11, duration: 0.8, ease: 'power3.out' }, '-=0.3')
      .from('[data-h-sub]',    { y: 22, opacity: 0, duration: 0.65, ease: 'power2.out' }, '-=0.45')
      .from('[data-h-cta]',    { y: 20, opacity: 0, stagger: 0.1, duration: 0.5, ease: 'power2.out' }, '-=0.4')
      .from('[data-h-mockup]', { y: 70, opacity: 0, scale: 0.96, duration: 1.3, ease: 'power3.out' }, 0.25)

    // ── Hero mockup internal "live demo" animations ───────────────
    // Runs after mockup entrance completes (~1.7s from page load)
    const mockupTL = gsap.timeline({ delay: 1.9 })
    mockupTL
      .from('[data-hero-badge-streak]', {
        y: -20, opacity: 0, scale: 0.8, duration: 0.65, ease: 'back.out(1.8)',
      })
      .from('[data-hero-track-card]', {
        y: 10, opacity: 0, stagger: 0.1, duration: 0.45, ease: 'power2.out',
      }, '-=0.3')
      .to('[data-hero-progress]', {
        width: '34%', duration: 1.6, ease: 'power2.inOut',
      }, '-=0.1')
      .from('[data-hero-lesson-row]', {
        y: 10, opacity: 0, duration: 0.45, ease: 'power2.out',
      }, '-=1.3')
      .from('[data-hero-badge-success]', {
        y: 20, opacity: 0, scale: 0.8, duration: 0.65, ease: 'back.out(1.8)',
      }, '-=0.8')

    // Hero glow parallax
    gsap.to('[data-hero-glow]', {
      y: -120,
      scrollTrigger: {
        trigger: '[data-hero-section]',
        start: 'top top',
        end: 'bottom top',
        scrub: 2,
      },
    })

    // Stats bar
    ScrollTrigger.create({
      trigger: '[data-stats-section]',
      start: 'top 82%',
      once: true,
      onEnter: () => {
        gsap.from('[data-stat-item]', {
          y: 22, opacity: 0, stagger: 0.1, duration: 0.6, ease: 'power2.out',
        })
      },
    })

    // Bento cards stagger
    ScrollTrigger.create({
      trigger: '[data-bento-grid]',
      start: 'top 78%',
      once: true,
      onEnter: () => {
        gsap.from('[data-bento-card]', {
          y: 44, opacity: 0, stagger: 0.08, duration: 0.7, ease: 'power2.out',
        })
      },
    })

    // ── Lesson reader mockup "live demo" animations ───────────────
    ScrollTrigger.create({
      trigger: '[data-reader-section]',
      start: 'top 72%',
      once: true,
      onEnter: () => {
        const readerTL = gsap.timeline()
        readerTL
          .to('[data-reader-progress]', {
            width: '38%', duration: 2, ease: 'power2.out',
          })
          .from('[data-reader-line]', {
            scaleX: 0, transformOrigin: 'left center',
            stagger: 0.1, duration: 0.45, ease: 'power2.out',
          }, '-=1.7')
          .from('[data-reader-verse]', {
            x: 24, opacity: 0, duration: 0.7, ease: 'power2.out',
          }, '-=0.9')
          .from('[data-reader-quiz]', {
            y: 18, opacity: 0, duration: 0.6, ease: 'power2.out',
          }, '-=0.5')

        // Quiz answer selection fires ~2.4s after section enters view
        setTimeout(() => { quizAnswered.value = true }, 2400)
      },
    })

    // Generic [data-reveal] elements
    gsap.utils.toArray('[data-reveal]').forEach(el => {
      gsap.from(el, {
        y: 36, opacity: 0, duration: 0.8, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 87%', once: true },
      })
    })

  }, '.home-page')
})

onUnmounted(() => {
  gsapCtx?.revert()
  lenis?.destroy()
  quizAnswered.value = false
})
</script>

