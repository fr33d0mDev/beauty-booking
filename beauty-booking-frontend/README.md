# Beauty Booking Frontend

React-based frontend for a beauty salon appointment booking system with AI chatbot integration.

## Features

- Modern, responsive UI built with React 18 and Tailwind CSS
- User authentication and role-based access (Client/Admin)
- Service browsing and booking
- Interactive appointment calendar
- Real-time availability checking
- Admin dashboard with statistics
- AI-powered chatbot assistance (Claude)
- Mobile-first responsive design

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library
- **date-fns** - Date manipulation

## Prerequisites

- Node.js 16+ and npm
- Backend API running (see backend README)

## Installation

```bash
# Navigate to frontend directory
cd beauty-booking-frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Configure .env with your API URL (default: http://localhost:5000/api)
```

## Development

```bash
# Start development server
npm run dev

# The app will be available at http://localhost:5173
```

## Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
beauty-booking-frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   │   ├── common/       # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Modal.jsx
│   │   │   └── Loading.jsx
│   │   ├── layout/       # Layout components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Layout.jsx
│   │   └── ProtectedRoute.jsx
│   ├── contexts/         # React contexts
│   │   └── AuthContext.jsx
│   ├── pages/            # Page components
│   │   ├── public/       # Public pages
│   │   │   ├── Landing.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── Services.jsx
│   │   ├── client/       # Client pages
│   │   │   ├── Dashboard.jsx
│   │   │   ├── BookAppointment.jsx
│   │   │   └── MyAppointments.jsx
│   │   └── admin/        # Admin pages
│   │       ├── Dashboard.jsx
│   │       ├── Appointments.jsx
│   │       ├── Services.jsx
│   │       └── Clients.jsx
│   ├── services/         # API services
│   │   └── api.js
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Key Features

### Public Pages

- **Landing Page** - Hero section, features, and call-to-action
- **Services** - Browse available beauty services
- **Login/Register** - User authentication

### Client Features

- **Dashboard** - Overview of upcoming appointments
- **Book Appointment** - Interactive booking with date/time selection
- **My Appointments** - View and cancel appointments

### Admin Features

- **Dashboard** - Statistics and appointment overview
- **Appointments** - Manage all appointments
- **Services** - Service management
- **Clients** - Client list and management

## Environment Variables

Create a `.env` file in the root directory:

```env
# API URL - Backend server address
VITE_API_URL=http://localhost:5000/api
```

## Routing

- `/` - Landing page (public)
- `/services` - Services catalog (public)
- `/login` - Login page (public)
- `/register` - Registration page (public)
- `/dashboard` - Client dashboard (protected)
- `/book` - Book appointment (protected)
- `/my-appointments` - My appointments (protected)
- `/admin/dashboard` - Admin dashboard (admin only)
- `/admin/appointments` - Manage appointments (admin only)
- `/admin/services` - Manage services (admin only)
- `/admin/clients` - Manage clients (admin only)

## Authentication

The app uses JWT tokens stored in localStorage. Protected routes automatically redirect unauthenticated users to `/login`.

### Demo Accounts

After running backend seed command:

**Admin Account:**
- Email: `admin@beautysalon.com`
- Password: `admin123`

**Client Account:**
- Email: `client@example.com`
- Password: `client123`

## Components

### Common Components

- **Button** - Reusable button with variants (primary, secondary, outline, ghost, danger)
- **Input** - Form input with label, error handling, and icons
- **Card** - Container with shadow and hover effects
- **Modal** - Dialog/modal component
- **Loading** - Loading spinner

### Context

- **AuthContext** - Global authentication state management

## API Integration

All API calls are centralized in `src/services/api.js`:

```javascript
import { authAPI, servicesAPI, appointmentsAPI } from './services/api';

// Example usage
const response = await servicesAPI.getAll();
```

## Styling

The project uses Tailwind CSS with custom configuration:

- **Primary color** - Pink (#ec4899)
- **Secondary color** - Gray (#64748b)
- **Custom utilities** - Transitions, gradients, shadows

## Development Tips

1. **Hot Module Replacement (HMR)** - Changes reflect instantly during development
2. **React DevTools** - Install browser extension for debugging
3. **Tailwind IntelliSense** - VS Code extension for class autocomplete
4. **ESLint** - Configured for React best practices

## Common Issues

### API Connection Errors

Ensure the backend server is running on the correct port (default: 5000)

### CORS Errors

The backend CORS configuration must include the frontend URL (`http://localhost:5173`)

### Build Errors

Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Future Enhancements

- [ ] Add AI chatbot component
- [ ] Implement real-time notifications
- [ ] Add email confirmations
- [ ] Implement payment processing
- [ ] Add service reviews and ratings
- [ ] Multi-language support
- [ ] Dark mode toggle

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT

## Support

For issues and questions, please check the backend README or create an issue on GitHub.
