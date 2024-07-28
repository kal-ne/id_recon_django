# Generated by Django 5.0.4 on 2024-07-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('linked_id', models.IntegerField(blank=True, null=True)),
                ('link_precedence', models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary')], max_length=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]