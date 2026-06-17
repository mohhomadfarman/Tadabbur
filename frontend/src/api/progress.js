import client from './client'

export const progressApi = {
  getProgress: () => client.get('/progress/').then(r => r.data),
  markComplete: (slug) => client.post(`/progress/complete/${slug}/`).then(r => r.data),
  enrollTrack: (trackSlug) => client.post(`/progress/enroll/${trackSlug}/`).then(r => r.data),
  unenrollTrack: (trackSlug) => client.delete(`/progress/enroll/${trackSlug}/`).then(r => r.data),
  getTrackProgress: (trackSlug) => client.get(`/progress/track/${trackSlug}/`).then(r => r.data),
}
