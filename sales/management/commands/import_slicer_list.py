import pandas as pd
from django.core.management.base import BaseCommand

from sales.models import SlicerList


class Command(BaseCommand):
    help = "Import slicer list data from an Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="The path to the Excel file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        self.stdout.write(self.style.NOTICE(f"Reading data from {file_path}..."))

        try:
            df = pd.read_excel(file_path, engine="openpyxl")  # Read Excel file
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading the Excel file: {e}"))
            return

        # Check if 'Slicer_List' column exists
        if "Slicer_List" not in df.columns:
            self.stdout.write(self.style.ERROR("Column 'Slicer_List' not found in the Excel file."))
            return

        imported_count = 0
        for index, row in df.iterrows():
            try:
                slicer_name = str(row["Slicer_List"]).strip()  # Convert to string and remove extra spaces
                if slicer_name:  # Avoid empty rows
                    SlicerList.objects.get_or_create(name=slicer_name)
                    imported_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing row {index + 1}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {imported_count} records!"))


# Run the file
# python manage.py import_slicer_list "E:\Documents\eAccountExpert\reconcilation\Slicer_List.xlsx"
