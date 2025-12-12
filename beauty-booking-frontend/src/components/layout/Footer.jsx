/**
 * Footer Component
 * Site footer with links and information
 */
import { Link } from 'react-router-dom';
import { useLanguage } from '../../contexts/LanguageContext';
import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  const { t } = useLanguage();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-secondary-900 text-secondary-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 gradient-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">B</span>
              </div>
              <span className="text-xl font-bold text-white">Beauty Salon</span>
            </div>
            <p className="text-sm text-secondary-400">
              {t('footer.brandDescription')}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">{t('footer.quickLinks')}</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-sm hover:text-primary-400 transition-colors">
                  {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-sm hover:text-primary-400 transition-colors">
                  {t('nav.services')}
                </Link>
              </li>
              <li>
                <Link to="/book" className="text-sm hover:text-primary-400 transition-colors">
                  {t('nav.bookAppointment')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">{t('footer.contactUs')}</h3>
            <ul className="space-y-3">
              <li className="flex items-start gap-2 text-sm">
                <MapPin className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <span>123 Beauty Street, New York, NY 10001</span>
              </li>
              <li className="flex items-center gap-2 text-sm">
                <Phone className="w-4 h-4 flex-shrink-0" />
                <a href="tel:+1234567890" className="hover:text-primary-400 transition-colors">
                  (123) 456-7890
                </a>
              </li>
              <li className="flex items-center gap-2 text-sm">
                <Mail className="w-4 h-4 flex-shrink-0" />
                <a href="mailto:info@beautysalon.com" className="hover:text-primary-400 transition-colors">
                  info@beautysalon.com
                </a>
              </li>
            </ul>
          </div>

          {/* Hours & Social */}
          <div>
            <h3 className="text-white font-semibold mb-4">{t('footer.hours')}</h3>
            <p className="text-sm mb-2">{t('footer.mondayFriday')}</p>
            <p className="text-sm mb-4">{t('footer.saturday')}</p>

            <h3 className="text-white font-semibold mb-3">{t('footer.followUs')}</h3>
            <div className="flex gap-3">
              <a
                href="#"
                className="w-8 h-8 rounded-full bg-secondary-800 hover:bg-primary-600 flex items-center justify-center transition-colors"
              >
                <Facebook className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-8 h-8 rounded-full bg-secondary-800 hover:bg-primary-600 flex items-center justify-center transition-colors"
              >
                <Instagram className="w-4 h-4" />
              </a>
              <a
                href="#"
                className="w-8 h-8 rounded-full bg-secondary-800 hover:bg-primary-600 flex items-center justify-center transition-colors"
              >
                <Twitter className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-secondary-800 text-center text-sm">
          <p>&copy; {currentYear} Beauty Salon. {t('footer.allRightsReserved')}</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
