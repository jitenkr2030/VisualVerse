import axios from 'axios'

const API_BASE_URL = '/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          
          const { access_token, refresh_token } = response.data
          localStorage.setItem('accessToken', access_token)
          localStorage.setItem('refreshToken', refresh_token)
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { username: email, password }),
  
  register: (data: { email: string; password: string; full_name: string }) =>
    api.post('/auth/register', data),
  
  getMe: () => api.get('/auth/me'),
  
  refresh: (refreshToken: string) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
}

// Content API
export const contentApi = {
  list: (params?: { platform?: string; page?: number; page_size?: number }) =>
    api.get('/content', { params }),
  
  get: (id: number) => api.get(`/content/${id}`),
  
  create: (data: {
    title: string
    description?: string
    platform: string
    difficulty?: string
    is_premium?: boolean
    animation_script?: string
  }) => api.post('/content', data),
  
  update: (id: number, data: Partial<{
    title: string
    description: string
    animation_script: string
    is_premium: boolean
    metadata: Record<string, unknown>
  }>) => api.put(`/content/${id}`, data),
  
  getVersions: (id: number) => api.get(`/content/${id}/versions`),
}

// License API
export const licenseApi = {
  verify: (params: { license_id?: number; content_id?: number }) =>
    api.post('/licenses/verify', params),
}

// Syllabus API
export const syllabusApi = {
  list: (params?: { platform?: string }) =>
    api.get('/syllabi', { params }),
  
  get: (id: number) => api.get(`/syllabi/${id}`),
  
  create: (data: {
    title: string
    description?: string
    platform: string
    is_public?: boolean
    structure?: Record<string, unknown>
  }) => api.post('/syllabi', data),
}

// Moderation API
export const moderationApi = {
  submit: (contentId: number) =>
    api.post(`/moderation/content/${contentId}/submit`),
}

// Export api instance
export default api
