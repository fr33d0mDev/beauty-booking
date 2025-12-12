import { useLanguage } from '../contexts/LanguageContext';

const LanguageSelector = () => {
  const { language, toggleLanguage } = useLanguage();

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-1.5 rounded-lg border-2 border-secondary-200 hover:border-primary-400 hover:bg-primary-50 transition-all duration-200"
      aria-label="Toggle language"
      title={language === 'es' ? 'Cambiar a Inglés' : 'Switch to Spanish'}
    >
      {language === 'es' ? (
        <>
          <span className="text-xl">🇪🇸</span>
          <span className="text-sm font-semibold text-secondary-700">ES</span>
        </>
      ) : (
        <>
          <span className="text-xl">🇺🇸</span>
          <span className="text-sm font-semibold text-secondary-700">EN</span>
        </>
      )}
    </button>
  );
};

export default LanguageSelector;
