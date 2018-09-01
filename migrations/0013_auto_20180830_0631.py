# Generated by Django 2.0.6 on 2018-08-30 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojomobile', '0012_operatingsystems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid', models.BooleanField()),
                ('sign_date', models.DateField(null=True)),
                ('expiry_date', models.DateField(null=True)),
                ('allows_photos', models.BooleanField()),
                ('data_di_consegna', models.DateField(null=True)),
                ('scanned_image', models.FileField(max_length=200, null=True, upload_to='waivers/')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='waiver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='participant', to='coderdojomobile.Waiver'),
        ),
    ]
