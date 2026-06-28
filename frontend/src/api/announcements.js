import client from './client'

export const announcementsApi = {
  getActive: () => client.get('/announcements/active/').then(r => r.data),
  recordView: (id) => client.post(`/announcements/${id}/view/`).then(r => r.data),
  dismiss: (id) => client.post(`/announcements/${id}/dismiss/`).then(r => r.data),
}
