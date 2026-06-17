import client from './client'

export const videosApi = {
  getVideos: (pageToken = '') =>
    client.get('/videos/', { params: pageToken ? { pageToken } : {} }).then(r => r.data),
  getVideo: (id) => client.get(`/videos/${id}/`).then(r => r.data),
}
