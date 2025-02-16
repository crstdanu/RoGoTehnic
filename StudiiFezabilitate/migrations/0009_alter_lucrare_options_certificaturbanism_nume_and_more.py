# Generated by Django 5.1.5 on 2025-02-16 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudiiFezabilitate', '0008_alter_judet_options_alter_localitate_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lucrare',
            options={'ordering': ['nume_intern'], 'verbose_name': 'Lucrare', 'verbose_name_plural': 'Lucrări'},
        ),
        migrations.AddField(
            model_name='certificaturbanism',
            name='nume',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='lucrare',
            name='nume',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
