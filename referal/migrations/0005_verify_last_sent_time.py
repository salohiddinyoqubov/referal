# Generated by Django 4.2.7 on 2023-12-03 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referal', '0004_alter_referal_invited_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='verify',
            name='last_sent_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
