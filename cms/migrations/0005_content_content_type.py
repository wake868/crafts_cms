# Generated by Django 2.1.2 on 2018-10-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20181016_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.CharField(default='IMAGE', max_length=15),
            preserve_default=False,
        ),
    ]
