# Generated by Django 4.2.1 on 2023-05-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsubcategory',
            name='parent_category',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_cat',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sub_cat',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='ProductSubCategory',
        ),
    ]
