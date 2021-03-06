# Generated by Django 2.2.1 on 2019-09-17 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='account.UserProfileInfo'),
        ),
        migrations.AlterField(
            model_name='case',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='account.UserProfileInfo2'),
        ),
        migrations.AlterField(
            model_name='schedules',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc', to='account.UserProfileInfo'),
        ),
    ]
