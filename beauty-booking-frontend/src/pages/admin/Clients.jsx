/**
 * Admin Clients Page
 * View all registered clients (simplified)
 */
import Card from '../../components/common/Card';

const AdminClients = () => {
  return (
    <div className="min-h-screen bg-secondary-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 mb-8">Clients</h1>
        <Card padding="xl">
          <p className="text-secondary-600 text-center">
            Client management feature coming soon. You can extend this page to list and manage clients.
          </p>
        </Card>
      </div>
    </div>
  );
};

export default AdminClients;
