# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-16 19:12
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import oioioi.base.fields
import oioioi.filetracker.fields
import oioioi.problems.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='full name')),
                ('short_name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='short name')),
                ('controller_name', oioioi.base.fields.DottedNameField(choices=[(b'dummy', b'Dummy')], superclass=b'oioioi.problems.controllers.ProblemController', verbose_name='type')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('package_backend_name', oioioi.base.fields.DottedNameField(blank=True, choices=[(b'dummy', b'Dummy')], null=True, superclass=b'oioioi.problems.package.ProblemPackageBackend', verbose_name='package type')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('contest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.Contest', verbose_name='contest')),
            ],
            options={
                'verbose_name': 'problem',
                'verbose_name_plural': 'problems',
                'permissions': (('problems_db_admin', 'Can administer the problems database'), ('problem_admin', 'Can administer the problem')),
            },
        ),
        migrations.CreateModel(
            name='ProblemAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('content', oioioi.filetracker.fields.FileField(max_length=255, upload_to=oioioi.problems.models.make_problem_filename, verbose_name='content')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='problems.Problem')),
            ],
            options={
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
        ),
        migrations.CreateModel(
            name='ProblemPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_file', oioioi.filetracker.fields.FileField(max_length=255, upload_to=oioioi.problems.models._make_package_filename, verbose_name='package')),
                ('problem_name', models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='problem name')),
                ('celery_task_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('info', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Package information')),
                ('traceback', oioioi.filetracker.fields.FileField(blank=True, max_length=255, null=True, upload_to=oioioi.problems.models._make_package_filename, verbose_name='traceback')),
                ('status', oioioi.base.fields.EnumField(default=b'?', max_length=64, verbose_name='status')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('contest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.Contest', verbose_name='contest')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='created by')),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='problems.Problem', verbose_name='problem')),
            ],
            options={
                'ordering': ['-creation_date'],
                'verbose_name': 'problem package',
                'verbose_name_plural': 'problem packages',
            },
        ),
        migrations.CreateModel(
            name='ProblemSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_key', models.CharField(max_length=40, unique=True)),
                ('problem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
            ],
            options={
                'verbose_name': 'problem site',
                'verbose_name_plural': 'problem sites',
            },
        ),
        migrations.CreateModel(
            name='ProblemStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(blank=True, max_length=6, null=True, verbose_name='language code')),
                ('content', oioioi.filetracker.fields.FileField(max_length=255, upload_to=oioioi.problems.models.make_problem_filename, verbose_name='content')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements', to='problems.Problem')),
            ],
            options={
                'verbose_name': 'problem statement',
                'verbose_name_plural': 'problem statements',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(20), django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='name')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='TagThrough',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='MainProblemInstance',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contests.probleminstance',),
        ),
        migrations.AddField(
            model_name='tag',
            name='problems',
            field=models.ManyToManyField(through='problems.TagThrough', to='problems.Problem'),
        ),
        migrations.AddField(
            model_name='problem',
            name='main_problem_instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_problem_instance', to='contests.ProblemInstance', verbose_name='main problem instance'),
        ),
        migrations.CreateModel(
            name='ContestProblemPackage',
            fields=[
            ],
            options={
                'verbose_name': 'Contest Problem Package',
                'proxy': True,
            },
            bases=('problems.problempackage',),
        ),
        migrations.AlterUniqueTogether(
            name='tagthrough',
            unique_together=set([('problem', 'tag')]),
        ),
    ]
