# Generated by Django 4.2.1 on 2023-05-23 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmentation', '0004_plotimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='segmentedcustomer',
            name='email',
            field=models.EmailField(default='khairahmed@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='segmentedcustomer',
            name='name',
            field=models.CharField(default='Khair Ahmed', max_length=255),
            preserve_default=False,
        ),
    ]
