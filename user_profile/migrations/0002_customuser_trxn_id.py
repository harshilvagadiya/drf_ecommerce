# Generated by Django 4.2.3 on 2023-08-11 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='trxn_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
