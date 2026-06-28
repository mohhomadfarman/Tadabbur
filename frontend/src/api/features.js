import client from './client'

// Learner-facing: the resolved { key: bool } map for the current user.
export const featuresApi = {
  getEffective: () => client.get('/features/me/').then(r => r.data),
}
