from django.urls import path, include
from .views import (
    ManagerListView,
    ManagerRUDView,
    ManagerCreateView,
    DatabaseListView,
    DatabaseCreateView,
    DatabaseRUDView,
    TableListView,
)

table_api = [
    path("table/", TableListView.as_view(), name="column-list")
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
