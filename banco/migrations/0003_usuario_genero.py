# Generated by Django 5.1.4 on 2024-12-13 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0002_genero_usuario_cpf_usuario_endereco_usuario_saldo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='genero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='banco.genero'),
        ),
    ]
