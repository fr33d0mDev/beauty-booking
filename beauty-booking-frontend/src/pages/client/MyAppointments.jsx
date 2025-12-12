/**
 * My Appointments Page
 * View and manage user's appointments
 */
import { useState, useEffect } from 'react';
import { appointmentsAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import { Calendar, Clock, X } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import Modal from '../../components/common/Modal';
import { format } from 'date-fns';

const MyAppointments = () => {
  const { t, language } = useLanguage();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelModal, setCancelModal] = useState({ open: false, appointmentId: null });

  useEffect(() => {
    fetchAppointments();
  }, [language]); // Re-fetch when language changes

  const fetchAppointments = async () => {
    try {
      const response = await appointmentsAPI.getMyAppointments({}, language);
      setAppointments(response.data.appointments);
    } catch (err) {
      console.error('Failed to fetch appointments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async () => {
    try {
      await appointmentsAPI.update(cancelModal.appointmentId, { status: 'cancelled' });
      setCancelModal({ open: false, appointmentId: null });
      fetchAppointments();
    } catch (err) {
      console.error('Failed to cancel appointment:', err);
    }
  };

  if (loading) {
    return <Loading fullScreen text={t('appointments.loadingAppointments')} />;
  }

  const getStatusTranslation = (status) => {
    return t(`appointments.${status}`) || status;
  };

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 mb-8">{t('appointments.title')}</h1>

        {appointments.length === 0 ? (
          <Card padding="xl">
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 mx-auto text-secondary-300 mb-4" />
              <p className="text-secondary-600 text-lg">{t('appointments.noAppointments')}</p>
            </div>
          </Card>
        ) : (
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <Card key={appointment.id} padding="lg">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="flex-grow">
                    <h3 className="text-xl font-bold text-secondary-900 mb-2">
                      {appointment.service.name}
                    </h3>
                    <div className="space-y-1 text-secondary-600">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        <span>{format(new Date(appointment.appointment_date), 'MMMM d, yyyy')}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4" />
                        <span>{appointment.appointment_time} ({appointment.service.duration} {t('services.minutes')})</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      appointment.status === 'confirmed' ? 'bg-green-100 text-green-700' :
                      appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                      appointment.status === 'cancelled' ? 'bg-red-100 text-red-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {getStatusTranslation(appointment.status)}
                    </span>

                    {(appointment.status === 'pending' || appointment.status === 'confirmed') && (
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => setCancelModal({ open: true, appointmentId: appointment.id })}
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {/* Cancel Confirmation Modal */}
        <Modal
          isOpen={cancelModal.open}
          onClose={() => setCancelModal({ open: false, appointmentId: null })}
          title={t('appointments.cancelAppointment')}
          footer={
            <>
              <Button
                variant="ghost"
                onClick={() => setCancelModal({ open: false, appointmentId: null })}
              >
                {t('appointments.keepAppointment')}
              </Button>
              <Button variant="danger" onClick={handleCancel}>
                {t('appointments.yesCancel')}
              </Button>
            </>
          }
        >
          <p className="text-secondary-600">
            {t('appointments.confirmCancel')}
          </p>
        </Modal>
      </div>
    </div>
  );
};

export default MyAppointments;
