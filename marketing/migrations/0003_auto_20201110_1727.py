# Generated by Django 3.1.2 on 2020-11-10 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_auto_20201110_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'ordering': ['order', '-start_date', '-end_date']},
        ),
        migrations.AddField(
            model_name='slider',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
