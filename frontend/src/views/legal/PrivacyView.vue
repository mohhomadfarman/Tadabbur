<template>
  <div class="legal" dir="ltr">
    <div class="max-w-3xl mx-auto px-4 py-12 sm:py-16">
      <RouterLink to="/" class="inline-flex items-center gap-1.5 text-sm text-[#234ecc] hover:text-[#1a3ba8] mb-8 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
        Back to home
      </RouterLink>

      <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
      <p class="text-sm text-gray-400 mb-10">Last updated: 25 June 2026</p>

      <p>
        Tadabbur ("we", "us", "our") is a free, open-source Islamic learning platform. This Privacy
        Policy explains what information we collect, how we use it, and the choices you have. By using
        <a href="https://thetadabbur.org">thetadabbur.org</a> you agree to this policy.
      </p>

      <h2>Information we collect</h2>
      <ul>
        <li><strong>Account information</strong> — your email address, username, and (optionally) your full name when you register.</li>
        <li><strong>Learning data</strong> — your progress, completed lessons, quiz answers, enrolled tracks, and streaks, so we can show your dashboard and track your journey.</li>
        <li><strong>Usage data</strong> — anonymous analytics about how pages are used, collected via Google Analytics (e.g. pages visited, device and browser type).</li>
        <li><strong>Technical data</strong> — standard server logs such as IP address and request times, used for security and reliability.</li>
      </ul>

      <h2>How we use your information</h2>
      <ul>
        <li>To create and secure your account and keep you signed in.</li>
        <li>To save and display your learning progress.</li>
        <li>To understand how the platform is used and improve it.</li>
        <li>To protect the service against abuse, fraud, and technical issues.</li>
      </ul>

      <h2>Cookies &amp; local storage</h2>
      <p>
        We store your authentication tokens and preferences (such as language and theme) in your
        browser's local storage so you stay signed in and the site remembers your settings. Google
        Analytics may set cookies to measure usage. You can clear these at any time through your browser.
      </p>

      <h2>How your data is stored</h2>
      <p>
        Account and learning data is stored in our database, and uploaded files (such as book PDFs and
        images) are stored on our file storage. Passwords are never stored in plain text — they are
        hashed. Access to the platform is authenticated with secure tokens (JWT).
      </p>

      <h2>Sharing your information</h2>
      <p>
        We do not sell your personal information. We share data only with the services needed to run the
        platform — for example Google Analytics (usage measurement) and YouTube (when videos are embedded).
        These third parties have their own privacy policies.
      </p>

      <h2>Your rights</h2>
      <ul>
        <li>Access and update your basic profile from your account settings.</li>
        <li>Request deletion of your account and associated data by contacting us.</li>
        <li>Opt out of analytics by using browser controls or extensions that block Google Analytics.</li>
      </ul>

      <h2>Children's privacy</h2>
      <p>
        Tadabbur is intended for general audiences. We do not knowingly collect personal information from
        children under 13. If you believe a child has provided us information, please contact us and we
        will remove it.
      </p>

      <h2>Changes to this policy</h2>
      <p>
        We may update this Privacy Policy from time to time. The "last updated" date above will reflect any
        changes. Continued use of the platform after changes means you accept the updated policy.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about this policy? Email us at
        <a href="mailto:mohhomadfarman@gmail.com">mohhomadfarman@gmail.com</a>.
      </p>
    </div>
  </div>
</template>

<script setup>
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

useSeo({
  title: 'Privacy Policy',
  description: 'How Tadabbur collects, uses, and protects your information.',
  url: `${SEO_ORIGIN}/privacy`,
})
</script>

<style scoped>
.legal { color: #374151; }
.legal :deep(p) { line-height: 1.75; margin-bottom: 1rem; color: #4b5563; }
.legal :deep(h2) {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  margin-top: 2.25rem;
  margin-bottom: 0.75rem;
}
.legal :deep(ul) { list-style: disc; padding-left: 1.5rem; margin-bottom: 1rem; }
.legal :deep(li) { line-height: 1.7; margin-bottom: 0.5rem; color: #4b5563; }
.legal :deep(a) { color: #234ecc; text-decoration: underline; text-underline-offset: 2px; }
.legal :deep(a:hover) { color: #1a3ba8; }
</style>
