# Generated by Django 2.2.4 on 2019-11-11 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20191105_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StoreTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Store')),
                ('t_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.HashTag')),
            ],
        ),
    ]