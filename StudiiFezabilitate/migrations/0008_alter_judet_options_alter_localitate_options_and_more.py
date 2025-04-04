# Generated by Django 5.1.5 on 2025-02-15 14:07

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudiiFezabilitate', '0007_localitate_tip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judet',
            options={'ordering': ['nume'], 'verbose_name': 'Județ', 'verbose_name_plural': 'Județe'},
        ),
        migrations.AlterModelOptions(
            name='localitate',
            options={'ordering': ['nume'], 'verbose_name': 'Localitate', 'verbose_name_plural': 'Localități'},
        ),
        migrations.AlterField(
            model_name='inginer',
            name='numar_ci',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Numărul CI trebuie să conțină exact 6 cifre', regex='^[0-9]{6}$')]),
        ),
        migrations.AlterField(
            model_name='persoanacontact',
            name='numar_ci',
            field=models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.RegexValidator(message='Numărul CI trebuie să conțină exact 6 cifre', regex='^[0-9]{6}$')]),
        ),
        migrations.CreateModel(
            name='Aviz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('descriere', models.TextField()),
                ('judet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='avize', to='StudiiFezabilitate.judet')),
            ],
        ),
        migrations.CreateModel(
            name='UAT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=100)),
                ('adresa', models.CharField(blank=True, max_length=512, null=True)),
                ('cod_postal', models.CharField(blank=True, max_length=6, null=True)),
                ('telefon', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('cont_trezorerie', models.CharField(blank=True, max_length=30, null=True)),
                ('judet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='UAT', to='StudiiFezabilitate.judet')),
                ('localitate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='UAT', to='StudiiFezabilitate.localitate')),
            ],
            options={
                'verbose_name': 'Unitate administrativ teritorială',
                'verbose_name_plural': 'Unități administrativ teritoriale',
            },
        ),
        migrations.CreateModel(
            name='CertificatUrbanism',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numar', models.CharField(max_length=100)),
                ('data', models.DateField()),
                ('valabilitate', models.DateField()),
                ('descrierea_proiectului', models.TextField()),
                ('suprafata_ocupata', models.IntegerField(blank=True, null=True)),
                ('lungime_traseu', models.IntegerField(blank=True, null=True)),
                ('cale_CU', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_plan_incadrare_CU', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_plan_situatie_CU', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_acte_beneficiar', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_acte_facturare', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_chitanta_APM', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_plan_situatie_PDF', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_plan_topo_DWG', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_extrase_CF', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_aviz_GIS', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_ATR', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_aviz_CTE', models.CharField(blank=True, max_length=512, null=True)),
                ('cale_chitanta_DSP', models.CharField(blank=True, max_length=512, null=True)),
                ('inginer_intocmit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificat_urbanism_intocmit', to='StudiiFezabilitate.inginer')),
                ('inginer_verificat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificat_urbanism_verificat', to='StudiiFezabilitate.inginer')),
                ('lucrare', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='certificat_urbanism', to='StudiiFezabilitate.lucrare')),
                ('emitent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='StudiiFezabilitate.uat')),
            ],
            options={
                'verbose_name': 'Certificat de urbanism',
                'verbose_name_plural': 'Certificate de urbanism',
            },
        ),
        migrations.CreateModel(
            name='AvizeCU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depus', models.BooleanField(default=False)),
                ('data_depunere', models.DateField(blank=True, null=True)),
                ('primit', models.BooleanField(default=False)),
                ('numar_aviz', models.CharField(blank=True, max_length=100, null=True)),
                ('data_aviz', models.DateField(blank=True, null=True)),
                ('cale_aviz', models.CharField(max_length=512)),
                ('descriere_aviz', models.TextField(blank=True, null=True)),
                ('cost_net', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('cost_tva', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('cost_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('nume_aviz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificat_avize', to='StudiiFezabilitate.aviz')),
                ('certificat_urbanism', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='avize_certificat', to='StudiiFezabilitate.certificaturbanism')),
            ],
            options={
                'verbose_name': 'Aviz',
                'verbose_name_plural': 'Avize',
                'unique_together': {('certificat_urbanism', 'nume_aviz')},
            },
        ),
    ]
