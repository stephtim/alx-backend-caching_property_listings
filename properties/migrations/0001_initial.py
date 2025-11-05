"""Initial migration for properties app."""
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('location', models.CharField(max_length=200)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('square_feet', models.IntegerField()),
                ('property_type', models.CharField(choices=[
                    ('house', 'House'),
                    ('apartment', 'Apartment'),
                    ('condo', 'Condo'),
                    ('townhouse', 'Townhouse')
                ], max_length=50)),
                ('status', models.CharField(choices=[
                    ('available', 'Available'),
                    ('sold', 'Sold'),
                    ('pending', 'Pending')
                ], default='available', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Properties',
                'ordering': ['-created_at'],
            },
        ),
    ]