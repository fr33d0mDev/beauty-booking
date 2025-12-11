/**
 * Admin Appointments Page
 * Manage all appointments
 */
import { useState, useEffect } from 'react';
import { appointmentsAPI } from '../../services/api';
import Card from '../../components/common/Card';
import Loading from '../../components/common/Loading';
import { format } from 'date-fns';

const AdminAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const response = await appointmentsAPI.getAllAppointments();
      setAppointments(response.data.appointments);
    } catch (err) {
      console.error('Failed to fetch appointments:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading fullScreen text="Loading appointments..." />;
  }

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 mb-8">All Appointments</h1>

        <Card padding="none">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-secondary-100">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-secondary-600 uppercase tracking-wider">
                    Client
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-secondary-600 uppercase tracking-wider">
                    Service
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-secondary-600 uppercase tracking-wider">
                    Date & Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-secondary-600 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-secondary-200">
                {appointments.map((appointment) => (
                  <tr key={appointment.id} className="hover:bg-secondary-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="font-medium text-secondary-900">{appointment.client?.name}</div>
                        <div className="text-sm text-secondary-600">{appointment.client?.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-secondary-900">{appointment.service?.name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-secondary-600">
                      {format(new Date(appointment.appointment_date), 'MMM d, yyyy')} at {appointment.appointment_time}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                        appointment.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        appointment.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {appointment.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdminAppointments;
