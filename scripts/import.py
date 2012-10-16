#!/usr/bin/env python
# -*- coding: utf-8 -*-   
import os
import sys
from django.utils.timezone import utc
from django.template.defaultfilters import slugify
from unidecode import unidecode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mikran_com.settings")

import django
from legacy.models import LegacyMain
from mshop.models import MikranProduct

import datetime

o = LegacyMain.objects.using('legacy_mikran').all()
#o = LegacyMain.objects.using('legacy_mikran').filter(id=1829)
for item in o:
    #print item.id,item.name_L0
    p = MikranProduct()
    p.id = item.id
    p.name = item.name_L0
    p.name_pl = item.name_L0
    if item.xml_description_L0 is not None:
        p.description_pl = item.xml_description_L0
    else:
        p.description_pl = ''
    
    if item.active is not None:
        p.active = item.active
    else:
        p.active = False
    p.vat = item.vat

    #p.native_price = 0
    p.native_price = item.price_brutto/((p.vat/100) + 1)
    p.price = p.native_price
    p.unit_price = p.native_price

    p.slug = item.id
    print "--------------------------"
    print p.name
    print unidecode(p.name)
    if len(p.name) > 0:
        p.slug = slugify(unidecode(p.name))
        slug_count = MikranProduct.objects.filter(slug=p.slug).exclude(id=p.id).count()
        print slug_count
        if slug_count >= 1:
            p.slug = p.slug + ",#" + str(p.id)
            print p.slug
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print p.slug
    print "--------------------------"

    p.date_added = datetime.datetime.utcnow().replace(tzinfo=utc)
    #p.date_added = datetime.datetime.now()
    try:
        p.save()
    except:
        raise
        print "--------------------------"
        print "Exception"
        print item.id
        print "--------------------------"
