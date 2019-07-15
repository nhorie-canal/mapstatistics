# Generated by Django 2.2.3 on 2019-07-14 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map1.Person'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map1.Manager'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map1.Person'),
        ),
    ]
