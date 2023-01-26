# Generated by Django 3.2.12 on 2023-01-26 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0004_vagas_email'),
        ('vagas', '0002_rename_taref_tarefa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assunto', models.CharField(max_length=100)),
                ('corpo', models.TextField()),
                ('enviado', models.BooleanField()),
                ('vaga', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresa.vagas')),
            ],
        ),
    ]