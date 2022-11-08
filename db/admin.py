from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Manager, Database, Table, Column, Row, RowValue


admin.site.register(Manager)
admin.site.register(Database)
admin.site.register(Column)


class RowValueAdmin(admin.StackedInline):
    model = RowValue
    extra = 3


class ColumnAdmin(admin.StackedInline):
    model = Column
    extra = 10


@admin.register(Row)
class TableAdmin(admin.ModelAdmin):
    inlines = [RowValueAdmin]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ColumnAdmin]


admin.site.unregister(Group)
admin.site.unregister(User)
