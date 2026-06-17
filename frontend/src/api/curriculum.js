import client from './client'

export const curriculumApi = {
  getTracks: () => client.get('/curriculum/tracks/').then(r => r.data),
  getTrack: (slug) => client.get(`/curriculum/tracks/${slug}/`).then(r => r.data),
  getSubject: (slug) => client.get(`/curriculum/subjects/${slug}/`).then(r => r.data),
  getLesson: (slug) => client.get(`/lessons/${slug}/`).then(r => r.data),
}
