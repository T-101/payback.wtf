# Generated by Django 5.1.1 on 2024-09-18 22:40

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payback', '0007_alter_questionnaire_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='paybackuser',
            name='user_id_short',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, include_digits=False, length=8, lowercase=True),
        ),
    ]
