import { Outlet } from 'react-router-dom';
import { NavLink } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary-50 to-primary-50">
      <div className="min-h-screen flex flex-col">
        {/* Logo */}
        <div className="p-4 lg:p-6">
          <NavLink to="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-xl bg-primary-600 flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-xl">V</span>
            </div>
            <span className="font-display font-bold text-2xl text-secondary-900">
              VisualVerse
            </span>
          </NavLink>
        </div>

        {/* Content */}
        <div className="flex-1 flex items-center justify-center p-4 lg:p-6">
          <Outlet />
        </div>

        {/* Footer */}
        <div className="p-4 lg:p-6 text-center">
          <p className="text-sm text-secondary-500">
            © 2024 VisualVerse. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
