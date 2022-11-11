from rest_framework.response import Response
from .serializers import (
    ManagerSerializer,
    DatabaseSerializer,
    DatabaseCreateSerializer,
    TableSerializer,
    TableCreateSerializer,
    ColumnSerializer,
    ColumnCreateSerializer,
    ColumnSwapSerializer,
    RowSerializer,
    RowCreateSerializer
)
from rest_framework import generics, status
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


class ColumnSwapView(generics.GenericAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSwapSerializer

    def get(self, request, *args, **kwargs):
        query = Column.objects.filter(db__pk=kwargs.get("table_pk", None))
        serializer = self.get_serializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        column_1 = Column.objects.get(pk=request.data["pk"])
        column_2 = Column.objects.get(pk=request.data["name"])
        column_1_name = column_1.name
        column_2_name = column_2.name

        if column_2 == column_1:
            return Response(
                {"message": "You can't swap the same column"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        column_1_count = 0
        column_2_count = 0
        counter = 0

        for column in Column.objects.all():
            if column == column_1:
                column_1_count = counter
            if column == column_2:
                column_2_count = counter
            counter += 1

        column_1.name = "c123a"
        column_2.name = "s123b"
        column_1.save()
        column_2.save()

        column_1.type, column_2.type = column_2.type, column_1.type
        column_1.name = column_2_name
        column_2.name = column_1_name

        column_1.save()
        column_2.save()

        print(column_1.name)
        print(column_2.name)

        column_1.refresh_from_db()
        column_2.refresh_from_db()
        rows = Row.objects.filter(table__id=column_1.db_id)
        for r in rows:
            row_values = list(RowValue.objects.filter(row_id=r.id))
            row_values[column_1_count].value, row_values[column_2_count].value = row_values[column_2_count].value, row_values[column_1_count].value
            row_values[column_1_count].save()
            row_values[column_2_count].save()

        serializer = ColumnSerializer([column_1, column_2], many=True)
        return Response(serializer.data)


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


def validate_row_value(value, column_type):

    if column_type == 0:
        if type(value) != int:
            return False

    elif column_type == 1:
        if not float(value):
            return False

    elif column_type == 2:
        if type(value) != str or len(value) != 1:
            return False

    elif column_type == 3:
        if type(value) != str:
            return False

    elif column_type == 4:
        open_tag = value.count("<")
        close_tag = value.count(">")
        if type(value) != str or open_tag != close_tag or open_tag == 0 or close_tag == 0:
            return False

    elif column_type == 5:
        if type(value) != list or type(list(value)[0]) != str or type(list(value)[1]) != str:
            return False

        if list(value)[0] > list(value)[1]:
            return False

    return True


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

            columns = Column.objects.filter(db__id=row.table_id)
            column_types = [column.type for column in columns]
            counter = 0
            can_be_created = True

            for value in row_values:
                column_type = column_types[counter]
                can_be_created = validate_row_value(value, column_type)
                counter += 1

            if can_be_created:
                for value in row_values:
                    RowValue.objects.create(value=value, row_id=row.id)

                return Response(
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "Invalid row values!"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"message": "Something went wrong!"}, status=status.HTTP_400_BAD_REQUEST
        )
