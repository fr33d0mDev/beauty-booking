"""
Script to add multi-language support for service names
Run this script to add name_en and name_es columns
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
-- Add new columns for multi-language names
ALTER TABLE services
ADD COLUMN IF NOT EXISTS name_en VARCHAR(100),
ADD COLUMN IF NOT EXISTS name_es VARCHAR(100);

-- Migrate existing data: copy name to name_en
UPDATE services
SET name_en = name
WHERE name IS NOT NULL AND name_en IS NULL;
"""

# Service name translations
name_translations = {
    'Haircut': 'Corte de Cabello',
    'Hair Coloring': 'Coloración de Cabello',
    'Manicure': 'Manicura',
    'Pedicure': 'Pedicura',
    'Facial Treatment': 'Tratamiento Facial',
    'Facial': 'Facial',
    'Massage': 'Masaje',
    'Makeup': 'Maquillaje',
    'Waxing': 'Depilación',
    'Nail Art': 'Arte en Uñas',
    'Hair Extensions': 'Extensiones de Cabello',
    'Eyebrow Shaping': 'Diseño de Cejas',
    'Eyelash Extensions': 'Extensiones de Pestañas',
    'Deep Tissue Massage': 'Masaje de Tejido Profundo',
    'Swedish Massage': 'Masaje Sueco',
    'Hot Stone Massage': 'Masaje con Piedras Calientes',
    'Aromatherapy Massage': 'Masaje de Aromaterapia',
    'Hair Styling': 'Peinado',
    'Highlights': 'Mechas',
    'Balayage': 'Balayage',
    'Brazilian Blowout': 'Alisado Brasileño',
    'Keratin Treatment': 'Tratamiento de Keratina',
    'Bridal Makeup': 'Maquillaje de Novia',
    'Special Occasion Makeup': 'Maquillaje para Ocasiones Especiales',
}

try:
    print("Starting name translation migration...")

    with engine.connect() as conn:
        # Execute migration
        print("Adding name columns...")
        conn.execute(text(migration_sql))
        conn.commit()
        print("[OK] Columns added successfully")

        # Get all services
        print("\nFetching services...")
        result = conn.execute(text("SELECT id, name FROM services"))
        services = result.fetchall()

        # Update Spanish name translations
        print(f"\nUpdating Spanish name translations for {len(services)} services...")
        updated_count = 0
        for service_id, name in services:
            if name in name_translations:
                spanish_name = name_translations[name]
                update_sql = text("""
                    UPDATE services
                    SET name_es = :name_es
                    WHERE id = :id AND name_es IS NULL
                """)
                conn.execute(update_sql, {'name_es': spanish_name, 'id': service_id})
                print(f"  [OK] '{name}' -> '{spanish_name}'")
                updated_count += 1
            else:
                print(f"  [SKIP] No translation found for '{name}'")

        conn.commit()

        print(f"\n[SUCCESS] Migration completed successfully!")
        print("\nSummary:")
        print("- Added name_en column")
        print("- Added name_es column")
        print("- Migrated existing names to name_en")
        print(f"- Added Spanish translations for {updated_count} services")

except Exception as e:
    print(f"\n[ERROR] Error during migration: {str(e)}")
    exit(1)
finally:
    engine.dispose()
