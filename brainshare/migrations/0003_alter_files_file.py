# Generated by Django 4.1.1 on 2024-01-21 11:33

import brainshare.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brainshare', '0002_alter_files_created_alter_folder_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.FileField(blank=True, upload_to=brainshare.models.get_upload_path),
        ),
    ]
