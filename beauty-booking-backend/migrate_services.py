"""
Script to add multi-language support to services table
Run this script to add description_en and description_es columns
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)

# SQL migration
migration_sql = """
-- Add new columns for multi-language descriptions
ALTER TABLE services
ADD COLUMN IF NOT EXISTS description_en TEXT,
ADD COLUMN IF NOT EXISTS description_es TEXT;

-- Migrate existing data: copy description to description_en
UPDATE services
SET description_en = description
WHERE description IS NOT NULL AND description_en IS NULL;
"""

# Sample service translations in Spanish
sample_translations = {
    'Haircut': 'Corte de cabello profesional y estilizado personalizado para tu look perfecto',
    'Hair Coloring': 'Color de cabello profesional con productos de alta calidad',
    'Manicure': 'Servicio completo de manicura para uñas hermosas y saludables',
    'Pedicure': 'Servicio de pedicura relajante con tratamiento de spa para pies',
    'Facial Treatment': 'Tratamiento facial profesional para rejuvenecer y refrescar tu piel',
    'Facial': 'Tratamiento facial profesional para rejuvenecer y refrescar tu piel',
    'Massage': 'Masaje terapéutico profesional para relajación y bienestar',
    'Makeup': 'Servicio profesional de maquillaje para cualquier ocasión especial',
    'Waxing': 'Servicio de depilación con cera profesional y productos de calidad',
    'Nail Art': 'Arte en uñas creativo y diseños personalizados',
    'Hair Extensions': 'Extensiones de cabello de alta calidad para mayor volumen y longitud',
    'Eyebrow Shaping': 'Diseño y modelado profesional de cejas',
    'Eyelash Extensions': 'Extensiones de pestañas profesionales para una mirada impactante',
}

try:
    print("Starting migration...")

    with engine.connect() as conn:
        # Execute migration
        print("Adding columns...")
        conn.execute(text(migration_sql))
        conn.commit()
        print("[OK] Columns added successfully")

        # Get all services
        print("\nFetching services...")
        result = conn.execute(text("SELECT id, name FROM services"))
        services = result.fetchall()

        # Update Spanish translations
        print(f"\nUpdating Spanish translations for {len(services)} services...")
        for service_id, name in services:
            if name in sample_translations:
                spanish_desc = sample_translations[name]
                update_sql = text("""
                    UPDATE services
                    SET description_es = :desc_es
                    WHERE id = :id AND description_es IS NULL
                """)
                conn.execute(update_sql, {'desc_es': spanish_desc, 'id': service_id})
                print(f"  [OK] Updated '{name}' with Spanish translation")

        conn.commit()

        print("\n[SUCCESS] Migration completed successfully!")
        print("\nSummary:")
        print("- Added description_en column")
        print("- Added description_es column")
        print("- Migrated existing descriptions to description_en")
        print(f"- Added Spanish translations for {len(sample_translations)} services")

except Exception as e:
    print(f"\n[ERROR] Error during migration: {str(e)}")
    exit(1)
finally:
    engine.dispose()
