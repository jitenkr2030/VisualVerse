import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAuthStore } from './store/authStore'

// Layout
import AppLayout from './components/AppLayout'

// Pages
import Dashboard from './pages/Dashboard'
import Editor from './pages/Editor'
import ContentLibrary from './pages/ContentLibrary'
import Analytics from './pages/Analytics'
import Earnings from './pages/Earnings'
import Settings from './pages/Settings'
import Login from './pages/Login'

// Query client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

// Protected route wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, checkAuth } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

// Main App component
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="editor" element={<Editor />} />
            <Route path="editor/:contentId" element={<Editor />} />
            <Route path="library" element={<ContentLibrary />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="earnings" element={<Earnings />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          
          {/* Catch all - redirect to dashboard */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
