from rest_framework import serializers
from .models import RowValue, Row, Table, Manager, Column, Database


class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manager
        fields = '__all__'


class DatabaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Database
        fields = '__all__'


class DatabaseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Database
        fields = "__all__"
        read_only_fields = ("manager",)


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = '__all__'
