# Generated by Django 4.0.4 on 2022-08-15 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_api.rareuser')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_api.post')),
            ],
        ),
    ]
