# Generated by Django 5.1.7 on 2025-04-29 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_categorymapping_remove_reconciliation_cat_list_c_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reconciliation',
            unique_together={('sales_data', 'description', 'amount')},
        ),
    ]
