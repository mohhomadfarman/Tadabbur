import client from './client'

export const badgesApi = {
  getMine:   () => client.get('/badges/me/').then(r => r.data),
  getUnseen: () => client.get('/badges/unseen/').then(r => r.data),
  markSeen:  (id) => client.post(`/badges/${id}/seen/`).then(r => r.data),
}
