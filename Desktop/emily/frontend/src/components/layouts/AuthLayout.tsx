import React from 'react'
import { Outlet } from 'react-router-dom'

const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen gradient-bg flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            AI Marketing Agent
          </h1>
          <p className="text-white/80">
            Your intelligent marketing companion
          </p>
        </div>
        <div className="card">
          <Outlet />
        </div>
      </div>
    </div>
  )
}

export default AuthLayout 