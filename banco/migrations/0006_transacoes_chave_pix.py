# Generated by Django 5.1.4 on 2024-12-17 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0005_usuario_senha_pix'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacoes',
            name='chave_pix',
            field=models.CharField(default='', max_length=30, verbose_name='Chave pix do recebedor'),
        ),
    ]
