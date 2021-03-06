# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-04 08:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import markymark.fields


class Migration(migrations.Migration):

    dependencies = [
        ('legaltext', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalTextCheckbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markymark.fields.MarkdownField(help_text='You can use [anchor]Your text[/anchor] to create a link to the full legal text. If you use [anchor:foo]Your text[/anchor] the link will go to the block "foo" inside the legal text.', verbose_name='Text')),
            ],
            options={
                'verbose_name_plural': 'Legal text Checkboxes',
                'ordering': ('legaltext_version',),
                'verbose_name': 'Legal text checkbox',
            },
        ),
        migrations.AddField(
            model_name='legaltextcheckbox',
            name='legaltext_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkboxes', to='legaltext.LegalTextVersion', verbose_name='Legal text version'),
        ),
    ]
