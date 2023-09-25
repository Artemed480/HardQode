from rest_framework import serializers
from .models import *


class ViewingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Viewing
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
