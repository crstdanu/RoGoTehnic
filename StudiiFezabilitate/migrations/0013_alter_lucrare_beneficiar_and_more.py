# Generated by Django 5.1.5 on 2025-02-27 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudiiFezabilitate', '0012_alter_certificaturbanism_inginer_intocmit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lucrare',
            name='beneficiar',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lucrari', to='StudiiFezabilitate.beneficiar'),
        ),
        migrations.AlterField(
            model_name='lucrare',
            name='firma_proiectare',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lucrari', to='StudiiFezabilitate.firmaproiectare'),
        ),
    ]
