from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Manager, Database, Table, Column, Row, RowValue


admin.site.register(Manager)
admin.site.register(Database)
admin.site.register(Column)


class RowValueAdmin(admin.StackedInline):
    model = RowValue
    extra = 10


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


# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ("name", "url", "email", "phone")
#     list_filter = ("categories__name", )
#     search_fields = ("name", "email")
#     list_display_links = ("url", "name")
#     fieldsets = [
#         ('Main information', {'fields': ['logo', 'name', 'url', 'address', 'email', 'phone', 'description', 'categories']}),
#         ('Media', {'fields': ('image1', 'image2', 'image3', 'image4', 'video', 'video_url')}),
#         # ('Video', {'fields': }),
#     ]
#
#
# @admin.register(CategoryBlock)
# class CompanyAdmin(admin.ModelAdmin):
#     search_fields = ("name", )
#
#
# @admin.register(Partner)
# class PartnerAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ('url', 'logo')})
#     ]

admin.site.unregister(Group)
admin.site.unregister(User)
