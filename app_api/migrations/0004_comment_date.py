# Generated by Django 4.0.4 on 2022-08-15 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0003_merge_0002_comment_0002_tag_posttag'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateField(default='2022-09-01'),
            preserve_default=False,
        ),
    ]