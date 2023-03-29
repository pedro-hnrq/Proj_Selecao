# Generated by Django 4.1.7 on 2023-03-29 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('prioridade', models.CharField(choices=[('B', 'Baixa'), ('A', 'Alta'), ('U', 'Urgente')], max_length=1)),
                ('data', models.DateField()),
                ('realizada', models.BooleanField(default=False)),
                ('vaga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.vagas')),
            ],
        ),
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
