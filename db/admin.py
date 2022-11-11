from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Manager, Database, Table, Column, Row, RowValue, StatisticInfo


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
class RowAdmin(admin.ModelAdmin):
    inlines = [RowValueAdmin]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ColumnAdmin]


@admin.register(StatisticInfo)
class StatisticInfoAdmin(admin.ModelAdmin):
    list_filter = ("table__name",)
    list_display = ("table_name", "time", "row_amount", "column_amount")
    readonly_fields = ("time",)
    list_display_links = ("table_name", "time")

    @admin.display()
    def table_name(self, obj):
        return obj.table.name


admin.site.unregister(Group)
admin.site.unregister(User)
