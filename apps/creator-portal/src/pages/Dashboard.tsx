import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

interface StatCard {
  label: string
  value: string | number
  change?: string
  icon: React.ReactNode
}

export default function Dashboard() {
  const { user } = useAuthStore()
  
  const stats: StatCard[] = [
    {
      label: 'Total Content',
      value: 24,
      change: '+3 this month',
      icon: <ContentIcon />,
    },
    {
      label: 'Total Views',
      value: '12.5K',
      change: '+15% vs last month',
      icon: <ViewsIcon />,
    },
    {
      label: 'Total Earnings',
      value: '$1,234',
      change: '+8% vs last month',
      icon: <EarningsIcon />,
    },
    {
      label: 'Avg. Completion',
      value: '72%',
      change: '+5% improvement',
      icon: <CompletionIcon />,
    },
  ]
  
  const recentContent = [
    { id: 1, title: 'Introduction to Calculus', platform: 'mathverse', status: 'approved', views: 1250 },
    { id: 2, title: 'Newton\'s Laws of Motion', platform: 'physicsverse', status: 'pending_review', views: 890 },
    { id: 3, title: 'Sorting Algorithms Explained', platform: 'algverse', status: 'approved', views: 2100 },
    { id: 4, title: 'Chemical Bonding Basics', platform: 'chemverse', status: 'rejected', views: 450 },
  ]
  
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.full_name?.split(' ')[0] || 'Creator'}!
        </h1>
        <p className="text-gray-600 mt-1">
          Here's what's happening with your content
        </p>
      </div>
      
      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="card">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                {stat.change && (
                  <p className="text-sm text-green-600 mt-1">{stat.change}</p>
                )}
              </div>
              <div className="w-10 h-10 bg-primary-50 rounded-lg flex items-center justify-center text-primary-600">
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Quick actions and recent content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick actions */}
        <div className="card lg:col-span-1">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              to="/editor"
              className="flex items-center gap-3 p-3 rounded-lg bg-primary-50 text-primary-600 hover:bg-primary-100 transition-colors"
            >
              <PlusIcon className="w-5 h-5" />
              <span className="font-medium">Create New Content</span>
            </Link>
            <Link
              to="/library"
              className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <LibraryIcon className="w-5 h-5" />
              <span className="font-medium">View Content Library</span>
            </Link>
            <Link
              to="/analytics"
              className="flex items-center gap-3 p-3 rounded-lg bg-gray-50 text-gray-700 hover:bg-gray-100 transition-colors"
            >
              <AnalyticsIcon className="w-5 h-5" />
              <span className="font-medium">Check Analytics</span>
            </Link>
          </div>
        </div>
        
        {/* Recent content */}
        <div className="card lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Content</h2>
            <Link to="/library" className="text-sm text-primary-600 hover:text-primary-700">
              View all →
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-gray-500 border-b">
                  <th className="pb-3 font-medium">Title</th>
                  <th className="pb-3 font-medium">Platform</th>
                  <th className="pb-3 font-medium">Status</th>
                  <th className="pb-3 font-medium text-right">Views</th>
                </tr>
              </thead>
              <tbody>
                {recentContent.map((content) => (
                  <tr key={content.id} className="border-b last:border-0">
                    <td className="py-3">
                      <Link 
                        to={`/editor/${content.id}`}
                        className="font-medium text-gray-900 hover:text-primary-600"
                      >
                        {content.title}
                      </Link>
                    </td>
                    <td className="py-3">
                      <span className="text-sm text-gray-600 capitalize">
                        {content.platform.replace('verse', '')}
                      </span>
                    </td>
                    <td className="py-3">
                      <StatusBadge status={content.status} />
                    </td>
                    <td className="py-3 text-right">
                      <span className="text-sm text-gray-600">
                        {content.views.toLocaleString()}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const statusConfig: Record<string, { class: string; label: string }> = {
    approved: { class: 'badge-success', label: 'Approved' },
    pending_review: { class: 'badge-warning', label: 'Pending' },
    rejected: { class: 'badge-danger', label: 'Rejected' },
    draft: { class: 'badge-secondary', label: 'Draft' },
  }
  
  const config = statusConfig[status] || { class: 'badge-secondary', label: status }
  
  return <span className={`badge ${config.class}`}>{config.label}</span>
}

// Icons
function ContentIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  )
}

function ViewsIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  )
}

function EarningsIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="12" y1="1" x2="12" y2="23" />
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
    </svg>
  )
}

function CompletionIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
      <polyline points="22 4 12 14.01 9 11.01" />
    </svg>
  )
}

function PlusIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  )
}

function LibraryIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  )
}

function AnalyticsIcon() {
  return (
    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  )
}
