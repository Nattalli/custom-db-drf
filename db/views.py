from rest_framework.response import Response
from .serializers import (
    ManagerSerializer,
    DatabaseSerializer,
    DatabaseCreateSerializer,
    TableSerializer,
    TableCreateSerializer,
    ColumnSerializer,
    ColumnCreateSerializer,
    RowSerializer,
    RowCreateSerializer
)
from rest_framework import generics, status, permissions
from .models import RowValue, Row, Table, Manager, Column, Database
from py_custom_db_drf.pagination import NewPagination


class ManagerListView(generics.ListAPIView):
    """
    Return a list of all created managers
    """

    serializer_class = ManagerSerializer
    queryset = Manager.objects.order_by("-id")
    pagination_class = NewPagination


class ManagerRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read, Update, Delete Manager by id
    """

    serializer_class = ManagerSerializer
    queryset = Manager.objects.order_by("-id")


class ManagerCreateView(generics.CreateAPIView):
    """
    Create new manager
    """

    serializer_class = ManagerSerializer
    queryset = Manager.objects.order_by("-id")


class DatabaseListView(generics.ListAPIView):
    """
    Return a list of all created databases
    """

    serializer_class = DatabaseSerializer
    queryset = Database.objects.order_by("-id")

    def list(self, request, *args, **kwargs):
        manager_pk = kwargs.get("manager_pk", None)
        if manager_pk:
            query = Database.objects.filter(manager__pk=manager_pk)
            page = self.paginate_queryset(query)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(
                {"message": "Should be manager pk in the path"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DatabaseCreateView(generics.CreateAPIView):
    """
    Create new database
    """

    serializer_class = DatabaseCreateSerializer
    queryset = Database.objects.all()

    def create(self, request, *args, **kwargs):
        manager_pk = kwargs.get("manager_pk", None)
        if manager_pk:
            db = Database.objects.create(
                name=request.data["name"], manager=Manager.objects.get(id=manager_pk)
            )
            return Response(
                self.get_serializer(db, many=False).data, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST
        )


class DatabaseRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read Update Delete Database
    """

    serializer_class = DatabaseSerializer
    queryset = Database.objects.all()


class TableListView(generics.ListAPIView):
    """
    Return a list of all created tables
    """

    serializer_class = TableSerializer
    queryset = Table.objects.order_by("-id")

    def list(self, request, *args, **kwargs):
        database_pk = kwargs.get("database_pk", None)
        if database_pk:
            query = Table.objects.filter(database__pk=database_pk)
            page = self.paginate_queryset(query)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(
                {"message": "Should be database pk in the path"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TableCreateView(generics.CreateAPIView):
    """
    Create new table
    """

    serializer_class = TableCreateSerializer
    queryset = Table.objects.all()

    def create(self, request, *args, **kwargs):
        database_pk = kwargs.get("database_pk", None)
        if database_pk:
            db = Table.objects.create(
                name=request.data["name"], database=Database.objects.get(id=database_pk)
            )
            return Response(
                self.get_serializer(db, many=False).data, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST
        )


class TableRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read Update Delete Table
    """

    serializer_class = TableSerializer
    queryset = Table.objects.all()


class ColumnCreatView(generics.CreateAPIView):
    """Create Column"""

    serializer_class = ColumnCreateSerializer
    queryset = Column.objects.all()

    def create(self, request, *args, **kwargs):
        table_pk = kwargs.get("table_pk", None)
        if table_pk:
            db = Column.objects.create(
                name=request.data["name"], type=request.data["type"], db=Table.objects.get(id=table_pk)
            )
            return Response(
                self.get_serializer(db, many=False).data, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST
        )


class ColumnListView(generics.ListAPIView):
    """
    Return a list of all created columns
    """

    serializer_class = ColumnSerializer
    queryset = Column.objects.order_by("-id")

    def list(self, request, *args, **kwargs):
        table_pk = kwargs.get("table_pk", None)
        if table_pk:
            query = Column.objects.filter(db__pk=table_pk)
            page = self.paginate_queryset(query)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(
                {"message": "Should be database pk in the path"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ColumnRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read Update Delete Column
    """

    serializer_class = ColumnSerializer
    queryset = Column.objects.all()


class RowListView(generics.ListAPIView):
    """
    Return a list of all created rows
    """

    serializer_class = RowSerializer
    queryset = Row.objects.order_by("-id")

    def list(self, request, *args, **kwargs):
        table_pk = kwargs.get("table_pk", None)
        if table_pk:
            query = Row.objects.filter(table__pk=table_pk)
            page = self.paginate_queryset(query)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(
                {"message": "Should be database pk in the path"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RowRUDView(generics.RetrieveUpdateDestroyAPIView):
    """
    Read Update Delete Row
    """
    serializer_class = RowSerializer
    queryset = Row.objects.all()


class RowCreateView(generics.CreateAPIView):
    """
    Create new row
    """
    queryset = Row.objects.all()
    serializer_class = RowCreateSerializer

    def create(self, request, *args, **kwargs):
        table_pk = kwargs.get("table_pk", None)
        if table_pk:
            row = Row.objects.create(
                table=Table.objects.get(id=table_pk)
            )
            row_values = request.data["row_values"]
            print(row_values)

            for value in row_values:
                print(value)
                RowValue.objects.create(value=value, row_id=row.id)

            return Response(
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST
        )
