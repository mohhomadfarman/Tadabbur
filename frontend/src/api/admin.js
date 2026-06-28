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
}
