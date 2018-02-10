# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import House5i5j


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House5i5j
        fields = '__all__'
        read_only_fields = ['city', 'area', 'house_type',
                            'layout', 'square', 'price', 'put_date', 'address', 'house_url']
