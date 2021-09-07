# Generated by Django 2.2.19 on 2021-09-05 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20210905_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='delegate_persons',
            field=models.ManyToManyField(through='api.AccessPrivilege', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accessprivilege',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Company'),
        ),
        migrations.AlterField(
            model_name='accessprivilege',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]