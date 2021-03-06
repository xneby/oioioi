# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-16 19:12
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import oioioi.base.utils.validators
import oioioi.participants.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OIRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('postal_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(b'^\\d{2}-\\d{3}$', 'Enter a postal code in the format XX-XXX')], verbose_name='postal code')),
                ('city', models.CharField(max_length=100, verbose_name='city')),
                ('phone', models.CharField(blank=True, max_length=64, null=True, validators=[django.core.validators.RegexValidator(b'\\+?[0-9() -]{6,}', 'Invalid phone number')], verbose_name='phone number')),
                ('birthday', models.DateField(verbose_name='birth date')),
                ('birthplace', models.CharField(max_length=255, verbose_name='birthplace')),
                ('t_shirt_size', models.CharField(choices=[(b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'XXL', b'XXL')], max_length=7, verbose_name='t-shirt size')),
                ('class_type', models.CharField(choices=[(b'1LO', b'pierwsza szko\xc5\x82y ponadgimnazjalnej'), (b'2LO', b'druga szko\xc5\x82y ponadgimnazjalnej'), (b'3LO', b'trzecia szko\xc5\x82y ponadgimnazjalnej'), (b'4LO', b'czwarta szko\xc5\x82y ponadgimnazjalnej'), (b'5LO', b'pi\xc4\x85ta szko\xc5\x82y ponadgimnazjalnej'), (b'1G', b'pierwsza gimnazjum'), (b'2G', b'druga gimnazjum'), (b'3G', b'trzecia gimnazjum'), (b'1SP', b'pierwsza szko\xc5\x82y podstawowej'), (b'2SP', b'druga szko\xc5\x82y podstawowej'), (b'3SP', b'trzecia szko\xc5\x82y podstawowej'), (b'4SP', b'czwarta szko\xc5\x82y podstawowej'), (b'5SP', b'pi\xc4\x85ta szko\xc5\x82y podstawowej'), (b'6SP', b'sz\xc3\xb3sta szko\xc5\x82y podstawowej'), (b'7SP', b'si\xc3\xb3dma szko\xc5\x82y podstawowej'), (b'8SP', b'\xc3\xb3sma szko\xc5\x82y podstawowej')], max_length=7, verbose_name='class')),
                ('terms_accepted', models.BooleanField(default=False, verbose_name='terms accepted')),
                ('participant', oioioi.participants.fields.OneToOneBothHandsCascadingParticipantField(on_delete=django.db.models.deletion.CASCADE, related_name='oi_oiregistration', to='participants.Participant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[oioioi.base.utils.validators.validate_whitespaces], verbose_name='name')),
                ('address', models.CharField(max_length=255, verbose_name='address')),
                ('postal_code', models.CharField(db_index=True, max_length=6, validators=[django.core.validators.RegexValidator(b'^\\d{2}-\\d{3}$', 'Enter a postal code in the format XX-XXX')], verbose_name='postal code')),
                ('city', models.CharField(db_index=True, max_length=100, verbose_name='city')),
                ('province', models.CharField(choices=[('dolno\u015bl\u0105skie', 'dolno\u015bl\u0105skie'), ('kujawsko-pomorskie', 'kujawsko-pomorskie'), ('lubelskie', 'lubelskie'), ('lubuskie', 'lubuskie'), ('\u0142\xf3dzkie', '\u0142\xf3dzkie'), ('ma\u0142opolskie', 'ma\u0142opolskie'), ('mazowieckie', 'mazowieckie'), ('opolskie', 'opolskie'), ('podkarpackie', 'podkarpackie'), ('podlaskie', 'podlaskie'), ('pomorskie', 'pomorskie'), ('\u015bl\u0105skie', '\u015bl\u0105skie'), ('\u015bwi\u0119tokrzyskie', '\u015bwi\u0119tokrzyskie'), ('warmi\u0144sko-mazurskie', 'warmi\u0144sko-mazurskie'), ('wielkopolskie', 'wielkopolskie'), ('zachodniopomorskie', 'zachodniopomorskie')], db_index=True, max_length=100, verbose_name='province')),
                ('phone', models.CharField(blank=True, max_length=64, null=True, validators=[django.core.validators.RegexValidator(b'\\+?[0-9() -]{6,}', 'Invalid phone number')], verbose_name='phone number')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_approved', models.BooleanField(default=True, verbose_name='approved')),
            ],
            options={
                'ordering': ['province', 'city', 'address', 'name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='school',
            unique_together=set([('name', 'postal_code')]),
        ),
        migrations.AlterIndexTogether(
            name='school',
            index_together=set([('city', 'is_active'), ('province', 'is_active')]),
        ),
        migrations.AddField(
            model_name='oiregistration',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='oi.School', verbose_name='school'),
        ),
    ]
