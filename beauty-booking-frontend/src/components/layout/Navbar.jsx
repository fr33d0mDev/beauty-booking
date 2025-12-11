/**
 * Navbar Component
 * Main navigation bar with authentication state
 */
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Menu, X, User, Calendar, LogOut, Settings, LayoutDashboard } from 'lucide-react';
import { useState } from 'react';
import Button from '../common/Button';

const Navbar = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setMobileMenuOpen(false);
  };

  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/services', label: 'Services' },
  ];

  const authLinks = isAuthenticated()
    ? [
        {
          to: isAdmin() ? '/admin/dashboard' : '/dashboard',
          label: 'Dashboard',
          icon: LayoutDashboard,
        },
        ...(isAdmin()
          ? []
          : [{ to: '/book', label: 'Book Appointment', icon: Calendar }]),
      ]
    : [];

  return (
    <nav className="bg-white shadow-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 gradient-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">B</span>
            </div>
            <span className="text-xl font-bold text-secondary-900">Beauty Salon</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="text-secondary-700 hover:text-primary-600 font-medium transition-colors"
              >
                {link.label}
              </Link>
            ))}

            {authLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className="flex items-center gap-2 text-secondary-700 hover:text-primary-600 font-medium transition-colors"
              >
                {link.icon && <link.icon className="w-4 h-4" />}
                {link.label}
              </Link>
            ))}

            {isAuthenticated() ? (
              <div className="flex items-center gap-3 ml-4 pl-4 border-l border-secondary-200">
                <span className="text-secondary-600 text-sm">
                  {user?.name}
                  {isAdmin() && <span className="ml-2 text-xs text-primary-600 font-semibold">(Admin)</span>}
                </span>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  <LogOut className="w-4 h-4 mr-1" />
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Button variant="ghost" size="sm" onClick={() => navigate('/login')}>
                  Login
                </Button>
                <Button size="sm" onClick={() => navigate('/register')}>
                  Sign Up
                </Button>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-secondary-100 transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-secondary-200 animate-fadeIn">
            <div className="flex flex-col space-y-3">
              {navLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="px-3 py-2 text-secondary-700 hover:bg-secondary-50 rounded-lg transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </Link>
              ))}

              {authLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className="flex items-center gap-2 px-3 py-2 text-secondary-700 hover:bg-secondary-50 rounded-lg transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.icon && <link.icon className="w-4 h-4" />}
                  {link.label}
                </Link>
              ))}

              {isAuthenticated() ? (
                <div className="pt-3 border-t border-secondary-200">
                  <div className="px-3 py-2 text-sm text-secondary-600">
                    Logged in as: <span className="font-medium">{user?.name}</span>
                    {isAdmin() && <span className="ml-2 text-xs text-primary-600 font-semibold">(Admin)</span>}
                  </div>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex flex-col gap-2 pt-3 border-t border-secondary-200">
                  <Button
                    variant="ghost"
                    fullWidth
                    onClick={() => {
                      navigate('/login');
                      setMobileMenuOpen(false);
                    }}
                  >
                    Login
                  </Button>
                  <Button
                    fullWidth
                    onClick={() => {
                      navigate('/register');
                      setMobileMenuOpen(false);
                    }}
                  >
                    Sign Up
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
