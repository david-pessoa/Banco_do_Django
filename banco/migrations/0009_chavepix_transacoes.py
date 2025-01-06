# Generated by Django 5.1.4 on 2024-12-30 20:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0008_delete_chavepix_delete_transacoes_usuario_cpf_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChavePIX',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('EMAIL', 'E-mail'), ('CPF', 'CPF'), ('CELULAR', 'Número de celular')], default='CPF', max_length=20, verbose_name='Tipo de chave PIX')),
                ('valor', models.CharField(max_length=30, verbose_name='Valor da chave PIX')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('SAQUE', 'Saque'), ('DEPOSITO', 'Depósito'), ('PAGAMENTO PIX', 'Pagamento PIX')], max_length=20, verbose_name='Tipo de transação')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Valor')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data e horário da transação')),
                ('chave_pix', models.CharField(default='', max_length=30, verbose_name='Chave pix do recebedor')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transacoes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
            },
        ),
    ]
