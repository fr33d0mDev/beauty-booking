/**
 * Login Page
 * User login form with validation
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import { Mail, Lock } from 'lucide-react';
import Input from '../../components/common/Input';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setErrors({});

    const result = await login(formData.email, formData.password);

    if (result.success) {
      navigate('/dashboard');
    } else {
      setErrors({ general: result.error });
    }

    setLoading(false);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12 bg-secondary-50">
      <Card className="w-full max-w-md" padding="xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">{t('auth.welcomeBack')}</h1>
          <p className="text-secondary-600">{t('auth.signInToAccount')}</p>
        </div>

        {errors.general && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{errors.general}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label={t('auth.email')}
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="you@example.com"
            error={errors.email}
            icon={Mail}
            required
          />

          <Input
            label={t('auth.password')}
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder={t('auth.password')}
            error={errors.password}
            icon={Lock}
            required
          />

          <Button
            type="submit"
            fullWidth
            loading={loading}
            disabled={loading}
            size="lg"
          >
            {t('auth.signIn')}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-secondary-600">
            {t('auth.noAccount')}{' '}
            <Link to="/register" className="text-primary-600 font-medium hover:text-primary-700">
              {t('auth.signUp')}
            </Link>
          </p>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 p-4 bg-primary-50 rounded-lg">
          <p className="text-sm text-secondary-700 font-medium mb-2">{t('auth.demoAccounts')}</p>
          <div className="text-sm text-secondary-600 space-y-1">
            <p>{t('auth.admin')}: admin@beautysalon.com / admin123</p>
            <p>{t('auth.client')}: client@example.com / client123</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Login;
