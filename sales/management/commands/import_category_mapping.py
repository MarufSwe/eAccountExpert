import pandas as pd
from django.core.management.base import BaseCommand
from sales.models import CategoryMapping


class Command(BaseCommand):
    help = "Import CategoryMapping data from Excel with enhanced validation"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        clear_existing = kwargs.get('clear', False)
        
        self.stdout.write(self.style.NOTICE(f"📁 Reading data from: {file_path}"))
        
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading Excel file: {e}"))
            return

        # Expected columns: Slicer_List, Cat_List_d, Cat_List_c
        required_cols = ['Slicer_List', 'Cat_List_d', 'Cat_List_c']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            self.stdout.write(self.style.ERROR(f"❌ Missing columns: {', '.join(missing_cols)}"))
            self.stdout.write(self.style.NOTICE(f"Available columns: {list(df.columns)}"))
            return

        # Clear existing data if requested
        if clear_existing:
            deleted_count = CategoryMapping.objects.all().count()
            CategoryMapping.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"🗑️ Cleared {deleted_count} existing records"))

        # Filter out empty rows
        df_clean = df.dropna(subset=required_cols)
        df_clean = df_clean[
            (df_clean['Slicer_List'].str.strip() != '') &
            (df_clean['Cat_List_d'].str.strip() != '') &
            (df_clean['Cat_List_c'].str.strip() != '')
        ]

        count_created = 0
        count_updated = 0
        count_skipped = 0

        for _, row in df_clean.iterrows():
            slicer = str(row['Slicer_List']).strip()
            cat_d = str(row['Cat_List_d']).strip()
            cat_c = str(row['Cat_List_c']).strip()

            if slicer and cat_d and cat_c:
                obj, created = CategoryMapping.objects.update_or_create(
                    slicer_list=slicer,
                    defaults={'cat_list_d': cat_d, 'cat_list_c': cat_c}
                )
                
                if created:
                    count_created += 1
                else:
                    count_updated += 1
            else:
                count_skipped += 1

        # Summary
        self.stdout.write(self.style.SUCCESS(f"✅ Import completed!"))
        self.stdout.write(self.style.SUCCESS(f"   📝 Created: {count_created} records"))
        self.stdout.write(self.style.SUCCESS(f"   🔄 Updated: {count_updated} records"))
        if count_skipped > 0:
            self.stdout.write(self.style.WARNING(f"   ⏭️ Skipped: {count_skipped} records (empty data)"))
        
        total_records = CategoryMapping.objects.count()
        self.stdout.write(self.style.SUCCESS(f"   📊 Total records in database: {total_records}"))


# Usage Examples:
# python manage.py import_category_mapping '/path/to/category-mapping-data.xlsx'
# python manage.py import_category_mapping '/path/to/category-mapping-data.xlsx' --clear