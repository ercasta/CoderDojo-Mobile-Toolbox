# Generated by Django 2.0.6 on 2018-07-13 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojomobile', '0004_auto_20180712_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1500)),
                ('event_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('uuid', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_checked_in', models.BooleanField(default=False)),
                ('uuid', models.CharField(max_length=200)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coderdojomobile.Event')),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coderdojomobile.Participant')),
            ],
        ),
    ]