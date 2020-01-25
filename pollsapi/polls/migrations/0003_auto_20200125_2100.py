# Generated by Django 2.0.13 on 2020-01-25 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_auto_20200125_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_votes', to='polls.Poll'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('poll', 'voted_by')},
        ),
    ]