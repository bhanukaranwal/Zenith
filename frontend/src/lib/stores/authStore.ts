import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  username: string
  role: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  token: string | null
  setUser: (user: User) => void
  setToken: (token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      token: null,
      setUser: (user) => set({ user, isAuthenticated: true }),
      setToken: (token) => {
        localStorage.setItem('access_token', token)
        set({ token, isAuthenticated: true })
      },
      logout: () => {
        localStorage.removeItem('access_token')
        set({ user: null, token: null, isAuthenticated: false })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
