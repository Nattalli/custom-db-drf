from django.urls import path, include
from .views import (
    ManagerListView,
    ManagerRUDView,
    ManagerCreateView,
    DatabaseListView,
    DatabaseCreateView,
    DatabaseRUDView,
    TableListView,
    TableCreateView,
    TableRUDView,
    ColumnListView,
    ColumnCreatView,
    ColumnSwapView,
    ColumnRUDView,
    RowListView,
    RowRUDView,
    RowCreateView
)

row_api = [
    path("row/", RowListView.as_view(), name="row-list"),
    path("row/create/", RowCreateView.as_view(), name="row-create"),
    path("row/<int:pk>/", RowRUDView.as_view(), name="row-rud"),
]

column_api = [
    path("column/", ColumnListView.as_view(), name="column-list"),
    path("column/create/", ColumnCreatView.as_view(), name="column-create"),
    path("column/swap/", ColumnSwapView.as_view(), name="column-swap"),
    path("column/<int:pk>/", ColumnRUDView.as_view(), name="column-rud"),
]

table_api = [
    path("table/", TableListView.as_view(), name="table-list"),
    path("table/create/", TableCreateView.as_view(), name="table-create"),
    path("table/<int:pk>/", TableRUDView.as_view(), name="table-rud"),
    path("table/<int:table_pk>/", include(column_api)),
    path("table/<int:table_pk>/", include(row_api))
]

database_api = [
    path("database/", DatabaseListView.as_view(), name="database-list"),
    path("database/create/", DatabaseCreateView.as_view(), name="database-create"),
    path("database/<int:pk>/", DatabaseRUDView.as_view(), name="database-rud"),
    path("database/<int:database_pk>/", include(table_api)),
]

urlpatterns = [
    path("manager/", ManagerListView.as_view(), name="managers-list"),
    path("manager/create/", ManagerCreateView.as_view(), name="managers-create"),
    path("manager/<int:pk>/", ManagerRUDView.as_view(), name="manager-rud"),
    path("manager/<int:manager_pk>/", include(database_api)),
]
app_name = "db"
