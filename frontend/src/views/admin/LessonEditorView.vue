<template>
  <div class="px-6 py-8 max-w-6xl mx-auto">

    <!-- Sticky top bar -->
    <div class="sticky top-0 z-10 bg-white/95 backdrop-blur border-b border-gray-200 -mx-6 px-6 py-3 flex items-center justify-between mb-8">
      <nav class="text-sm text-gray-400 flex items-center gap-2">
        <RouterLink to="/admin" class="hover:text-gray-600 transition-colors">Admin</RouterLink>
        <span>/</span>
        <span class="text-gray-600">{{ isEdit ? 'Edit Lesson' : 'New Lesson' }}</span>
      </nav>
      <div class="flex items-center gap-3">
        <span
          class="text-xs font-semibold px-2.5 py-1 rounded-full"
          :class="form.status === 'published' ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
        >
          {{ form.status === 'published' ? 'Published' : 'Draft' }}
        </span>
        <button
          type="button"
          :disabled="saving"
          @click="onSave"
          class="bg-[#234ecc] hover:bg-[#1a3ba8] disabled:opacity-60 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
        >
          {{ saving ? 'Saving…' : saveLabel }}
        </button>
        <span v-if="saved" class="text-sm text-emerald-600 font-medium flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          Saved
        </span>
        <RouterLink to="/admin" class="text-sm text-gray-500 hover:text-gray-700 transition-colors">
          Cancel
        </RouterLink>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loadingLesson" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pulse">
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-gray-100 rounded-2xl h-48" />
        <div class="bg-gray-100 rounded-2xl h-64" />
        <div class="bg-gray-100 rounded-2xl h-40" />
      </div>
      <div class="bg-gray-100 rounded-2xl h-64" />
    </div>

    <div v-else-if="loadError" class="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm">
      {{ loadError }}
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left: metadata + block editor -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Language tabs (Original | translations | generate) -->
        <div v-if="isEdit" class="bg-white border border-gray-200 rounded-2xl p-3 shadow-sm">
          <div class="flex items-center gap-2 flex-wrap">
            <button type="button" @click="activeLang = ''"
              class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
              :class="!activeLang ? 'bg-[#234ecc] text-white' : 'text-gray-500 hover:bg-gray-100'">
              Original
            </button>
            <button v-for="code in translatedCodes" :key="code" type="button" @click="activeLang = code"
              class="group inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
              :class="activeLang === code ? 'bg-[#234ecc] text-white' : 'text-gray-500 hover:bg-gray-100'">
              {{ langName(code) }}
              <span v-if="translations[code]?.is_outdated"
                :class="activeLang === code ? 'text-amber-200' : 'text-amber-500'" title="Original changed since this was translated">●</span>
              <span @click.stop="askDeleteTranslation(code)"
                class="opacity-50 hover:opacity-100" title="Delete translation">×</span>
            </button>

            <div class="flex-1" />

            <!-- Generate -->
            <template v-if="availableLangs.length">
              <select v-model="genLang"
                class="border border-gray-200 rounded-lg px-2.5 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40">
                <option value="">Add language…</option>
                <option v-for="l in availableLangs" :key="l.code" :value="l.code">{{ l.name }}</option>
              </select>
              <button type="button" @click="generateTranslation" :disabled="generating || !genLang"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-semibold bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 3v4M3 5h4M6 17v4m-2-2h4M13 3l2.5 6.5L22 12l-6.5 2.5L13 21l-2.5-6.5L4 12l6.5-2.5L13 3z"/></svg>
                {{ generating ? 'Translating…' : 'Translate' }}
              </button>
            </template>
            <RouterLink v-else :to="{ name: 'admin-translations' }" class="text-xs text-[#234ecc] hover:underline">
              Add languages to enable translation
            </RouterLink>
          </div>

          <!-- Outdated / translation banner -->
          <div v-if="activeLang" class="mt-3 flex items-center justify-between gap-3 rounded-lg px-3 py-2 text-xs"
            :class="translations[activeLang]?.is_outdated ? 'bg-amber-50 text-amber-700' : 'bg-purple-50 text-purple-700'">
            <span v-if="translations[activeLang]?.is_outdated">
              The original lesson changed after this translation was generated — review or re-translate.
            </span>
            <span v-else>Editing the <strong>{{ langName(activeLang) }}</strong> translation. Proofread, then save.</span>
            <button type="button" @click="generateTranslationFor(activeLang)" :disabled="generating"
              class="shrink-0 font-semibold hover:underline disabled:opacity-50">
              {{ generating ? 'Translating…' : 'Re-translate' }}
            </button>
          </div>
        </div>

        <!-- Metadata card -->
        <div class="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Title <span class="text-red-500">*</span></label>
            <input
              v-model="doc.title"
              @input="autofillSlug"
              type="text"
              required
              :dir="editDir"
              placeholder="e.g. The Five Pillars of Islam"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
          </div>

          <div v-if="!activeLang">
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Slug</label>
            <div class="flex gap-2">
              <input
                v-model="form.slug"
                @input="slugWasEdited = true"
                type="text"
                placeholder="auto-generated"
                class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
              <button
                type="button"
                @click="regenerateSlug"
                class="px-3 py-2.5 text-xs text-gray-500 border border-gray-200 rounded-xl hover:border-[#234ecc]/40 hover:text-[#234ecc] transition-colors"
              >
                Regenerate
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Summary</label>
            <textarea
              v-model="doc.summary"
              rows="2"
              :dir="editDir"
              placeholder="Brief description shown in lesson lists…"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
            />
          </div>
        </div>

        <!-- WYSIWYG Block Editor -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-sm font-semibold text-gray-700">Content</h2>
            <span class="text-xs text-gray-400">{{ doc.content_blocks.length }} block{{ doc.content_blocks.length !== 1 ? 's' : '' }}</span>
          </div>

          <!-- Block list -->
          <div class="space-y-3">
            <div v-if="doc.content_blocks.length === 0" class="text-center text-gray-400 text-sm py-10 border-2 border-dashed border-gray-200 rounded-2xl">
              No content yet — add your first block below.
            </div>

            <div
              v-for="(block, idx) in doc.content_blocks"
              :key="idx"
              class="border rounded-2xl overflow-hidden shadow-sm"
              :class="BLOCK_BORDER_CLASSES[block.type]"
            >
              <!-- Block header -->
              <div
                class="flex items-center gap-3 px-4 py-2.5 border-b"
                :class="BLOCK_HEADER_CLASSES[block.type]"
              >
                <span
                  class="text-[11px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full"
                  :class="BLOCK_BADGE_CLASSES[block.type]"
                >
                  {{ block.type }}
                </span>
                <span class="text-xs text-gray-400">#{{ idx + 1 }}</span>
                <div class="flex-1" />
                <div v-if="!activeLang" class="flex items-center gap-1">
                  <button type="button" @click="moveBlock(idx, -1)" :disabled="idx === 0"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-white/60 disabled:opacity-30 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
                    </svg>
                  </button>
                  <button type="button" @click="moveBlock(idx, 1)" :disabled="idx === doc.content_blocks.length - 1"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-700 hover:bg-white/60 disabled:opacity-30 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </button>
                  <button type="button" @click="removeBlock(idx)"
                    class="w-7 h-7 flex items-center justify-center rounded-lg text-red-300 hover:text-red-500 hover:bg-red-50 transition-colors ml-1">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </div>
              </div>

              <!-- TEXT -->
              <template v-if="block.type === 'text'">
                <div class="bg-white px-5 py-4">
                  <textarea
                    v-model="block.body.text"
                    placeholder="Start writing your paragraph…"
                    rows="5"
                    :dir="editDir"
                    class="w-full text-gray-700 leading-relaxed text-[1.05rem] resize-y bg-transparent border-0 focus:outline-none focus:ring-0 placeholder:text-gray-300"
                  />
                </div>
              </template>

              <!-- VERSE -->
              <template v-else-if="block.type === 'verse'">
                <div class="bg-emerald-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-emerald-500 px-6 py-5 space-y-3">
                  <textarea
                    v-model="block.body.arabic"
                    rows="3"
                    dir="rtl"
                    placeholder="أدخل الآية الكريمة بالتشكيل…"
                    class="w-full text-2xl text-right arabic-text text-gray-900 leading-loose bg-transparent border-0 border-b border-emerald-200 focus:outline-none focus:border-emerald-400 resize-none pb-2 placeholder:text-emerald-200"
                  />
                  <textarea
                    v-model="block.body.translation"
                    rows="2"
                    :dir="editDir"
                    placeholder="Enter English translation…"
                    class="w-full text-gray-600 italic text-sm bg-transparent border-0 border-b border-emerald-200 focus:outline-none focus:border-emerald-400 resize-none pb-2 placeholder:text-emerald-300"
                  />
                  <div class="flex items-center gap-2 text-xs text-emerald-700 font-medium flex-wrap">
                    <span class="text-emerald-400">Surah</span>
                    <input
                      v-model="block.body.surah"
                      placeholder="Name"
                      class="flex-1 min-w-[6rem] bg-transparent border-0 focus:outline-none text-emerald-700 placeholder:text-emerald-300 font-medium"
                    />
                    <span class="text-emerald-300 mx-1">·</span>
                    <span class="text-emerald-400">Ayah</span>
                    <input
                      v-model.number="block.body.ayah"
                      type="number"
                      placeholder="0"
                      class="w-16 text-right bg-transparent border-0 focus:outline-none text-emerald-700 placeholder:text-emerald-300"
                    />
                  </div>
                </div>
              </template>

              <!-- HADITH -->
              <template v-else-if="block.type === 'hadith'">
                <div class="bg-amber-50 border-l-4 rtl:border-l-0 rtl:border-r-4 border-amber-400 px-6 py-5 space-y-3">
                  <textarea
                    v-model="block.body.text"
                    rows="4"
                    :dir="editDir"
                    placeholder="Enter hadith text…"
                    class="w-full text-gray-700 italic leading-relaxed bg-transparent border-0 border-b border-amber-200 focus:outline-none focus:border-amber-400 resize-y pb-2 placeholder:text-amber-200"
                  />
                  <div class="flex items-center gap-2 text-xs">
                    <span class="text-amber-400 font-medium">—</span>
                    <input
                      v-model="block.body.source"
                      placeholder="Source (e.g. Sahih Bukhari 1)"
                      class="flex-1 text-amber-700 font-medium bg-transparent border-0 focus:outline-none placeholder:text-amber-300"
                    />
                  </div>
                  <div class="flex items-center gap-2 text-xs">
                    <span class="text-amber-300">Narrated by:</span>
                    <input
                      v-model="block.body.narrator"
                      placeholder="Narrator (optional)"
                      class="flex-1 text-amber-600 bg-transparent border-0 focus:outline-none placeholder:text-amber-300"
                    />
                  </div>
                </div>
              </template>

              <!-- IMAGE -->
              <template v-else-if="block.type === 'image'">
                <div class="bg-white p-4 space-y-3">
                  <!-- Preview -->
                  <div v-if="block.body.url" class="rounded-xl overflow-hidden border border-gray-100">
                    <img :src="block.body.url" :alt="block.body.caption || ''" class="w-full object-cover max-h-72" />
                  </div>
                  <div v-else class="rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 h-36 flex flex-col items-center justify-center gap-2 text-gray-400 text-sm">
                    <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    <span>Paste a URL or upload an image</span>
                  </div>

                  <!-- URL + upload -->
                  <div class="flex gap-2">
                    <input
                      v-model="block.body.url"
                      type="url"
                      placeholder="Paste image URL…"
                      class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                    />
                    <button
                      type="button"
                      @click="imageInputRefs[idx]?.click()"
                      :disabled="imageUploading[idx]"
                      class="shrink-0 px-3 py-2 text-xs font-medium border border-[#234ecc]/30 text-[#234ecc] rounded-xl hover:bg-[#234ecc]/5 disabled:opacity-60 transition-colors"
                    >
                      {{ imageUploading[idx] ? 'Uploading…' : 'Upload' }}
                    </button>
                    <input
                      :ref="el => imageInputRefs[idx] = el"
                      type="file"
                      accept="image/jpeg,image/png,image/webp,image/gif"
                      class="hidden"
                      @change="handleImageUpload(idx, $event)"
                    />
                  </div>

                  <!-- Caption -->
                  <input
                    v-model="block.body.caption"
                    placeholder="Caption (optional)"
                    class="w-full text-xs text-center text-gray-400 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300"
                  />
                </div>
              </template>

              <!-- VIDEO -->
              <template v-else-if="block.type === 'video'">
                <div class="bg-white p-4 space-y-3">
                  <!-- Preview -->
                  <div v-if="youtubeId(block.body.url)" class="rounded-xl overflow-hidden bg-gray-900 aspect-video">
                    <iframe
                      :src="`https://www.youtube.com/embed/${youtubeId(block.body.url)}`"
                      class="w-full h-full"
                      frameborder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowfullscreen
                    />
                  </div>
                  <div v-else-if="block.body.url" class="rounded-xl overflow-hidden bg-gray-900">
                    <video controls class="w-full aspect-video">
                      <source :src="block.body.url" />
                    </video>
                  </div>
                  <div v-else class="rounded-xl border-2 border-dashed border-gray-200 bg-gray-50 h-36 flex flex-col items-center justify-center gap-2 text-gray-400 text-sm">
                    <svg class="w-8 h-8 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                    </svg>
                    <span>Paste a YouTube or video URL below to preview</span>
                  </div>

                  <input
                    v-model="block.body.url"
                    type="url"
                    placeholder="YouTube or video URL…"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
                  />

                  <input
                    v-model="block.body.caption"
                    placeholder="Caption (optional)"
                    class="w-full text-xs text-center text-gray-400 border-0 border-b border-dashed border-gray-200 pb-1 focus:outline-none focus:border-gray-400 bg-transparent placeholder:text-gray-300"
                  />
                </div>
              </template>

              <!-- QUIZ -->
              <template v-else-if="block.type === 'quiz'">
                <!-- Question header -->
                <div class="bg-gray-50 px-5 py-4 border-b border-gray-200">
                  <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Quick Check</p>
                  <input
                    v-model="block.body.question"
                    :dir="editDir"
                    placeholder="Enter your question…"
                    class="w-full font-medium text-gray-900 bg-transparent border-0 focus:outline-none text-base placeholder:text-gray-300"
                  />
                </div>

                <!-- Options -->
                <div class="bg-white px-4 py-4 space-y-2">
                  <div
                    v-for="(opt, oi) in (block.body.options || ['', '', '', ''])"
                    :key="oi"
                    class="flex items-center gap-2.5"
                  >
                    <input
                      type="radio"
                      :name="`quiz-correct-${idx}`"
                      :value="oi"
                      v-model="block.body.correct"
                      class="accent-[#234ecc] shrink-0"
                      title="Mark as correct answer"
                    />
                    <input
                      :value="opt"
                      @input="setOption(block, oi, $event.target.value)"
                      :placeholder="`Option ${['A', 'B', 'C', 'D'][oi]}`"
                      class="flex-1 px-3 py-2.5 rounded-xl border text-sm transition-all focus:outline-none focus:ring-1"
                      :class="block.body.correct === oi
                        ? 'border-emerald-500 bg-emerald-50 text-emerald-800 focus:ring-emerald-300'
                        : 'border-gray-200 text-gray-700 hover:border-gray-300 focus:ring-[#234ecc]/30 placeholder:text-gray-300'"
                    />
                  </div>
                  <p class="text-xs text-gray-400 mt-1 ms-6">Click the radio to mark the correct answer.</p>
                </div>

                <!-- Explanation -->
                <div class="bg-white px-4 pb-4">
                  <textarea
                    v-model="block.body.explanation"
                    rows="2"
                    :dir="editDir"
                    placeholder="Explanation shown after answering (optional)…"
                    class="w-full text-sm text-blue-800 bg-blue-50 border border-blue-100 rounded-xl px-3 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-blue-300 placeholder:text-blue-300"
                  />
                </div>
              </template>

            </div>
          </div>

          <!-- Add block pills (original only — translations mirror the source structure) -->
          <div v-if="!activeLang" class="flex flex-wrap gap-2 pt-2">
            <button
              v-for="type in BLOCK_TYPES"
              :key="type.value"
              type="button"
              @click="addBlock(type.value)"
              class="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-gray-200 hover:border-[#234ecc]/30 hover:bg-[#234ecc]/5 hover:text-[#234ecc] text-xs font-medium text-gray-500 transition-colors"
            >
              <svg class="w-3.5 h-3.5 shrink-0" :class="type.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="type.icon" />
              </svg>
              + {{ type.label }}
            </button>
          </div>
        </div>

        <div v-if="apiError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
          {{ apiError }}
        </div>
      </div>

      <!-- Right: sidebar -->
      <div class="lg:col-span-1 lg:sticky lg:top-24 space-y-4">
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Subject <span class="text-red-500">*</span></label>
            <select
              v-model="form.subject_slug"
              required
              :disabled="isEdit"
              class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 bg-white disabled:bg-gray-50 disabled:text-gray-500"
            >
              <option value="" disabled>Select a subject…</option>
              <optgroup v-for="track in tracks" :key="track.slug" :label="track.title">
                <option v-for="subj in subjectsByTrack[track.slug] || []" :key="subj.slug" :value="subj.slug">
                  {{ subj.title }}
                </option>
              </optgroup>
            </select>
          </div>

          <div class="flex gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Order</label>
              <input
                v-model.number="form.order"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">Est. Minutes</label>
              <input
                v-model.number="form.estimated_minutes"
                type="number" min="0"
                class="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
              />
            </div>
          </div>

          <div class="flex items-center justify-between py-1">
            <div>
              <p class="text-sm font-medium text-gray-700">Published</p>
              <p class="text-xs text-gray-400 mt-0.5">Visible to learners when on.</p>
            </div>
            <button
              type="button"
              @click="toggleStatus"
              class="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
              :class="form.status === 'published' ? 'bg-[#234ecc]' : 'bg-gray-300'"
            >
              <span
                class="inline-block h-3.5 w-3.5 transform rounded-full bg-white shadow transition-transform"
                :class="form.status === 'published' ? 'translate-x-4' : 'translate-x-1'"
              />
            </button>
          </div>

          <div class="pt-1 border-t border-gray-100 space-y-1">
            <p class="text-xs text-gray-400">{{ form.content_blocks.length }} content block{{ form.content_blocks.length !== 1 ? 's' : '' }}</p>
            <p v-if="isEdit" class="text-xs text-gray-400">
              <RouterLink
                :to="{ name: 'lesson', params: { lessonSlug: form.slug } }"
                target="_blank"
                class="text-[#234ecc] hover:underline"
              >
                Preview lesson ↗
              </RouterLink>
            </p>
          </div>
        </div>

        <!-- SEO card -->
        <div class="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4">
          <h3 class="text-sm font-semibold text-gray-700 flex items-center gap-1.5">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="m21 21-4.35-4.35"/></svg>
            Search & Social (SEO)
          </h3>
          <p class="text-xs text-gray-400 -mt-1">Optional. Left blank, Google uses the title &amp; summary.</p>

          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1.5">Meta Title</label>
            <input
              v-model="form.meta_title"
              type="text"
              maxlength="70"
              :placeholder="form.title || 'Defaults to lesson title'"
              class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
            <p class="text-[11px] mt-1" :class="(form.meta_title?.length || 0) > 60 ? 'text-amber-500' : 'text-gray-400'">
              {{ form.meta_title?.length || 0 }}/70 — aim for ≤ 60
            </p>
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1.5">Meta Description</label>
            <textarea
              v-model="form.meta_description"
              rows="3"
              maxlength="200"
              :placeholder="form.summary || 'Defaults to lesson summary'"
              class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40 resize-none"
            />
            <p class="text-[11px] mt-1" :class="(form.meta_description?.length || 0) > 160 ? 'text-amber-500' : 'text-gray-400'">
              {{ form.meta_description?.length || 0 }}/200 — aim for ≤ 160
            </p>
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1.5">Social Image URL</label>
            <input
              v-model="form.og_image"
              type="url"
              placeholder="https://… (1200×630 recommended)"
              class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#234ecc]/40"
            />
          </div>
        </div>
      </div>

    </div>

    <!-- Delete translation modal -->
    <div v-if="deleteLangTarget" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="deleteLangTarget = null">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full p-6">
        <h3 class="font-bold text-gray-900 mb-1">Delete translation?</h3>
        <p class="text-sm text-gray-500 mb-5">The <strong>{{ langName(deleteLangTarget) }}</strong> translation of this lesson will be removed. The original is untouched.</p>
        <div class="flex gap-3">
          <button @click="deleteLangTarget = null" class="flex-1 px-4 py-2.5 text-sm text-gray-600 border border-gray-200 rounded-xl hover:text-gray-900 transition-colors">Cancel</button>
          <button :disabled="deletingLang" @click="confirmDeleteTranslation" class="flex-1 px-4 py-2.5 bg-red-500 hover:bg-red-600 disabled:opacity-60 text-white text-sm font-semibold rounded-xl transition-colors">
            {{ deletingLang ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/admin'
import { curriculumApi } from '@/api/curriculum'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.slug)

const BLOCK_TYPES = [
  { value: 'text',   label: 'Text',       icon: 'M4 6h16M4 12h16M4 18h7',                                                                                                                                                                                         iconColor: 'text-gray-500' },
  { value: 'verse',  label: 'Verse',      icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',                                                                                                                  iconColor: 'text-emerald-600' },
  { value: 'hadith', label: 'Hadith',     icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',                                                                                                   iconColor: 'text-amber-600' },
  { value: 'image',  label: 'Image',      icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',                                                  iconColor: 'text-orange-500' },
  { value: 'video',  label: 'Video',      icon: 'M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',                                                                          iconColor: 'text-red-500' },
  { value: 'quiz',   label: 'Quiz',       icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',                                                   iconColor: 'text-purple-500' },
]

const BLOCK_BADGE_CLASSES = {
  text:   'bg-gray-100 text-gray-600',
  verse:  'bg-emerald-100 text-emerald-700',
  hadith: 'bg-amber-100 text-amber-700',
  image:  'bg-orange-100 text-orange-600',
  video:  'bg-red-100 text-red-600',
  quiz:   'bg-purple-100 text-purple-600',
}

const BLOCK_HEADER_CLASSES = {
  text:   'bg-gray-50 border-gray-100',
  verse:  'bg-emerald-50 border-emerald-100',
  hadith: 'bg-amber-50 border-amber-100',
  image:  'bg-orange-50 border-orange-100',
  video:  'bg-red-50 border-red-100',
  quiz:   'bg-purple-50 border-purple-100',
}

const BLOCK_BORDER_CLASSES = {
  text:   'border-gray-200',
  verse:  'border-emerald-200',
  hadith: 'border-amber-200',
  image:  'border-orange-200',
  video:  'border-red-200',
  quiz:   'border-purple-200',
}

const BLOCK_DEFAULTS = {
  text:   { text: '' },
  verse:  { arabic: '', translation: '', surah: '', ayah: null },
  hadith: { text: '', source: '', narrator: '' },
  image:  { url: '', caption: '' },
  video:  { url: '', caption: '' },
  quiz:   { question: '', options: ['', '', '', ''], correct: 0, explanation: '' },
}

const form = ref({
  subject_slug: route.query.subject || '',
  title: '',
  slug: '',
  summary: '',
  estimated_minutes: 10,
  order: 0,
  status: 'draft',
  content_blocks: [],
  meta_title: '',
  meta_description: '',
  og_image: '',
})

const tracks = ref([])
const subjectsByTrack = ref({})
const loadingLesson = ref(isEdit.value)
const loadError = ref('')
const saving = ref(false)
const saved = ref(false)
const apiError = ref('')
let slugWasEdited = false

const imageUploading = reactive({})
const imageInputRefs = ref([])

// ── Translations ─────────────────────────────────────────────────────────
const activeLang = ref('')            // '' = original; otherwise a language code
const translations = reactive({})     // code -> { title, summary, meta_*, content_blocks, is_outdated, ... }
const availableLangs = ref([])        // enabled languages from admin settings
const genLang = ref('')               // selected language in the "Add language" dropdown
const generating = ref(false)
const deleteLangTarget = ref(null)
const deletingLang = ref(false)

// The document currently being edited: the original form, or a translation.
const doc = computed(() =>
  (activeLang.value && translations[activeLang.value]) ? translations[activeLang.value] : form.value
)
const translatedCodes = computed(() => Object.keys(translations))
const editDir = computed(() => (activeLang.value && langRtl(activeLang.value)) ? 'rtl' : 'ltr')
const saveLabel = computed(() =>
  activeLang.value ? `Save ${langName(activeLang.value)}` : (isEdit.value ? 'Save Changes' : 'Create Lesson')
)

function langName(code) {
  return availableLangs.value.find(l => l.code === code)?.name || code
}
function langRtl(code) {
  return !!availableLangs.value.find(l => l.code === code)?.rtl
}

function normalizeTranslation(raw) {
  return {
    title: raw.title || '',
    summary: raw.summary || '',
    meta_title: raw.meta_title || '',
    meta_description: raw.meta_description || '',
    content_blocks: (raw.content_blocks || []).map(b => ({
      type: b.type,
      body: { ...BLOCK_DEFAULTS[b.type], ...b.body },
    })),
    is_outdated: !!raw.is_outdated,
    translated_at: raw.translated_at || '',
    model: raw.model || '',
    edited: !!raw.edited,
  }
}

async function generateTranslation() {
  if (genLang.value) await generateTranslationFor(genLang.value)
}

async function generateTranslationFor(code) {
  if (!isEdit.value) { apiError.value = 'Create the lesson first, then translate it.'; return }
  apiError.value = ''
  generating.value = true
  try {
    // Persist the latest original so Gemini translates the current content.
    await adminApi.updateLesson(route.params.slug, buildOriginalPayload())
    const res = await adminApi.generateTranslation(route.params.slug, code)
    translations[code] = normalizeTranslation(res.translation)
    activeLang.value = code
    genLang.value = ''
  } catch (e) {
    apiError.value = e.response?.data?.detail
      || 'Could not generate translation. Check the Gemini settings in Admin → Languages.'
  } finally {
    generating.value = false
  }
}

async function saveTranslation() {
  const code = activeLang.value
  const tr = translations[code]
  if (!tr) return
  apiError.value = ''
  saved.value = false
  saving.value = true
  try {
    const res = await adminApi.saveTranslation(route.params.slug, code, {
      title: tr.title,
      summary: tr.summary,
      meta_title: tr.meta_title,
      meta_description: tr.meta_description,
      content_blocks: tr.content_blocks.map((b, i) => ({ type: b.type, order: i, body: b.body })),
      edited: true,
    })
    translations[code] = normalizeTranslation(res.translation)
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
  } catch {
    apiError.value = 'Could not save the translation.'
  } finally {
    saving.value = false
  }
}

function onSave() {
  return activeLang.value ? saveTranslation() : save()
}

function askDeleteTranslation(code) {
  deleteLangTarget.value = code
}

async function confirmDeleteTranslation() {
  const code = deleteLangTarget.value
  deletingLang.value = true
  try {
    await adminApi.deleteTranslation(route.params.slug, code)
    delete translations[code]
    if (activeLang.value === code) activeLang.value = ''
    deleteLangTarget.value = null
  } catch {
    apiError.value = 'Could not delete the translation.'
  } finally {
    deletingLang.value = false
  }
}

function youtubeId(url) {
  if (!url) return null
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/)
  return match ? match[1] : null
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function autofillSlug() {
  if (activeLang.value) return  // slug belongs to the original only
  if (!slugWasEdited) form.value.slug = slugify(form.value.title)
}

function regenerateSlug() {
  form.value.slug = slugify(form.value.title)
  slugWasEdited = false
}

function toggleStatus() {
  form.value.status = form.value.status === 'published' ? 'draft' : 'published'
}

function addBlock(type) {
  form.value.content_blocks.push({ type, body: { ...BLOCK_DEFAULTS[type] } })
}

function removeBlock(idx) {
  form.value.content_blocks.splice(idx, 1)
}

function moveBlock(idx, dir) {
  const blocks = form.value.content_blocks
  const target = idx + dir
  if (target < 0 || target >= blocks.length) return
  const tmp = blocks[idx]
  blocks[idx] = blocks[target]
  blocks[target] = tmp
}

function setOption(block, oi, val) {
  if (!block.body.options) block.body.options = ['', '', '', '']
  block.body.options[oi] = val
}

async function handleImageUpload(idx, event) {
  const file = event.target.files?.[0]
  if (!file) return
  imageUploading[idx] = true
  try {
    const { upload_url, public_url } = await adminApi.getUploadUrl(file.name, file.type, 'image')
    const res = await fetch(upload_url, {
      method: 'PUT',
      body: file,
      headers: { 'Content-Type': file.type },
    })
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    doc.value.content_blocks[idx].body.url = public_url
  } catch {
    apiError.value = 'Image upload failed. Please try again or paste a URL.'
  } finally {
    imageUploading[idx] = false
    if (imageInputRefs.value[idx]) imageInputRefs.value[idx].value = ''
  }
}

function buildOriginalPayload() {
  return {
    subject_slug: form.value.subject_slug,
    title: form.value.title,
    slug: form.value.slug,
    summary: form.value.summary,
    estimated_minutes: form.value.estimated_minutes,
    order: form.value.order,
    status: form.value.status,
    meta_title: form.value.meta_title,
    meta_description: form.value.meta_description,
    og_image: form.value.og_image,
    content_blocks: form.value.content_blocks.map((b, i) => ({
      type: b.type,
      order: i,
      body: b.body,
    })),
  }
}

async function save() {
  apiError.value = ''
  saved.value = false
  saving.value = true
  try {
    const payload = buildOriginalPayload()
    if (isEdit.value) {
      await adminApi.updateLesson(route.params.slug, payload)
      saved.value = true
      setTimeout(() => { saved.value = false }, 2500)
    } else {
      const created = await adminApi.createLesson(payload)
      slugWasEdited = true
      saved.value = true
      setTimeout(() => { saved.value = false }, 2500)
      // Go to the edit page so the user stays on the editor (now editable)
      if (created?.slug) router.replace({ name: 'admin-lesson-edit', params: { slug: created.slug } })
    }
  } catch (e) {
    const data = e.response?.data
    apiError.value = typeof data === 'object'
      ? Object.values(data).flat().join(' ')
      : 'Could not save lesson.'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  tracks.value = await adminApi.listTracks()
  await Promise.all(
    tracks.value.map(async (t) => {
      subjectsByTrack.value[t.slug] = await adminApi.listSubjects(t.slug)
    })
  )

  try { availableLangs.value = await curriculumApi.getLanguages() } catch { /* none configured */ }

  if (!isEdit.value) return
  try {
    const data = await adminApi.getLesson(route.params.slug)
    form.value = {
      subject_slug: data.subject_slug,
      title: data.title,
      slug: data.slug,
      summary: data.summary || '',
      estimated_minutes: data.estimated_minutes || 10,
      order: data.order ?? 0,
      status: data.status,
      meta_title: data.meta_title || '',
      meta_description: data.meta_description || '',
      og_image: data.og_image || '',
      content_blocks: (data.content_blocks || []).map(b => ({
        type: b.type,
        body: { ...BLOCK_DEFAULTS[b.type], ...b.body },
      })),
    }
    slugWasEdited = true

    // Load any existing translations into the per-language editors.
    Object.entries(data.translations || {}).forEach(([code, tr]) => {
      translations[code] = normalizeTranslation(tr)
    })
  } catch (e) {
    loadError.value = e.response?.status === 404
      ? 'Lesson not found.'
      : 'Could not load lesson. Please refresh and try again.'
  } finally {
    loadingLesson.value = false
  }
})
</script>
