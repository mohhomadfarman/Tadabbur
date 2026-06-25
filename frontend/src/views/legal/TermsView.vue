<template>
  <div class="legal" dir="ltr">
    <div class="max-w-3xl mx-auto px-4 py-12 sm:py-16">
      <RouterLink to="/" class="inline-flex items-center gap-1.5 text-sm text-[#234ecc] hover:text-[#1a3ba8] mb-8 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
        Back to home
      </RouterLink>

      <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">Terms &amp; Conditions</h1>
      <p class="text-sm text-gray-400 mb-10">Last updated: 25 June 2026</p>

      <p>
        Welcome to Tadabbur. These Terms &amp; Conditions ("Terms") govern your use of
        <a href="https://thetadabbur.org">thetadabbur.org</a> (the "Service"). By accessing or using the
        Service, you agree to these Terms. If you do not agree, please do not use the Service.
      </p>

      <h2>About the Service</h2>
      <p>
        Tadabbur is a free, open-source platform offering structured, scholar-verified Islamic learning
        content. The Service is provided for educational purposes and is free to use.
      </p>

      <h2>Your account</h2>
      <ul>
        <li>You are responsible for providing accurate information when registering.</li>
        <li>You are responsible for keeping your password secure and for activity under your account.</li>
        <li>You must notify us of any unauthorised use of your account.</li>
        <li>We may suspend or remove accounts that violate these Terms.</li>
      </ul>

      <h2>Acceptable use</h2>
      <p>You agree not to:</p>
      <ul>
        <li>Use the Service for any unlawful purpose or to harm others.</li>
        <li>Attempt to disrupt, attack, or gain unauthorised access to the platform or its data.</li>
        <li>Misrepresent religious content or use the Service to spread misinformation.</li>
        <li>Scrape, resell, or redistribute content in violation of its licence.</li>
      </ul>

      <h2>Content &amp; intellectual property</h2>
      <p>
        Learning content is reviewed by qualified scholars and provided for personal, educational use.
        The platform's source code is open source under the MIT Licence and available on
        <a href="https://github.com/mohhomadfarman/Tadabbur" target="_blank" rel="noopener noreferrer">GitHub</a>.
        Third-party materials (such as books and videos) remain the property of their respective owners.
      </p>

      <h2>Religious content disclaimer</h2>
      <p>
        Content on Tadabbur is provided for learning and reflection. While we strive for accuracy and
        scholarly review, it is not a substitute for guidance from a qualified scholar. For personal
        rulings or sensitive matters, please consult a trusted scholar directly.
      </p>

      <h2>Disclaimer of warranties</h2>
      <p>
        The Service is provided "as is" and "as available", without warranties of any kind, whether
        express or implied. We do not guarantee that the Service will be uninterrupted, error-free, or
        free of inaccuracies.
      </p>

      <h2>Limitation of liability</h2>
      <p>
        To the fullest extent permitted by law, Tadabbur and its contributors shall not be liable for any
        indirect, incidental, or consequential damages arising from your use of the Service.
      </p>

      <h2>Third-party links</h2>
      <p>
        The Service may link to or embed third-party sites and services (such as YouTube and GitHub). We
        are not responsible for the content or practices of those third parties.
      </p>

      <h2>Changes to these Terms</h2>
      <p>
        We may update these Terms from time to time. The "last updated" date above reflects the latest
        version. Continued use of the Service after changes means you accept the updated Terms.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about these Terms? Email us at
        <a href="mailto:mohhomadfarman@gmail.com">mohhomadfarman@gmail.com</a>.
      </p>
    </div>
  </div>
</template>

<script setup>
import { useSeo, SEO_ORIGIN } from '@/composables/useSeo'

useSeo({
  title: 'Terms & Conditions',
  description: 'The terms that govern your use of the Tadabbur Islamic learning platform.',
  url: `${SEO_ORIGIN}/terms`,
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
