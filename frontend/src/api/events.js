import client from './client'

export const eventsApi = {
  // Public: register for the live launch event.
  registerForLaunch: (payload) => client.post('/events/register/', payload).then(r => r.data),
  // Public: read the launch page settings (date, headline, intro).
  getLaunchSettings: () => client.get('/events/settings/').then(r => r.data),
}
