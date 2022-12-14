# Generated by Django 3.2.15 on 2022-11-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20221017_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address_line1',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line2',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Vendor'), (2, 'Customer')], null=True),
        ),
    ]
