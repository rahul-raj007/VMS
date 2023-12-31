# Generated by Django 5.0 on 2023-12-07 12:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseordermodel",
            name="delivery_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="purchaseordermodel",
            name="issue_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="purchaseordermodel",
            name="po_number",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="purchaseordermodel",
            name="quality_rating",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="purchaseordermodel",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
