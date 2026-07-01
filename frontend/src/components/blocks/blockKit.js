// Shared content-block constants + helpers used by BlockEditor.vue and any view
// that needs block defaults (e.g. the lesson editor's load/normalize logic).

export const BLOCK_TYPES = [
  { value: 'text',   label: 'Text',   icon: 'M4 6h16M4 12h16M4 18h7',                                                                                                                                                                                       iconColor: 'text-gray-500' },
  { value: 'verse',  label: 'Verse',  icon: 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',                                                                                                                iconColor: 'text-emerald-600' },
  { value: 'hadith', label: 'Hadith', icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',                                                                                                 iconColor: 'text-amber-600' },
  { value: 'image',  label: 'Image',  icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',                                                iconColor: 'text-orange-500' },
  { value: 'video',  label: 'Video',  icon: 'M15 10l4.553-2.276A1 1 0 0121 8.723v6.554a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',                                                                        iconColor: 'text-red-500' },
  { value: 'quiz',   label: 'Quiz',   icon: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',                                                 iconColor: 'text-purple-500' },
]

export const BLOCK_BADGE_CLASSES = {
  text:   'bg-gray-100 text-gray-600',
  verse:  'bg-emerald-100 text-emerald-700',
  hadith: 'bg-amber-100 text-amber-700',
  image:  'bg-orange-100 text-orange-600',
  video:  'bg-red-100 text-red-600',
  quiz:   'bg-purple-100 text-purple-600',
}

export const BLOCK_HEADER_CLASSES = {
  text:   'bg-gray-50 border-gray-100',
  verse:  'bg-emerald-50 border-emerald-100',
  hadith: 'bg-amber-50 border-amber-100',
  image:  'bg-orange-50 border-orange-100',
  video:  'bg-red-50 border-red-100',
  quiz:   'bg-purple-50 border-purple-100',
}

export const BLOCK_BORDER_CLASSES = {
  text:   'border-gray-200',
  verse:  'border-emerald-200',
  hadith: 'border-amber-200',
  image:  'border-orange-200',
  video:  'border-red-200',
  quiz:   'border-purple-200',
}

export const BLOCK_DEFAULTS = {
  text:   { text: '', source: '' },
  verse:  { arabic: '', translation: '', surah: '', ayah: null },
  hadith: { text: '', source: '', narrator: '' },
  image:  { url: '', caption: '' },
  video:  { url: '', caption: '' },
  quiz:   { question: '', options: ['', '', '', ''], correct: 0, explanation: '' },
}

export function youtubeId(url) {
  if (!url) return null
  const match = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/)
  return match ? match[1] : null
}
