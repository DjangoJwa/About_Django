# Generated by Django 2.1.3 on 2018-11-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('text', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
