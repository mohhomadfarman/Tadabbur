import client from './client'

export const eventsApi = {
  // Public: register for the live launch event.
  registerForLaunch: (payload) => client.post('/events/register/', payload).then(r => r.data),
}
