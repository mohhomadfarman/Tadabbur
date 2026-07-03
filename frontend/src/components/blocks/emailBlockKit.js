// Email-specific block constants + helpers used by EmailBlockEditor.vue.
// Mirrors blockKit.js but with email's own layout-block vocabulary (text,
// header, image, button, divider, spacer) — no verse/hadith/quiz.

export const EMAIL_BLOCK_TYPES = [
  { value: 'text',    label: 'Text',    icon: 'M4 6h16M4 12h16M4 18h7',                                                                                       iconColor: 'text-gray-500' },
  { value: 'header',  label: 'Header',  icon: 'M4 6h16M4 12h10M4 18h6',                                                                                       iconColor: 'text-blue-600' },
  { value: 'image',   label: 'Image',   icon: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z', iconColor: 'text-orange-500' },
  { value: 'button',  label: 'Button',  icon: 'M9 12h6m-6 4h6M5 8h14a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2v-8a2 2 0 012-2z',                               iconColor: 'text-[#234ecc]' },
  { value: 'divider', label: 'Divider', icon: 'M4 12h16',                                                                                                      iconColor: 'text-gray-400' },
  { value: 'spacer',  label: 'Spacer',  icon: 'M12 4v4m0 8v4M4 12h1m14 0h1',                                                                                   iconColor: 'text-gray-300' },
]

export const EMAIL_BLOCK_DEFAULTS = {
  text:    { text: '' },
  header:  { text: '', level: 'h2' },
  image:   { url: '', alt: '', link: '' },
  button:  { label: '', url: '' },
  divider: {},
  spacer:  { height: 24 },
}

export const EMAIL_BLOCK_BADGE_CLASSES = {
  text:    'bg-gray-100 text-gray-600',
  header:  'bg-blue-100 text-blue-700',
  image:   'bg-orange-100 text-orange-600',
  button:  'bg-[#234ecc]/10 text-[#234ecc]',
  divider: 'bg-gray-100 text-gray-500',
  spacer:  'bg-gray-100 text-gray-400',
}

export const EMAIL_BLOCK_HEADER_CLASSES = {
  text:    'bg-gray-50 border-gray-100',
  header:  'bg-blue-50 border-blue-100',
  image:   'bg-orange-50 border-orange-100',
  button:  'bg-[#234ecc]/5 border-[#234ecc]/10',
  divider: 'bg-gray-50 border-gray-100',
  spacer:  'bg-gray-50 border-gray-100',
}

export const EMAIL_BLOCK_BORDER_CLASSES = {
  text:    'border-gray-200',
  header:  'border-blue-200',
  image:   'border-orange-200',
  button:  'border-[#234ecc]/30',
  divider: 'border-gray-200',
  spacer:  'border-gray-200',
}

// Mirrors apps.emails.personalize.MERGE_TAG_CATALOGUE — drives the merge-tag
// palette shown next to the block editor.
export const MERGE_TAG_CATALOGUE = {
  universal: ['full_name', 'email'],
  verification: ['verify_url'],
  password_reset: ['reset_url'],
  badge_earned: ['badge_name', 'badge_reward'],
  automation: ['track_title'],
}
