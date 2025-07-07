import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, CheckCircle, ArrowLeft } from 'lucide-react'
import { toast } from 'react-hot-toast'

const ConfirmEmail: React.FC = () => {
  const [email, setEmail] = useState<string>('')
  const [isResending, setIsResending] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const pendingEmail = localStorage.getItem('pending_email')
    if (pendingEmail) {
      setEmail(pendingEmail)
    }
  }, [])

  const handleResendEmail = async () => {
    setIsResending(true)
    try {
      // TODO: Implement resend email API call
      toast.success('Confirmation email sent again!')
    } catch (error: any) {
      toast.error('Failed to resend email. Please try again.')
    } finally {
      setIsResending(false)
    }
  }

  const handleEmailVerified = () => {
    localStorage.removeItem('pending_email')
    navigate('/auth/login')
    toast.success('Email verified! You can now log in.')
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="text-center space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <div className="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
            <Mail className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Check your email</h2>
          <p className="text-gray-600">
            We've sent a confirmation link to
          </p>
          <p className="font-medium text-gray-900">{email}</p>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
          <h3 className="font-semibold text-blue-900">Next steps:</h3>
          <ol className="text-sm text-blue-800 space-y-2">
            <li className="flex items-start">
              <span className="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">1</span>
              Check your email inbox (and spam folder)
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">2</span>
              Click the "Confirm Email" link in the email
            </li>
            <li className="flex items-start">
              <span className="flex-shrink-0 w-5 h-5 bg-blue-200 rounded-full flex items-center justify-center text-xs font-medium mr-2 mt-0.5">3</span>
              Return here and click "I've verified my email"
            </li>
          </ol>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <button
            onClick={handleEmailVerified}
            className="btn-primary w-full flex items-center justify-center"
          >
            <CheckCircle className="w-4 h-4 mr-2" />
            I've verified my email
          </button>

          <button
            onClick={handleResendEmail}
            disabled={isResending}
            className="btn-secondary w-full"
          >
            {isResending ? 'Sending...' : 'Resend confirmation email'}
          </button>
        </div>

        {/* Back to Login */}
        <div className="pt-4 border-t border-gray-200">
          <Link
            to="/auth/login"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to login
          </Link>
        </div>

        {/* Help Text */}
        <div className="text-xs text-gray-500">
          <p>Didn't receive the email? Check your spam folder or try a different email address.</p>
        </div>
      </div>
    </div>
  )
}

export default ConfirmEmail 