export default function ContentLibrary() {
  const content = [
    { id: 1, title: 'Introduction to Calculus', platform: 'mathverse', status: 'approved', created: '2024-01-15', views: 1250 },
    { id: 2, title: 'Newton\'s Laws of Motion', platform: 'physicsverse', status: 'approved', created: '2024-01-12', views: 890 },
    { id: 3, title: 'Sorting Algorithms Explained', platform: 'algverse', status: 'approved', created: '2024-01-10', views: 2100 },
    { id: 4, title: 'Chemical Bonding Basics', platform: 'chemverse', status: 'rejected', created: '2024-01-08', views: 450 },
    { id: 5, title: 'Compound Interest Formula', platform: 'finverse', status: 'pending_review', created: '2024-01-05', views: 320 },
    { id: 6, title: 'Linear Algebra Basics', platform: 'mathverse', status: 'draft', created: '2024-01-03', views: 0 },
  ]
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Content Library</h1>
          <p className="text-gray-600 mt-1">Manage all your created content</p>
        </div>
        <a href="/editor" className="btn-primary">
          + Create New Content
        </a>
      </div>
      
      {/* Filters */}
      <div className="card">
        <div className="flex flex-wrap gap-4">
          <input
            type="text"
            placeholder="Search content..."
            className="input flex-1 min-w-64"
          />
          <select className="input w-40">
            <option value="">All Platforms</option>
            <option value="mathverse">MathVerse</option>
            <option value="physicsverse">PhysicsVerse</option>
            <option value="chemverse">ChemVerse</option>
            <option value="algverse">AlgoVerse</option>
            <option value="finverse">FinVerse</option>
          </select>
          <select className="input w-40">
            <option value="">All Status</option>
            <option value="approved">Approved</option>
            <option value="pending_review">Pending</option>
            <option value="rejected">Rejected</option>
            <option value="draft">Draft</option>
          </select>
        </div>
      </div>
      
      {/* Content grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {content.map((item) => (
          <div key={item.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <span className={`badge ${
                item.status === 'approved' ? 'badge-success' :
                item.status === 'pending_review' ? 'badge-warning' :
                item.status === 'rejected' ? 'badge-danger' : 'badge-secondary'
              }`}>
                {item.status.replace('_', ' ')}
              </span>
              <span className="text-xs text-gray-500 capitalize">
                {item.platform.replace('verse', '')}
              </span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
            <div className="flex items-center justify-between text-sm text-gray-500">
              <span>{item.views} views</span>
              <span>{item.created}</span>
            </div>
            <div className="mt-4 flex gap-2">
              <a href={`/editor/${item.id}`} className="btn-secondary btn-sm flex-1">
                Edit
              </a>
              <button className="btn-secondary btn-sm flex-1">
                View
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
