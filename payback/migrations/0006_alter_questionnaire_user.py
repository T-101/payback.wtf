# Generated by Django 5.1.1 on 2024-09-18 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payback', '0005_alter_paybackuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='payback.paybackuser'),
        ),
    ]
