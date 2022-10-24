# Generated by Django 4.1.2 on 2022-10-24 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_remove_table_rows_row_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='type',
            field=models.IntegerField(choices=[(0, 'int'), (1, 'real'), (2, 'char'), (3, 'str'), (4, 'html'), (5, 'strInvl')], max_length=255),
        ),
    ]