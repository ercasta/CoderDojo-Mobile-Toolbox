# Generated by Django 2.0.6 on 2018-07-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderdojomobile', '0005_event_participant_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningmaterial',
            name='resources',
            field=models
            .ManyToManyField(
                            null=True,
                            related_name='_learningmaterial_resources_+',
                            to='coderdojomobile.GenericUserFile'
                            ),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='uuid',
            field=models.CharField(max_length=1500),
        ),
    ]
