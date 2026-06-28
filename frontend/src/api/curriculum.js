import client from './client'

export const curriculumApi = {
  getTracks: () => client.get('/curriculum/tracks/').then(r => r.data),
  getTrack: (slug) => client.get(`/curriculum/tracks/${slug}/`).then(r => r.data),
  getSubject: (slug) => client.get(`/curriculum/subjects/${slug}/`).then(r => r.data),
  getLesson: (slug, lang) => client.get(`/lessons/${slug}/`, { params: lang ? { lang } : {} }).then(r => r.data),
  getLanguages: () => client.get('/translations/languages/').then(r => r.data),
}
