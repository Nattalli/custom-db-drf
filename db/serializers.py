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


class TableCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ("database",)


class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = '__all__'


class ColumnSwapSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class ColumnCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = '__all__'
        read_only_fields = ("db",)


class RowValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = RowValue
        fields = '__all__'


class RowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Row
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(RowSerializer, self).to_representation(instance)
        rep["row_values"] = [value.value for value in RowValue.objects.filter(row__id=instance.id)]
        return rep


class RowCreateSerializer(serializers.ModelSerializer):
    row_values = serializers.ListField()

    class Meta:
        model = Row
        fields = ("row_values", "table")
        read_only_fields = ("table",)
