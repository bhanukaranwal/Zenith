import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './lib/stores/authStore'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Datasets from './pages/Datasets'
import Experiments from './pages/Experiments'
import ModelRegistry from './pages/ModelRegistry'
import Deployments from './pages/Deployments'
import Monitoring from './pages/Monitoring'
import Agents from './pages/Agents'
import Login from './pages/Login'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
})

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/projects" element={<Projects />} />
                    <Route path="/datasets" element={<Datasets />} />
                    <Route path="/experiments" element={<Experiments />} />
                    <Route path="/models" element={<ModelRegistry />} />
                    <Route path="/deployments" element={<Deployments />} />
                    <Route path="/monitoring" element={<Monitoring />} />
                    <Route path="/agents" element={<Agents />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}

export default App
