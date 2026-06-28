import client from './client'

export const progressApi = {
  getProgress: () => client.get('/progress/').then(r => r.data),
  markComplete: (slug) => client.post(`/progress/complete/${slug}/`).then(r => r.data),
  saveQuizAnswer: (lessonSlug, payload) => client.post(`/progress/quiz/${lessonSlug}/`, payload).then(r => r.data),
  enrollTrack: (trackSlug, language) => client.post(`/progress/enroll/${trackSlug}/`, { language: language || '' }).then(r => r.data),
  unenrollTrack: (trackSlug) => client.delete(`/progress/enroll/${trackSlug}/`).then(r => r.data),
  setTrackLanguage: (trackSlug, language) => client.post(`/progress/track-language/${trackSlug}/`, { language: language || '' }).then(r => r.data),
  getTrackProgress: (trackSlug) => client.get(`/progress/track/${trackSlug}/`).then(r => r.data),
  getAdminLessonStats: (lessonSlug) => client.get('/progress/admin/lesson-stats/', { params: lessonSlug ? { lesson: lessonSlug } : {} }).then(r => r.data),
}
