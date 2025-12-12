/**
 * Landing Page
 * Homepage with hero section and featured services
 */
import { useNavigate } from 'react-router-dom';
import { Calendar, Star, Clock, Award } from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';

const Landing = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  const features = [
    {
      icon: Calendar,
      title: t('landing.features.easyBooking.title'),
      description: t('landing.features.easyBooking.description'),
    },
    {
      icon: Star,
      title: t('landing.features.expertProfessionals.title'),
      description: t('landing.features.expertProfessionals.description'),
    },
    {
      icon: Clock,
      title: t('landing.features.flexibleHours.title'),
      description: t('landing.features.flexibleHours.description'),
    },
    {
      icon: Award,
      title: t('landing.features.premiumQuality.title'),
      description: t('landing.features.premiumQuality.description'),
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="gradient-primary text-white py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 animate-fadeIn">
            {t('landing.heroTitle')}
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-pink-50 max-w-3xl mx-auto animate-fadeIn">
            {t('landing.heroSubtitle')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center animate-fadeIn">
            <Button
              size="lg"
              onClick={() => navigate('/book')}
              className="!bg-white !text-pink-600 hover:!bg-pink-50 font-bold shadow-lg hover:shadow-xl transition-all"
            >
              {t('landing.bookAppointment')}
            </Button>
            <Button
              size="lg"
              onClick={() => navigate('/services')}
              className="!bg-transparent !border-2 !border-white !text-white hover:!bg-white hover:!text-pink-600 font-semibold transition-all"
            >
              {t('landing.viewServices')}
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-12">
            {t('landing.whyChooseUs')}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="text-center" hover padding="lg">
                <div className="w-16 h-16 gradient-primary rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            {t('landing.readyTitle')}
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            {t('landing.readySubtitle')}
          </p>
          <Button size="lg" onClick={() => navigate('/register')}>
            {t('landing.getStarted')}
          </Button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { number: '10+', label: t('landing.stats.yearsExperience') },
              { number: '5000+', label: t('landing.stats.happyClients') },
              { number: '15+', label: t('landing.stats.servicesOffered') },
              { number: '98%', label: t('landing.stats.satisfactionRate') },
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl md:text-5xl font-bold gradient-primary bg-clip-text text-transparent mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600 font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Landing;
