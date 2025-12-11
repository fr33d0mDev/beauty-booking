/**
 * Admin Dashboard
 * Overview of appointments and statistics
 */
import { useState, useEffect } from 'react';
import { appointmentsAPI } from '../../services/api';
import { Calendar, DollarSign, Users, CheckCircle } from 'lucide-react';
import Card from '../../components/common/Card';
import Loading from '../../components/common/Loading';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await appointmentsAPI.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading fullScreen text="Loading dashboard..." />;
  }

  const statCards = [
    {
      title: 'Today\'s Appointments',
      value: stats?.today || 0,
      icon: Calendar,
      color: 'bg-blue-500',
    },
    {
      title: 'Upcoming This Week',
      value: stats?.upcoming_week || 0,
      icon: Users,
      color: 'bg-green-500',
    },
    {
      title: 'Completed',
      value: stats?.by_status?.completed || 0,
      icon: CheckCircle,
      color: 'bg-purple-500',
    },
    {
      title: 'Total Revenue',
      value: `$${stats?.total_revenue?.toFixed(2) || '0.00'}`,
      icon: DollarSign,
      color: 'bg-primary-500',
    },
  ];

  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 mb-8">Admin Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((stat, index) => (
            <Card key={index} padding="lg">
              <div className="flex items-center gap-4">
                <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                  <stat.icon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <p className="text-sm text-secondary-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-secondary-900">{stat.value}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>

        {/* Status Breakdown */}
        <Card padding="lg">
          <h2 className="text-2xl font-bold text-secondary-900 mb-6">Appointment Status</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats?.by_status && Object.entries(stats.by_status).map(([status, count]) => (
              <div key={status} className="text-center p-4 bg-secondary-50 rounded-lg">
                <p className="text-3xl font-bold text-primary-600">{count}</p>
                <p className="text-sm text-secondary-600 capitalize">{status}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;
