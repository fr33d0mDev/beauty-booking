/**
 * Services Page
 * Display all available services
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { servicesAPI } from '../../services/api';
import { Clock, DollarSign } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const { t, language } = useLanguage();

  useEffect(() => {
    fetchServices();
  }, [language]); // Re-fetch when language changes

  const fetchServices = async () => {
    try {
      const response = await servicesAPI.getAll(true, language);
      setServices(response.data.services);
    } catch (err) {
      setError('Failed to load services');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleBookService = (serviceId) => {
    if (isAuthenticated()) {
      navigate(`/book?service=${serviceId}`);
    } else {
      navigate('/login');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loading text={t('common.loading')} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-secondary-50 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-secondary-900 mb-4">{t('services.ourServices')}</h1>
          <p className="text-xl text-secondary-600 max-w-2xl mx-auto">
            {t('services.exploreServices')}
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Services Grid */}
        {services.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-secondary-600 text-lg">{t('services.noServicesAvailable')}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => (
              <Card key={service.id} className="flex flex-col" hover padding="none">
                {/* Service Image */}
                {service.image_url ? (
                  <div className="h-48 overflow-hidden rounded-t-lg">
                    <img
                      src={service.image_url}
                      alt={service.name}
                      className="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
                    />
                  </div>
                ) : (
                  <div className="h-48 gradient-primary rounded-t-lg flex items-center justify-center">
                    <span className="text-white text-4xl font-bold">
                      {service.name.charAt(0)}
                    </span>
                  </div>
                )}

                {/* Service Details */}
                <div className="p-6 flex-grow flex flex-col">
                  <h3 className="text-xl font-bold text-secondary-900 mb-2">
                    {service.name}
                  </h3>
                  <p className="text-secondary-600 mb-4 flex-grow line-clamp-3">
                    {service.description || t('services.professionalService')}
                  </p>

                  <div className="flex items-center justify-between mb-4 text-sm">
                    <div className="flex items-center gap-1 text-secondary-700">
                      <Clock className="w-4 h-4" />
                      <span>{service.duration} {t('services.minutes')}</span>
                    </div>
                    <div className="flex items-center gap-1 text-primary-600 font-semibold text-lg">
                      <DollarSign className="w-5 h-5" />
                      <span>{service.price.toFixed(2)}</span>
                    </div>
                  </div>

                  <Button
                    fullWidth
                    onClick={() => handleBookService(service.id)}
                  >
                    {t('services.bookNow')}
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Services;
