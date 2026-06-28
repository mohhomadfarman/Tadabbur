import client from './client'

export const feedbackApi = {
  submit: (trackSlug, { rating, comment }) =>
    client.post(`/feedback/track/${trackSlug}/`, { rating, comment }).then(r => r.data),
  mySubmission: (trackSlug) =>
    client.get(`/feedback/track/${trackSlug}/me/`).then(r => r.data),
}
