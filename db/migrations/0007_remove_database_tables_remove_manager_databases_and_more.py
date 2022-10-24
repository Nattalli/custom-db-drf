# Generated by Django 4.1.2 on 2022-10-24 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_remove_row_values_rowvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='tables',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='databases',
        ),
        migrations.AddField(
            model_name='database',
            name='manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.manager'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='database',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='table',
            name='database',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='db.database'),
            preserve_default=False,
        ),
    ]