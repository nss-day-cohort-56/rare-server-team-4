# Generated by Django 4.1 on 2022-08-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0013_merge_0010_merge_20220818_1948_0012_deactivate'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='unsubscribed_at',
            field=models.DateTimeField(null=True),
        ),
    ]