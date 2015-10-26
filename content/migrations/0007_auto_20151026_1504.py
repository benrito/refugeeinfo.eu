# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_authorizationtoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locationcontent',
            old_name='google_doc',
            new_name='html_url',
        ),
    ]
