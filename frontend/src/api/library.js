import client from './client'

export const libraryApi = {
  getBooks:     (params = {}) => client.get('/library/books/', { params }).then(r => r.data),
  getBook:      (slug)        => client.get(`/library/books/${slug}/`).then(r => r.data),
  getCategories:()            => client.get('/library/categories/').then(r => r.data),

  // Admin
  adminGetBooks:  ()           => client.get('/library/admin/books/').then(r => r.data),
  adminCreateBook:(data)       => client.post('/library/admin/books/', data).then(r => r.data),
  adminUpdateBook:(slug, data) => client.patch(`/library/admin/books/${slug}/`, data).then(r => r.data),
  adminDeleteBook:(slug)       => client.delete(`/library/admin/books/${slug}/`),
}
