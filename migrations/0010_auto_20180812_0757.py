# Generated by Django 2.0.6 on 2018-08-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojomobile', '0009_auto_20180812_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='image',
            field=models.FileField(default=None, max_length=200, upload_to=''),
            preserve_default=False,
        ),
    ]
