import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth, AuthProvider } from './hooks/useAuth'
import AuthLayout from './components/layouts/AuthLayout'
import DashboardLayout from './components/layouts/DashboardLayout'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import ConfirmEmail from './pages/auth/ConfirmEmail'
import Onboarding from './pages/onboarding/Onboarding'
import Dashboard from './pages/dashboard/Dashboard'
import UserDashboard from './pages/dashboard/UserDashboard'
import ContentWriterDashboard from './pages/dashboard/ContentWriterDashboard'
import ContentCreation from './pages/dashboard/ContentCreation'
import EditProfile from './pages/profile/EditProfile'
import LoadingSpinner from './components/ui/LoadingSpinner'

function AppContent() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/auth" element={<AuthLayout />}>
        <Route path="login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
        <Route path="register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
        <Route path="confirm-email" element={<ConfirmEmail />} />
      </Route>

      {/* Protected routes */}
      <Route path="/" element={<DashboardLayout />}>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route 
          path="dashboard" 
          element={user ? <Dashboard /> : <Navigate to="/auth/login" />} 
        />
        <Route 
          path="onboarding" 
          element={user ? <Onboarding /> : <Navigate to="/auth/login" />} 
        />
      </Route>

      {/* User Dashboard with its own layout */}
      <Route 
        path="/user-dashboard" 
        element={user ? <UserDashboard /> : <Navigate to="/auth/login" />} 
      />

      {/* Content Writer Dashboard */}
      <Route 
        path="/content-writer-dashboard" 
        element={user ? <ContentWriterDashboard /> : <Navigate to="/auth/login" />} 
      />

      {/* Content Creation */}
      <Route 
        path="/content/create" 
        element={user ? <ContentCreation /> : <Navigate to="/auth/login" />} 
      />

      {/* Edit Profile */}
      <Route 
        path="/edit-profile" 
        element={user ? <EditProfile /> : <Navigate to="/auth/login" />} 
      />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App 