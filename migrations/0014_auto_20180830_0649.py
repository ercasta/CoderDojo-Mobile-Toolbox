# Generated by Django 2.0.6 on 2018-08-30 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojomobile', '0013_auto_20180830_0631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waiver',
            name='data_di_consegna',
        ),
        migrations.AlterField(
            model_name='waiver',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='waiver',
            name='sign_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
