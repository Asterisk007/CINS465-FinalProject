# Generated by Django 2.2.5 on 2020-05-05 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20200505_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussionthread',
            name='topic',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
