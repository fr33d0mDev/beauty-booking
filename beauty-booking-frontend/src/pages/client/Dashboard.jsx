/**
 * Client Dashboard
 * Overview of upcoming appointments and quick actions
 */
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import { appointmentsAPI } from '../../services/api';
import { Calendar, Clock, Plus } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import { format } from 'date-fns';

const ClientDashboard = () => {
  const { user } = useAuth();
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAppointments();
  }, [language]); // Re-fetch when language changes

  const fetchAppointments = async () => {
    try {
      const response = await appointmentsAPI.getMyAppointments({ upcoming: true }, language);
      setAppointments(response.data.appointments);
    } catch (err) {
      console.error('Failed to fetch appointments:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading fullScreen text={t('dashboard.loadingDashboard')} />;
  }

  const getStatusTranslation = (status) => {
    return t(`appointments.${status}`) || status;
  };

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-secondary-900 mb-2">
            {t('dashboard.welcomeBack')}, {user?.name}!
          </h1>
          <p className="text-secondary-600">{t('dashboard.appointmentOverview')}</p>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card hover padding="lg" className="cursor-pointer" onClick={() => navigate('/book')}>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 gradient-primary rounded-lg flex items-center justify-center">
                <Plus className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-secondary-900">{t('dashboard.bookAppointment')}</h3>
                <p className="text-sm text-secondary-600">{t('dashboard.scheduleNewService')}</p>
              </div>
            </div>
          </Card>

          <Card hover padding="lg" className="cursor-pointer" onClick={() => navigate('/my-appointments')}>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-secondary-600 rounded-lg flex items-center justify-center">
                <Calendar className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-secondary-900">{t('dashboard.myAppointments')}</h3>
                <p className="text-sm text-secondary-600">{t('dashboard.viewAllBookings')}</p>
              </div>
            </div>
          </Card>

          <Card hover padding="lg" className="cursor-pointer" onClick={() => navigate('/services')}>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <Clock className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-secondary-900">{t('dashboard.browseServices')}</h3>
                <p className="text-sm text-secondary-600">{t('dashboard.viewAvailableServices')}</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Upcoming Appointments */}
        <Card padding="lg">
          <h2 className="text-2xl font-bold text-secondary-900 mb-6">{t('dashboard.upcomingAppointments')}</h2>

          {appointments.length === 0 ? (
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 mx-auto text-secondary-300 mb-4" />
              <p className="text-secondary-600 mb-4">{t('dashboard.noUpcomingAppointments')}</p>
              <Button onClick={() => navigate('/book')}>{t('dashboard.bookFirstAppointment')}</Button>
            </div>
          ) : (
            <div className="space-y-4">
              {appointments.slice(0, 5).map((appointment) => (
                <div
                  key={appointment.id}
                  className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 gradient-primary rounded-lg flex items-center justify-center">
                      <Calendar className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-secondary-900">{appointment.service.name}</h4>
                      <p className="text-sm text-secondary-600">
                        {format(new Date(appointment.appointment_date), 'MMMM d, yyyy')} at {appointment.appointment_time}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                      appointment.status === 'confirmed'
                        ? 'bg-green-100 text-green-700'
                        : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {getStatusTranslation(appointment.status)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default ClientDashboard;
