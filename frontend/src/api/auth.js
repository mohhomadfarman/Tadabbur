import client from './client'

export const authApi = {
  register: (email, username, password, fullName) =>
    client.post('/auth/register/', { email, username, password, full_name: fullName })
      .then(r => r.data),

  login: (email, password) =>
    client.post('/auth/login/', { email, password })
      .then(r => r.data),

  getProfile: () =>
    client.get('/auth/profile/').then(r => r.data),

  updateProfile: (data) =>
    client.patch('/auth/profile/', data).then(r => r.data),

  verifyEmail: (token) =>
    client.post('/auth/verify-email/', { token }).then(r => r.data),

  resendVerification: () =>
    client.post('/auth/resend-verification/').then(r => r.data),

  forgotPassword: (email) =>
    client.post('/auth/forgot-password/', { email }).then(r => r.data),

  resetPassword: (token, password) =>
    client.post('/auth/reset-password/', { token, password }).then(r => r.data),
}
