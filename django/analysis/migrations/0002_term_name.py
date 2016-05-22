# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='name',
            field=models.CharField(max_length=127, null=True, verbose_name='\u671f\u9593\u540d'),
        ),
    ]
