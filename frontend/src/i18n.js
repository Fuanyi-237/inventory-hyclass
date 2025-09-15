import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Detect language from browser, fallback to English
const resources = {
  en: { translation: require('./locales/en/translation.json') },
  fr: { translation: require('./locales/fr/translation.json') },
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('lang') || 'en',
    fallbackLng: 'en',
    interpolation: { escapeValue: false },
  });

export default i18n;
