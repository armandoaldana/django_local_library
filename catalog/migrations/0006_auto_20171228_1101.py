# Generated by Django 2.0 on 2017-12-28 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20171228_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned_1', 'Libro retornado'),)},
        ),
    ]