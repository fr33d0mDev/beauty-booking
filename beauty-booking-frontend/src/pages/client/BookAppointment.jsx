/**
 * Book Appointment Page
 * Service selection and appointment booking
 */
import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { servicesAPI, appointmentsAPI } from '../../services/api';
import { Calendar as CalendarIcon } from 'lucide-react';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';

const BookAppointment = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState(searchParams.get('service') || '');
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [availableSlots, setAvailableSlots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchServices();
  }, []);

  useEffect(() => {
    if (selectedService && selectedDate) {
      fetchAvailableSlots();
    }
  }, [selectedService, selectedDate]);

  const fetchServices = async () => {
    try {
      const response = await servicesAPI.getAll(true);
      setServices(response.data.services);
    } catch (err) {
      setError('Failed to load services');
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableSlots = async () => {
    try {
      const response = await appointmentsAPI.getAvailableSlots(selectedService, selectedDate);
      setAvailableSlots(response.data.available_slots);
    } catch (err) {
      console.error('Failed to fetch slots:', err);
      setAvailableSlots([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await appointmentsAPI.create({
        service_id: selectedService,
        appointment_date: selectedDate,
        appointment_time: selectedTime,
      });

      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to book appointment');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <Loading fullScreen text="Loading booking form..." />;
  }

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-3xl mx-auto">
        <Card padding="xl">
          <div className="flex items-center gap-3 mb-6">
            <CalendarIcon className="w-8 h-8 text-primary-600" />
            <h1 className="text-3xl font-bold text-secondary-900">Book Appointment</h1>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Service Selection */}
            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-2">
                Select Service *
              </label>
              <select
                value={selectedService}
                onChange={(e) => setSelectedService(e.target.value)}
                className="w-full px-4 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                required
              >
                <option value="">Choose a service...</option>
                {services.map((service) => (
                  <option key={service.id} value={service.id}>
                    {service.name} - ${service.price} ({service.duration} min)
                  </option>
                ))}
              </select>
            </div>

            {/* Date Selection */}
            <div>
              <label className="block text-sm font-medium text-secondary-700 mb-2">
                Select Date *
              </label>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="w-full px-4 py-2 border border-secondary-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                required
              />
            </div>

            {/* Time Selection */}
            {selectedService && selectedDate && (
              <div>
                <label className="block text-sm font-medium text-secondary-700 mb-2">
                  Select Time *
                </label>
                {availableSlots.length === 0 ? (
                  <p className="text-secondary-600">No available time slots for this date</p>
                ) : (
                  <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                    {availableSlots.map((slot) => (
                      <button
                        key={slot}
                        type="button"
                        onClick={() => setSelectedTime(slot)}
                        className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
                          selectedTime === slot
                            ? 'bg-primary-600 text-white border-primary-600'
                            : 'bg-white text-secondary-700 border-secondary-300 hover:border-primary-400'
                        }`}
                      >
                        {slot}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            <Button
              type="submit"
              fullWidth
              size="lg"
              loading={submitting}
              disabled={!selectedService || !selectedDate || !selectedTime || submitting}
            >
              Confirm Booking
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default BookAppointment;
