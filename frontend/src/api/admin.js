import client from './client'

export const adminApi = {
  // Tracks
  listTracks: () => client.get('/curriculum/admin/tracks/').then(r => r.data),
  getTrack: (slug) => client.get(`/curriculum/admin/tracks/${slug}/`).then(r => r.data),
  createTrack: (data) => client.post('/curriculum/admin/tracks/', data).then(r => r.data),
  updateTrack: (slug, data) => client.patch(`/curriculum/admin/tracks/${slug}/`, data).then(r => r.data),
  deleteTrack: (slug) => client.delete(`/curriculum/admin/tracks/${slug}/`),

  // Subjects
  listSubjects: (trackSlug) => client.get('/curriculum/admin/subjects/', { params: { track: trackSlug } }).then(r => r.data),
  getSubject: (slug) => client.get(`/curriculum/admin/subjects/${slug}/`).then(r => r.data),
  createSubject: (data) => client.post('/curriculum/admin/subjects/', data).then(r => r.data),
  updateSubject: (slug, data) => client.patch(`/curriculum/admin/subjects/${slug}/`, data).then(r => r.data),
  deleteSubject: (slug) => client.delete(`/curriculum/admin/subjects/${slug}/`),

  // Lessons
  listLessons: (subjectSlug) => client.get('/lessons/admin/', { params: { subject: subjectSlug } }).then(r => r.data),
  getLesson: (slug) => client.get(`/lessons/admin/${slug}/`).then(r => r.data),
  createLesson: (data) => client.post('/lessons/admin/', data).then(r => r.data),
  updateLesson: (slug, data) => client.patch(`/lessons/admin/${slug}/`, data).then(r => r.data),
  deleteLesson: (slug) => client.delete(`/lessons/admin/${slug}/`),

  // Lesson translations (section: curriculum)
  generateTranslation: (slug, language) => client.post(`/lessons/admin/${slug}/translate/`, { language }).then(r => r.data),
  saveTranslation:     (slug, code, data) => client.put(`/lessons/admin/${slug}/translations/${code}/`, data).then(r => r.data),
  deleteTranslation:   (slug, code) => client.delete(`/lessons/admin/${slug}/translations/${code}/`),

  // Media upload
  getUploadUrl: (filename, contentType, folder) =>
    client.post('/media/upload-url/', { filename, content_type: contentType, folder }).then(r => r.data),

  // Library (Books)
  listBooks:  ()            => client.get('/library/admin/books/').then(r => r.data),
  getBook:    (slug)        => client.get(`/library/admin/books/${slug}/`).then(r => r.data),
  createBook: (data)        => client.post('/library/admin/books/', data).then(r => r.data),
  updateBook: (slug, data)  => client.patch(`/library/admin/books/${slug}/`, data).then(r => r.data),
  deleteBook: (slug)        => client.delete(`/library/admin/books/${slug}/`),

  // Users (section: users)
  listUsers:       (params)       => client.get('/auth/admin/users/', { params }).then(r => r.data),
  getUser:         (id)           => client.get(`/auth/admin/users/${id}/`).then(r => r.data),
  updateUser:      (id, data)     => client.patch(`/auth/admin/users/${id}/`, data).then(r => r.data),
  setUserPassword: (id, password) => client.post(`/auth/admin/users/${id}/password/`, { password }).then(r => r.data),
  deleteUser:      (id)           => client.delete(`/auth/admin/users/${id}/`),
  getUserActivity: (id)           => client.get(`/auth/admin/users/${id}/activity/`).then(r => r.data),

  // Roles & permissions (section: roles)
  listRoles:    ()         => client.get('/auth/admin/roles/').then(r => r.data),
  createRole:   (data)     => client.post('/auth/admin/roles/', data).then(r => r.data),
  updateRole:   (id, data) => client.patch(`/auth/admin/roles/${id}/`, data).then(r => r.data),
  deleteRole:   (id)       => client.delete(`/auth/admin/roles/${id}/`),
  listSections: ()         => client.get('/auth/admin/sections/').then(r => r.data),

  // Event registrations (section: registrations)
  listRegistrations:  ()   => client.get('/events/admin/registrations/').then(r => r.data),
  deleteRegistration: (id) => client.delete(`/events/admin/registrations/${id}/`),

  // Launch page settings (section: registrations)
  getLaunchSettings:    ()     => client.get('/events/settings/').then(r => r.data),
  updateLaunchSettings: (data) => client.patch('/events/settings/', data).then(r => r.data),

  // Translation languages + Gemini settings (section: translations)
  getTranslationSettings:    ()     => client.get('/translations/settings/').then(r => r.data),
  updateTranslationSettings: (data) => client.patch('/translations/settings/', data).then(r => r.data),

  // Announcements / pop-up modals (section: announcements)
  listAnnouncements:   ()         => client.get('/announcements/admin/').then(r => r.data),
  getAnnouncement:     (id)       => client.get(`/announcements/admin/${id}/`).then(r => r.data),
  createAnnouncement:  (data)     => client.post('/announcements/admin/', data).then(r => r.data),
  updateAnnouncement:  (id, data) => client.patch(`/announcements/admin/${id}/`, data).then(r => r.data),
  deleteAnnouncement:  (id)       => client.delete(`/announcements/admin/${id}/`),

  // Track feedback (section: feedback)
  listFeedback:        ()           => client.get('/feedback/admin/').then(r => r.data),

  // Badges & rewards (section: badges)
  listBadges:   ()         => client.get('/badges/admin/').then(r => r.data),
  getBadge:     (id)       => client.get(`/badges/admin/${id}/`).then(r => r.data),
  createBadge:  (data)     => client.post('/badges/admin/', data).then(r => r.data),
  updateBadge:  (id, data) => client.patch(`/badges/admin/${id}/`, data).then(r => r.data),
  deleteBadge:  (id)       => client.delete(`/badges/admin/${id}/`),
  grantBadge:   (id, userId) => client.post(`/badges/admin/${id}/grant/`, { user_id: userId }).then(r => r.data),

  // Feature flags (section: features)
  listFeatureFlags:    ()           => client.get('/features/admin/').then(r => r.data),
  updateFeatureFlag:   (key, data)  => client.patch(`/features/admin/${key}/`, data).then(r => r.data),
  searchFeatureUsers:  (q)          => client.get('/features/admin/users/', { params: { q } }).then(r => r.data),
  resolveFeatureUsers: (ids)        => client.get('/features/admin/users/', { params: { ids: ids.join(',') } }).then(r => r.data),

  // Email marketing — templates (section: email)
  listEmailTemplates:  ()         => client.get('/emails/admin/templates/').then(r => r.data),
  getEmailTemplate:    (id)       => client.get(`/emails/admin/templates/${id}/`).then(r => r.data),
  createEmailTemplate: (data)     => client.post('/emails/admin/templates/', data).then(r => r.data),
  updateEmailTemplate: (id, data) => client.patch(`/emails/admin/templates/${id}/`, data).then(r => r.data),
  deleteEmailTemplate: (id)       => client.delete(`/emails/admin/templates/${id}/`),

  // Email marketing — campaigns (section: email)
  listEmailCampaigns:  ()         => client.get('/emails/admin/campaigns/').then(r => r.data),
  getEmailCampaign:    (id)       => client.get(`/emails/admin/campaigns/${id}/`).then(r => r.data),
  createEmailCampaign: (data)     => client.post('/emails/admin/campaigns/', data).then(r => r.data),
  updateEmailCampaign: (id, data) => client.patch(`/emails/admin/campaigns/${id}/`, data).then(r => r.data),
  deleteEmailCampaign: (id)       => client.delete(`/emails/admin/campaigns/${id}/`),
  sendEmailCampaign:   (id, data) => client.post(`/emails/admin/campaigns/${id}/send/`, data || {}).then(r => r.data),
  testEmailCampaign:   (id, email) => client.post(`/emails/admin/campaigns/${id}/test/`, { email }).then(r => r.data),
  listEmailSegments:   ()         => client.get('/emails/admin/segments/').then(r => r.data),
  previewEmailSegment: (segment)  => client.get('/emails/admin/segments/', { params: { segment } }).then(r => r.data),

  // Email marketing — SMTP settings (section: email)
  getEmailSettings:    ()         => client.get('/emails/admin/settings/').then(r => r.data),
  updateEmailSettings: (data)     => client.patch('/emails/admin/settings/', data).then(r => r.data),

  // Generic single test-send (synchronous — returns the real SMTP error on failure)
  testSendEmail:       (data)     => client.post('/emails/admin/test-send/', data).then(r => r.data),
}
