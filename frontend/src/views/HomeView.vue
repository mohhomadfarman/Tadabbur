<template>
  <div>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 1 — HERO (kept, enhanced with slide animations)    -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section
      class="relative h-[100dvh] flex flex-col justify-center items-center
             bg-black text-white overflow-hidden px-4 pt-8"
    >
      <!-- Decorative calligraphy background -->
      <div
        class="absolute inset-0 flex items-center justify-center
                pointer-events-none select-none overflow-hidden"
        aria-hidden="true"
      >
        <span
          class="arabic-text font-bold text-white/[0.035] float-arabic leading-none whitespace-nowrap"
          style="font-size: clamp(8rem, 25vw, 22rem);"
        >
          {{ t('home.heroDecor') }}
        </span>
      </div>

      <!-- Animated radial glow -->
      <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
               w-[600px] h-[600px] rounded-full pointer-events-none glow-pulse"
        style="background: radial-gradient(circle, rgba(35,78,204,0.12) 0%, transparent 70%);"
        aria-hidden="true"
      ></div>

      <!-- Subtle grid overlay -->
      <div
        class="absolute inset-0 pointer-events-none"
        style="background-image: linear-gradient(rgba(35,78,204,0.03) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(35,78,204,0.03) 1px, transparent 1px);
               background-size: 60px 60px;"
        aria-hidden="true"
      ></div>

      <!-- Content -->
      <div class="relative z-10 max-w-4xl mx-auto text-center">

        <!-- Arabic verse — slides DOWN from above -->
        <div class="hero-slide-down mb-2">
          <p class="arabic-center text-2xl sm:text-3xl text-brand-light">
            وَقُل رَّبِّ زِدْنِي عِلْمًا
          </p>
          <p class="text-white/40 text-sm italic mt-1">
            {{ t('home.verseTranslation') }}
          </p>
        </div>

        <!-- Blue accent line — fades up -->
        <div class="hero-slide-up flex justify-center my-8">
          <span class="block h-px w-24 rounded-full bg-gradient-to-r from-transparent via-brand to-transparent"></span>
        </div>

        <!-- Main headline — slides from right -->
        <h1
          class="hero-slide-left text-4xl sm:text-5xl lg:text-6xl font-bold
                 leading-tight mb-6 tracking-tight"
        >
          {{ t('home.heroHeadline') }}
        </h1>

        <!-- Sub-headline — scale in -->
        <p
          class="hero-scale-in text-white/60 text-lg sm:text-xl max-w-2xl mx-auto
                 mb-12 leading-relaxed"
        >
          {{ t('home.heroSub') }}
        </p>

        <!-- CTAs — scale in (delayed) -->
        <div
          class="flex flex-col sm:flex-row gap-4 justify-center"
          style="animation: scaleIn 0.8s cubic-bezier(0.16,1,0.3,1) both; animation-delay: 0.7s;"
        >
          <RouterLink
            to="/learn"
            class="bg-brand hover:bg-brand-dark text-white
                   px-8 py-4 rounded-xl font-semibold transition-all duration-200
                   shadow-lg shadow-brand/30 text-lg hover:-translate-y-0.5
                   hover:shadow-brand/40 hover:shadow-xl"
          >
            {{ t('home.heroCta1') }}
          </RouterLink>
          <a
            href="https://github.com/mohhomadfarman/Tadabbur"
            target="_blank"
            rel="noopener noreferrer"
            class="border border-white/20 hover:border-white/50 hover:bg-white/5
                   text-white/80 hover:text-white
                   px-8 py-4 rounded-xl font-semibold transition-all duration-200 text-lg
                   flex items-center justify-center gap-2.5"
          >
            <!-- GitHub icon -->
            <svg class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
            </svg>
            {{ t('home.heroCta2') }}
          </a>
        </div>

      </div>

      <!-- Scroll indicator -->
      <div
        class="absolute bottom-[-0] left-1/2 -translate-x-1/2 flex flex-col
                items-center gap-2 hero-enter-fade"
      >
        <span class="text-xs tracking-widest uppercase text-white/30 font-medium">
          {{ t('home.heroScrollHint') }}
        </span>
        <svg
          class="w-5 h-5 text-white/30 bounce-chevron"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 2 — THE PROBLEM (dark, editorial split layout)     -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section ref="problemRef" class="py-28 px-4 bg-[#0d0d0d] text-white">
      <div class="max-w-6xl mx-auto">

        <!-- Top: stat + headline -->
        <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-start mb-16">

          <!-- Left: big stat -->
          <div class="reveal">
            <p class="text-[clamp(3.5rem,8vw,6rem)] font-black leading-none text-white tracking-tighter mb-4">
              1.8<span class="text-brand-light">B</span>
            </p>
            <p class="text-white/40 text-lg leading-relaxed max-w-xs">
              Muslims worldwide. Zero platforms actually worth their time.
            </p>
            <div class="mt-8 w-12 h-1 rounded-full bg-brand"></div>
          </div>

          <!-- Right: headline -->
          <div class="reveal reveal-delay-2 lg:pt-4">
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold leading-tight text-white">
              {{ t('home.problemTitle') }}
            </h2>
            <p class="mt-5 text-white/40 text-lg leading-relaxed">
              {{ t('home.problemSub') }}
            </p>
          </div>
        </div>

        <!-- Pain points: horizontal rows -->
        <div class="space-y-5">

          <div class="reveal reveal-delay-1 group flex items-start gap-6
                      bg-white/[0.03] border border-white/[0.07] rounded-2xl p-6
                      hover:border-red-500/30 hover:bg-white/[0.05] transition-all duration-300">
            <div class="icon-circle bg-red-500/10 shrink-0">
              <!-- Fragmented/scatter icon -->
              <svg class="w-6 h-6 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect x="2" y="2" width="6" height="6" rx="1"/>
                <rect x="16" y="2" width="6" height="6" rx="1"/>
                <rect x="9" y="9" width="6" height="6" rx="1"/>
                <rect x="2" y="16" width="6" height="6" rx="1"/>
                <rect x="16" y="16" width="6" height="6" rx="1"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-white text-lg mb-2">{{ t('home.pain1Title') }}</h3>
              <p class="text-white/50 leading-relaxed text-base">{{ t('home.pain1Desc') }}</p>
            </div>
            <div class="shrink-0 text-red-500/30 group-hover:text-red-500/60 transition-colors">
              <span class="text-5xl font-black opacity-20 select-none">01</span>
            </div>
          </div>

          <div class="reveal reveal-delay-2 group flex items-start gap-6
                      bg-white/[0.03] border border-white/[0.07] rounded-2xl p-6
                      hover:border-red-500/30 hover:bg-white/[0.05] transition-all duration-300">
            <div class="icon-circle bg-red-500/10 shrink-0">
              <!-- Shield-off icon -->
              <svg class="w-6 h-6 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-white text-lg mb-2">{{ t('home.pain2Title') }}</h3>
              <p class="text-white/50 leading-relaxed text-base">{{ t('home.pain2Desc') }}</p>
            </div>
            <div class="shrink-0">
              <span class="text-5xl font-black opacity-20 select-none text-red-500/30">02</span>
            </div>
          </div>

          <div class="reveal reveal-delay-3 group flex items-start gap-6
                      bg-white/[0.03] border border-white/[0.07] rounded-2xl p-6
                      hover:border-red-500/30 hover:bg-white/[0.05] transition-all duration-300">
            <div class="icon-circle bg-red-500/10 shrink-0">
              <!-- Pause/passive icon -->
              <svg class="w-6 h-6 text-red-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <rect x="6" y="4" width="4" height="16" rx="1"/>
                <rect x="14" y="4" width="4" height="16" rx="1"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-white text-lg mb-2">{{ t('home.pain3Title') }}</h3>
              <p class="text-white/50 leading-relaxed text-base">{{ t('home.pain3Desc') }}</p>
            </div>
            <div class="shrink-0">
              <span class="text-5xl font-black opacity-20 select-none text-red-500/30">03</span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 3 — THE SOLUTION (white, feature grid)             -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section ref="diffRef" class="py-28 px-4 bg-white">
      <div class="max-w-6xl mx-auto">

        <!-- Header -->
        <div class="max-w-2xl mx-auto text-center mb-16">
          <h2 class="reveal text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight mb-5">
            {{ t('home.diffTitle') }}
          </h2>
          <p class="reveal reveal-delay-1 text-gray-500 text-lg leading-relaxed">
            {{ t('home.diffSub') }}
          </p>
        </div>

        <!-- 2x2 feature grid -->
        <div class="grid sm:grid-cols-2 gap-6">

          <div
            v-for="(item, i) in differentiators"
            :key="item.key"
            :class="`reveal reveal-delay-${i + 1}`"
            class="group relative bg-gray-50 border border-gray-100 rounded-2xl p-8
                   hover:border-brand/20 hover:shadow-xl hover:shadow-brand/5
                   hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <!-- Subtle top accent line -->
            <div
              class="absolute top-0 left-0 right-0 h-0.5 rounded-t-2xl opacity-0
                     group-hover:opacity-100 transition-opacity duration-300"
              :style="`background: linear-gradient(90deg, ${item.accentFrom}, ${item.accentTo});`"
            ></div>

            <div
              class="icon-circle mb-6 transition-transform duration-300 group-hover:scale-110"
              :style="`background: ${item.bgColor};`"
            >
              <svg
                class="w-6 h-6"
                :style="`color: ${item.iconColor};`"
                viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true"
                v-html="item.iconPath"
              ></svg>
            </div>

            <h3 class="font-bold text-gray-900 text-xl mb-3 group-hover:text-brand transition-colors duration-200">
              {{ t(`home.${item.key}Title`) }}
            </h3>
            <p class="text-gray-500 leading-relaxed text-base">
              {{ t(`home.${item.key}Desc`) }}
            </p>
          </div>

        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 4 — ROADMAP (light gray, timeline-inspired)        -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section ref="roadmapRef" class="py-28 px-4 bg-[#f8f9fb]">
      <div class="max-w-6xl mx-auto">

        <!-- Header -->
        <div class="max-w-xl mx-auto text-center mb-16">
          <h2 class="reveal text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight mb-5">
            {{ t('home.roadmapTitle') }}
          </h2>
          <p class="reveal reveal-delay-1 text-gray-500 text-lg leading-relaxed">
            {{ t('home.roadmapSub') }}
          </p>
        </div>

        <!-- Phase grid -->
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="(phase, i) in phases"
            :key="phase.key"
            :class="[
              `reveal reveal-delay-${(i % 3) + 1}`,
              phase.current
                ? 'border-brand bg-white ring-1 ring-brand/20 shadow-lg shadow-brand/8'
                : 'border-gray-200 bg-white hover:border-gray-300',
            ]"
            class="relative border rounded-2xl p-6 transition-all duration-300 hover:shadow-md"
          >
            <!-- Phase number badge -->
            <div class="flex items-center justify-between mb-5">
              <span
                :class="phase.current ? 'bg-brand text-white' : 'bg-gray-100 text-gray-400'"
                class="text-xs font-bold uppercase tracking-widest px-3 py-1.5 rounded-full"
              >
                {{ phase.current ? t('home.roadmapCurrentBadge') : t('home.roadmapPlannedBadge') }}
              </span>
              <span class="text-2xl font-black text-gray-100 select-none">{{ String(i + 1).padStart(2, '0') }}</span>
            </div>

            <!-- Icon -->
            <div
              class="icon-circle mb-4"
              :style="phase.current ? 'background: #e8edfb;' : 'background: #f3f4f6;'"
            >
              <svg
                class="w-5 h-5"
                :style="phase.current ? 'color: #234ecc;' : 'color: #9ca3af;'"
                viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true"
                v-html="phase.iconPath"
              ></svg>
            </div>

            <h3
              :class="phase.current ? 'text-brand' : 'text-gray-900'"
              class="font-bold text-lg mb-2"
            >
              {{ t(`home.${phase.key}Title`) }}
            </h3>
            <p class="text-gray-500 text-sm leading-relaxed">
              {{ t(`home.${phase.key}Desc`) }}
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 5 — WHO IT'S FOR (white, colored accent cards)     -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section ref="audienceRef" class="py-28 px-4 bg-white">
      <div class="max-w-6xl mx-auto">

        <!-- Header -->
        <div class="max-w-2xl mx-auto text-center mb-16">
          <h2 class="reveal text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 leading-tight">
            {{ t('home.audienceTitle') }}
          </h2>
        </div>

        <!-- Audience cards -->
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div
            v-for="(item, i) in audience"
            :key="item.key"
            :class="`reveal reveal-delay-${(i % 3) + 1}`"
            class="group relative bg-white border border-gray-100 rounded-2xl p-7
                   hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <!-- Colored left border accent -->
            <div
              class="absolute left-0 top-4 bottom-4 w-1 rounded-full transition-all duration-300
                     group-hover:top-0 group-hover:bottom-0 group-hover:rounded-none"
              :style="`background: ${item.accent};`"
            ></div>

            <!-- Icon -->
            <div
              class="icon-circle mb-5 transition-transform duration-300 group-hover:scale-110"
              :style="`background: ${item.bgColor};`"
            >
              <svg
                class="w-5 h-5"
                :style="`color: ${item.accent};`"
                viewBox="0 0 24 24" fill="none" stroke="currentColor"
                stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true"
                v-html="item.iconPath"
              ></svg>
            </div>

            <h3 class="font-bold text-gray-900 text-lg mb-2 transition-colors duration-200"
                :style="`color: ${item.accent}`"
            >
              {{ t(`home.${item.key}Title`) }}
            </h3>
            <p class="text-gray-500 text-sm leading-relaxed">
              {{ t(`home.${item.key}Desc`) }}
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 6 — OPEN SOURCE (dark, split mission + stats)      -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section ref="openSourceRef" class="py-28 px-4 bg-[#060606] text-white relative overflow-hidden">

      <!-- Decorative floating Arabic -->
      <div
        class="absolute inset-0 flex items-center justify-end pr-8
                pointer-events-none select-none"
        aria-hidden="true"
      >
        <span
          class="arabic-text font-bold text-white/[0.025] float-arabic-slow leading-none"
          style="font-size: clamp(8rem, 20vw, 18rem);"
        >
          علم
        </span>
      </div>

      <div class="relative z-10 max-w-6xl mx-auto">
        <div class="grid lg:grid-cols-2 gap-16 items-center">

          <!-- Left: mission statement -->
          <div>
            <h2 class="reveal text-3xl sm:text-4xl lg:text-5xl font-bold text-white leading-tight mb-6">
              {{ t('home.openSourceTitle') }}
            </h2>
            <p class="reveal reveal-delay-1 text-white/50 text-lg leading-relaxed mb-10">
              {{ t('home.openSourceSub') }}
            </p>

            <!-- CTAs -->
            <div class="reveal reveal-delay-2 flex flex-col sm:flex-row gap-4">
              <a
                href="https://github.com/mohhomadfarman/Tadabbur"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-2.5
                       bg-brand hover:bg-brand-dark text-white
                       px-7 py-3.5 rounded-xl font-semibold transition-all duration-200
                       shadow-lg shadow-brand/30 hover:-translate-y-0.5 hover:shadow-brand/40"
              >
                <svg class="w-5 h-5 shrink-0" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                </svg>
                {{ t('home.ctaGithub') }}
              </a>
              <RouterLink
                to="/learn"
                class="inline-flex items-center justify-center
                       border border-white/20 hover:border-white/40 hover:bg-white/5
                       text-white/70 hover:text-white
                       px-7 py-3.5 rounded-xl font-semibold transition-all duration-200"
              >
                {{ t('home.ctaDocs') }}
              </RouterLink>
            </div>
          </div>

          <!-- Right: stats -->
          <div class="reveal reveal-delay-2 space-y-4">
            <div
              v-for="stat in stats"
              :key="stat.labelKey"
              class="flex items-center gap-5 bg-white/[0.04] border border-white/[0.08]
                     rounded-2xl px-6 py-5 hover:bg-white/[0.07] transition-all duration-200"
            >
              <div class="icon-circle bg-brand/10 shrink-0">
                <svg
                  class="w-5 h-5 text-brand-light"
                  viewBox="0 0 24 24" fill="none" stroke="currentColor"
                  stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
                  aria-hidden="true"
                  v-html="stat.iconPath"
                ></svg>
              </div>
              <div>
                <p class="text-3xl font-black text-white leading-none mb-1">{{ stat.value }}</p>
                <p class="text-xs font-semibold uppercase tracking-widest text-white/40">
                  {{ t(`home.${stat.labelKey}`) }}
                </p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- SECTION 7 — FINAL CTA (deep blue gradient)                 -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <section
      ref="finalRef"
      class="relative py-32 px-4 overflow-hidden text-white"
      style="background: linear-gradient(135deg, #0a0f2e 0%, #162060 40%, #1a3ba8 70%, #234ecc 100%);"
    >
      <!-- Decorative mesh pattern -->
      <div
        class="absolute inset-0 pointer-events-none"
        style="background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
               background-size: 40px 40px;"
        aria-hidden="true"
      ></div>

      <!-- Glow -->
      <div
        class="absolute bottom-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px]
               rounded-full pointer-events-none blur-3xl"
        style="background: radial-gradient(ellipse, rgba(61,101,232,0.4) 0%, transparent 70%);"
        aria-hidden="true"
      ></div>

      <div class="relative z-10 max-w-2xl mx-auto text-center">

        <!-- Arabic verse — centered -->
        <div class="reveal mb-8">
          <p class="arabic-center text-3xl sm:text-4xl text-white/70 mb-2">
            {{ t('home.finalDecorVerse') }}
          </p>
          <p class="text-white/30 text-sm">{{ t('home.finalVerseRef') }}</p>
        </div>

        <h2 class="reveal reveal-delay-1 text-4xl sm:text-5xl lg:text-6xl font-bold
                   leading-tight mb-4 tracking-tight">
          {{ t('home.finalTitle') }}
          <span class="text-white/90 italic">{{ t('home.finalTitleAccent') }}</span>
        </h2>

        <p class="reveal reveal-delay-2 text-white/60 text-lg leading-relaxed
                  max-w-lg mx-auto mb-12">
          {{ t('home.finalSub') }}
        </p>

        <div class="reveal reveal-delay-3 flex flex-col sm:flex-row gap-4 justify-center">
          <RouterLink
            v-if="!auth.isLoggedIn"
            to="/register"
            class="bg-white hover:bg-gray-50 text-brand
                   px-8 py-4 rounded-xl font-bold text-lg transition-all duration-200
                   shadow-lg hover:-translate-y-0.5 hover:shadow-xl"
          >
            {{ t('home.finalCta1') }}
          </RouterLink>
          <RouterLink
            to="/learn"
            :class="auth.isLoggedIn
              ? 'bg-white hover:bg-gray-50 text-brand shadow-lg hover:shadow-xl'
              : 'border border-white/30 hover:border-white/60 hover:bg-white/10 text-white/80 hover:text-white'"
            class="px-8 py-4 rounded-xl font-bold text-lg transition-all duration-200 hover:-translate-y-0.5"
          >
            {{ t('home.finalCta2') }}
          </RouterLink>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useScrollReveal } from '@/composables/useScrollReveal'
import { useSeo } from '@/composables/useSeo'

const { t } = useI18n()
const auth = useAuthStore()

useSeo({
  title:       'Tadabbur — Structured Islamic Learning for the Ummah',
  description: 'A rigorous, scholar-verified Islamic curriculum. Structured tracks from beginner to advanced. Free forever. Built for the Ummah.',
  url:         'https://tadabbur.org/',
})

const { containerRef: problemRef }    = useScrollReveal()
const { containerRef: diffRef }       = useScrollReveal()
const { containerRef: roadmapRef }    = useScrollReveal()
const { containerRef: audienceRef }   = useScrollReveal()
const { containerRef: openSourceRef } = useScrollReveal()
const { containerRef: finalRef }      = useScrollReveal()

// ── Section 3: Differentiators (solutions) ─────────────────────────
const differentiators = [
  {
    key: 'diff1',
    bgColor: '#e8edfb',
    iconColor: '#234ecc',
    accentFrom: '#234ecc',
    accentTo: '#3d65e8',
    iconPath: `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="12" y1="6" x2="16" y2="6"/><line x1="12" y1="10" x2="16" y2="10"/>`,
  },
  {
    key: 'diff2',
    bgColor: '#ecfdf5',
    iconColor: '#059669',
    accentFrom: '#059669',
    accentTo: '#10b981',
    iconPath: `<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>`,
  },
  {
    key: 'diff3',
    bgColor: '#faf5ff',
    iconColor: '#7c3aed',
    accentFrom: '#7c3aed',
    accentTo: '#a855f7',
    iconPath: `<circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>`,
  },
  {
    key: 'diff4',
    bgColor: '#fff7ed',
    iconColor: '#ea580c',
    accentFrom: '#ea580c',
    accentTo: '#f97316',
    iconPath: `<rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>`,
  },
]

// ── Section 4: Roadmap phases ──────────────────────────────────────
const phases = [
  {
    key: 'phase1',
    current: true,
    iconPath: `<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>`,
  },
  {
    key: 'phase2',
    current: false,
    iconPath: `<circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>`,
  },
  {
    key: 'phase3',
    current: false,
    iconPath: `<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>`,
  },
  {
    key: 'phase4',
    current: false,
    iconPath: `<rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/>`,
  },
  {
    key: 'phase5',
    current: false,
    iconPath: `<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>`,
  },
  {
    key: 'phase6',
    current: false,
    iconPath: `<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>`,
  },
]

// ── Section 5: Audience ───────────────────────────────────────────
const audience = [
  {
    key: 'audience1',
    accent: '#059669',
    bgColor: '#ecfdf5',
    iconPath: `<path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2c-2.76 4-2.76 16 0 20"/><path d="M2 12h20"/>`,
  },
  {
    key: 'audience2',
    accent: '#2563eb',
    bgColor: '#eff6ff',
    iconPath: `<circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>`,
  },
  {
    key: 'audience3',
    accent: '#7c3aed',
    bgColor: '#faf5ff',
    iconPath: `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`,
  },
  {
    key: 'audience4',
    accent: '#b45309',
    bgColor: '#fffbeb',
    iconPath: `<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>`,
  },
  {
    key: 'audience5',
    accent: '#0f172a',
    bgColor: '#f1f5f9',
    iconPath: `<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>`,
  },
]

// ── Section 6: Stats ──────────────────────────────────────────────
const stats = [
  {
    labelKey: 'statStars',
    value: '0',
    iconPath: `<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>`,
  },
  {
    labelKey: 'statContributors',
    value: '1',
    iconPath: `<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>`,
  },
  {
    labelKey: 'statLanguages',
    value: '2',
    iconPath: `<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>`,
  },
]
</script>
