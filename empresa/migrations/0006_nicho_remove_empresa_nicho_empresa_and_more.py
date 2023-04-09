# Generated by Django 4.1.7 on 2023-04-04 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0005_remove_empresa_nicho_mercado_empresa_nicho_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nicho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nicho', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='nicho_empresa',
        ),
        migrations.AddField(
            model_name='empresa',
            name='nicho_empresa',
            field=models.ManyToManyField(to='empresa.nicho'),
        ),
    ]