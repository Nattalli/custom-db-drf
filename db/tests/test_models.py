from django.test import TestCase
from db.models import Manager, Database, Table, Column, Row, RowValue


class TestManager(TestCase):
    def test_managers_manager_created(self) -> None:
        Manager.objects.create(name="First")
        Manager.objects.create(name="Second")
        self.assertEqual(Manager.objects.count(), 2)

    def test_managers_ordered_by_id_desc(self) -> None:
        Manager.objects.create(name="First")
        Manager.objects.create(name="Second")
        self.assertEqual(Manager.objects.first().name, "Second")
        self.assertEqual(Manager.objects.last().name, "First")

    def test_manager_str(self) -> None:
        self.manager = Manager.objects.create(name="First")
        self.assertEqual(str(self.manager), "First")


class TestDatabase(TestCase):
    def setUp(self) -> None:
        self.manager = Manager.objects.create(name="Test")

    def test_db_created_with_correct_data(self) -> None:
        Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.assertEqual(Database.objects.count(), 1)

    def test_db_deletes_if_manager_deleted(self) -> None:
        Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.assertEqual(Database.objects.count(), 1)
        self.manager.delete()
        self.assertEqual(Database.objects.count(), 0)

    def test_dbs_ordered_by_id_desc(self) -> None:
        Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        Database.objects.create(
            manager=self.manager,
            name="Test db 2"
        )
        self.assertEqual(Database.objects.first().name, "Test db 2")
        self.assertEqual(Database.objects.last().name, "Test db")

    def test_db_str(self) -> None:
        self.db = Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.assertEqual(str(self.db), f"{self.manager.name}'s database {self.db.name}")


class TestTable(TestCase):
    def setUp(self) -> None:
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="Test db"
        )

    def test_table_creates(self) -> None:
        Table.objects.create(
            database=self.db,
            name="Test table"
        )
        self.assertEqual(Table.objects.count(), 1)
        self.assertEqual(Table.objects.first().name, "Test table")

    def test_str_without_columns(self) -> None:
        self.table = Table.objects.create(
            database=self.db,
            name="Test table"
        )
        self.assertEqual(str(self.table), f"{self.table.name}: []")

    def test_str_with_columns_data(self) -> None:
        self.table = Table.objects.create(
            database=self.db,
            name="Test table"
        )
        Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        Column.objects.create(
            name="Second",
            type=3,
            db=self.table
        )
        self.assertEqual(str(self.table), f"{self.table.name}: ['int', 'str']")

    def test_tables_ordered_by_id_desc(self) -> None:
        Table.objects.create(
            database=self.db,
            name="Test table"
        )
        Table.objects.create(
            database=self.db,
            name="Test table 2"
        )
        self.assertEqual(Table.objects.first().name, "Test table 2")
        self.assertEqual(Table.objects.last().name, "Test table")


class TestColumn(TestCase):
    def setUp(self) -> None:
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.table = Table.objects.create(
            database=self.db,
            name="Test table"
        )

    def test_column_creates(self):
        Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.assertEqual(Column.objects.count(), 1)

    def test_column_str(self):
        self.column = Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.assertEqual(str(self.column), f"'Test table' table: First - int")

    def test_column_deletes_with_table(self):
        self.column = Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.assertEqual(Column.objects.count(), 1)
        self.table.delete()
        self.assertEqual(Column.objects.count(), 0)


class TestRow(TestCase):
    def setUp(self) -> None:
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.table = Table.objects.create(
            database=self.db,
            name="Test table"
        )

    def test_row_creates(self) -> None:
        Row.objects.create(
            table=self.table
        )
        self.assertEqual(Row.objects.count(), 1)

    def test_row_str_without_values(self):
        self.row = Row.objects.create(
            table=self.table
        )
        self.assertEqual(str(self.row), "[]")

    def test_row_str_with_values(self):
        self.column = Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.column = Column.objects.create(
            name="Second",
            type=2,
            db=self.table
        )
        self.row = Row.objects.create(
            table=self.table
        )
        RowValue.objects.create(
            row=self.row,
            value=1
        )
        RowValue.objects.create(
            row=self.row,
            value='a'
        )
        self.assertEqual(str(self.row), "['1', 'a']")
