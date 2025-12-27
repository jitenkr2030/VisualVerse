/**
 * VisualVerse Student App - Layout Component
 * Main application layout with navigation
 */

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useStudent } from '../state/StudentContext';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { state } = useStudent();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigation = [
    { name: 'Home', href: '/', icon: '🏠' },
    { name: 'Lessons', href: '/lessons', icon: '📚' },
    { name: 'Subjects', href: '/subjects', icon: '📖' },
    { name: 'Search', href: '/search', icon: '🔍' },
    { name: 'Progress', href: '/progress', icon: '📊' },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            {/* Logo and brand */}
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-2">
                <span className="text-2xl">🎓</span>
                <span className="text-xl font-bold text-gray-900">VisualVerse</span>
                <span className="text-sm text-gray-500">Student</span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive(item.href)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              ))}
            </div>

            {/* User menu */}
            <div className="flex items-center space-x-4">
              {state.student && (
                <div className="flex items-center space-x-3">
                  <img
                    src={state.student.avatar || 'https://via.placeholder.com/32'}
                    alt={state.student.name}
                    className="w-8 h-8 rounded-full"
                  />
                  <div className="hidden md:block">
                    <p className="text-sm font-medium text-gray-900">{state.student.name}</p>
                    <p className="text-xs text-gray-500">{state.student.gradeLevel}</p>
                  </div>
                </div>
              )}
              
              {/* Mobile menu button */}
              <button
                className="md:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-base font-medium ${
                    isActive(item.href)
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <span>{item.icon}</span>
                  <span>{item.name}</span>
                </Link>
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">© 2024 VisualVerse Student App</span>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <Link to="/profile" className="hover:text-gray-700">Settings</Link>
              <span>•</span>
              <Link to="/help" className="hover:text-gray-700">Help</Link>
              <span>•</span>
              <Link to="/privacy" className="hover:text-gray-700">Privacy</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
