/**
 * Register Page
 * User registration form
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import { Mail, Lock, User, Phone } from 'lucide-react';
import Input from '../../components/common/Input';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.name || formData.name.trim().length < 2) {
      newErrors.name = 'Name must be at least 2 characters';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (formData.phone && !/^\d{10,15}$/.test(formData.phone.replace(/[-\s()]/g, ''))) {
      newErrors.phone = 'Phone number is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
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

    const { confirmPassword, ...userData } = formData;
    const result = await register(userData);

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
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">{t('auth.createAccount')}</h1>
          <p className="text-secondary-600">{t('auth.joinUs')}</p>
        </div>

        {errors.general && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{errors.general}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label={t('auth.fullName')}
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="John Doe"
            error={errors.name}
            icon={User}
            required
          />

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
            label={t('auth.phoneNumber')}
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            placeholder="(555) 123-4567"
            error={errors.phone}
            icon={Phone}
          />

          <Input
            label={t('auth.password')}
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder={t('auth.atLeast6Chars')}
            error={errors.password}
            icon={Lock}
            required
          />

          <Input
            label={t('auth.confirmPassword')}
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder={t('auth.confirmPassword')}
            error={errors.confirmPassword}
            icon={Lock}
            required
          />

          <Button
            type="submit"
            fullWidth
            loading={loading}
            disabled={loading}
            size="lg"
            className="mt-6"
          >
            {t('auth.createAccount')}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-secondary-600">
            {t('auth.alreadyHaveAccount')}{' '}
            <Link to="/login" className="text-primary-600 font-medium hover:text-primary-700">
              {t('auth.signIn')}
            </Link>
          </p>
        </div>
      </Card>
    </div>
  );
};

export default Register;
