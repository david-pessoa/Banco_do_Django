# Generated by Django 5.1.4 on 2024-12-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0004_transacoes'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='senha_pix',
            field=models.CharField(default='', max_length=19, verbose_name='Senha do pix'),
        ),
    ]
