# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markymark.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckboxTextVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', markymark.fields.MarkdownField(help_text='Use [[word]] to indicate the word used as a link to the legaltext content.', verbose_name='Text')),
                ('anchor', models.CharField(blank=True, max_length=64, verbose_name='Anchor')),
            ],
            options={
                'ordering': ('legaltext_version',),
                'verbose_name': 'Checkbox',
                'verbose_name_plural': 'Checkboxes',
            },
        ),
        migrations.CreateModel(
            name='LegalText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Legal text')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='Slug')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Legal text',
                'verbose_name_plural': 'Legal texts',
            },
        ),
        migrations.CreateModel(
            name='LegalTextVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Valid from')),
                ('content', markymark.fields.MarkdownField(help_text='Optional: use [[checkbox-anchor-name]] text ... [[end]] to insert checkbox anchor', verbose_name='Text')),
                ('legaltext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legaltext.LegalText', verbose_name='Legal text')),
            ],
            options={
                'ordering': ('legaltext__slug', '-valid_from'),
                'verbose_name': 'Legal text version',
                'verbose_name_plural': 'Legal text versions',
            },
        ),
        migrations.AddField(
            model_name='checkboxtextversion',
            name='legaltext_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='legaltext.LegalTextVersion', verbose_name='Legal text version'),
        ),
    ]
