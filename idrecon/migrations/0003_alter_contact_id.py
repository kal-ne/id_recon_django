# Generated by Django 5.0.4 on 2024-08-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idrecon', '0002_alter_contact_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]