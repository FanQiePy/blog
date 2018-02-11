# -*- coding: utf-8 -*-
import csv
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
project = os.path.dirname(pwd)
workspace = os.path.dirname(project)
sys.path.append(project)
sys.path.append(workspace)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
import django
django.setup()

from mycrawl.models import House5i5j
# windows
# data_file = os.path.join(workspace, 'media\data\house_pandas.csv')
# linux
data_file = os.path.join(workspace, 'media/data/house_pandas.csv')

with open(data_file, encoding='utf-8') as f:
    data = csv.DictReader(f)
    fields = [x for x in data.fieldnames]
    for piece in data:
        instance = House5i5j(**piece)
        instance.save()
f.close()

