/**
 * Admin Services Page
 * Manage services (simplified version)
 */
import { useState, useEffect } from 'react';
import { servicesAPI } from '../../services/api';
import Card from '../../components/common/Card';
import Loading from '../../components/common/Loading';

const AdminServices = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      const response = await servicesAPI.getAll(false);
      setServices(response.data.services);
    } catch (err) {
      console.error('Failed to fetch services:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading fullScreen text="Loading services..." />;
  }

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 mb-8">Services Management</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service) => (
            <Card key={service.id} padding="lg">
              <h3 className="text-xl font-bold text-secondary-900 mb-2">{service.name}</h3>
              <p className="text-secondary-600 mb-4 line-clamp-2">{service.description}</p>
              <div className="flex items-center justify-between text-sm">
                <span className="text-secondary-700">${service.price}</span>
                <span className="text-secondary-700">{service.duration} min</span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  service.active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                }`}>
                  {service.active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminServices;
