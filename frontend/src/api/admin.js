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

  // Media upload
  getUploadUrl: (filename, contentType, folder) =>
    client.post('/media/upload-url/', { filename, content_type: contentType, folder }).then(r => r.data),
}
