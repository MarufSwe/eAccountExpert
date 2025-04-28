import pandas as pd
from django.core.management.base import BaseCommand

from sales.models import CategoryMapping


class Command(BaseCommand):
    help = "Import CategoryMapping data from an Excel file"

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

        # Check if required columns exist
        required_columns = {"Slicer_List", "Cat_List_d", "Cat_List_c"}
        if not required_columns.issubset(df.columns):
            self.stdout.write(self.style.ERROR(
                f"Missing one or more required columns: {', '.join(required_columns)}"
            ))
            return

        imported_count = 0
        for index, row in df.iterrows():
            try:
                slicer_list = str(row["Slicer_List"]).strip()
                cat_list_d = str(row["Cat_List_d"]).strip()
                cat_list_c = str(row["Cat_List_c"]).strip()

                # Avoid empty rows
                if slicer_list and cat_list_d and cat_list_c:
                    CategoryMapping.objects.get_or_create(
                        slicer_list=slicer_list,
                        cat_list_d=cat_list_d,
                        cat_list_c=cat_list_c
                    )
                    imported_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing row {index + 1}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {imported_count} records!"))


# Run the file
# python manage.py import_slicer_list "E:\Documents\eAccountExpert\reconcilation\category_mapping.xlsx"
