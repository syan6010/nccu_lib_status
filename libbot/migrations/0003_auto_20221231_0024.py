# Generated by Django 3.1.13 on 2022-12-30 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libbot', '0002_auto_20221231_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='libState',
            field=models.TextField(choices=[('crowded', '擁擠'), ('free', '空閒')], default='free'),
        ),
    ]
