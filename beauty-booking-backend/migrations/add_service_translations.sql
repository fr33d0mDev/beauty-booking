-- Migration: Add multi-language support to services table
-- Description: Adds description_en and description_es columns for service translations
-- Date: 2025-12-11

-- Add new columns for multi-language descriptions
ALTER TABLE services
ADD COLUMN IF NOT EXISTS description_en TEXT,
ADD COLUMN IF NOT EXISTS description_es TEXT;

-- Migrate existing data: copy description to description_en (assuming current data is in English)
UPDATE services
SET description_en = description
WHERE description IS NOT NULL AND description_en IS NULL;

-- Add comments to document the columns
COMMENT ON COLUMN services.description IS 'Legacy description field - kept for backward compatibility';
COMMENT ON COLUMN services.description_en IS 'Service description in English';
COMMENT ON COLUMN services.description_es IS 'Service description in Spanish';

-- Sample translations for existing services (update as needed)
-- Uncomment and modify these based on your actual service data:

/*
UPDATE services SET
  description_es = 'Corte de cabello profesional y estilizado personalizado para tu look perfecto'
WHERE name = 'Haircut' AND description_es IS NULL;

UPDATE services SET
  description_es = 'Color de cabello profesional con productos de alta calidad'
WHERE name = 'Hair Coloring' AND description_es IS NULL;

UPDATE services SET
  description_es = 'Servicio completo de manicura para uñas hermosas y saludables'
WHERE name = 'Manicure' AND description_es IS NULL;

UPDATE services SET
  description_es = 'Servicio de pedicura relajante con tratamiento de spa para pies'
WHERE name = 'Pedicure' AND description_es IS NULL;

UPDATE services SET
  description_es = 'Tratamiento facial profesional para rejuvenecer y refrescar tu piel'
WHERE name = 'Facial Treatment' AND description_es IS NULL;

UPDATE services SET
  description_es = 'Masaje terapéutico profesional para relajación y bienestar'
WHERE name = 'Massage' AND description_es IS NULL;
*/
