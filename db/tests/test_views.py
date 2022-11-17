import json
from django import test
from mock import MagicMock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from mock import patch
from django_mock_queries.query import MockSet, MockModel
from django.contrib.auth.backends import ModelBackend
from db.models import Manager, Database, Table, Column, Row, RowValue


def active_users():
    return get_user_model().objects.filter(is_active=True)


class TestApi(TestCase):
    users = MockSet()
    user_objects = patch('django.contrib.auth.models.User.objects', users)

    @user_objects
    def test_api_active_users_filters_by_is_active_true(self):
        self.users.add(
            MockModel(mock_name='active user', is_active=True),
            MockModel(mock_name='inactive user', is_active=False)
        )

        for user in active_users():
            assert user.is_active


class BackendsTests(test.TestCase):

    def setUp(self):
        self.backend = ModelBackend()
        self.username = "Test"
        self.password = "zal;ksmdasklmd"

    def test_authenticate_using_email_and_phone_number(self):
        user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            is_active=True,
        )

        self.assertTrue(self.backend.user_can_authenticate(user))
        self.assertFalse(self.backend.user_can_authenticate(MagicMock(is_active=False)))


class TestManagerUrls(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='testpassword'
        )
        Manager.objects.create(name="First")
        Manager.objects.create(name="Second")

    @patch('db.views.ManagerListView')
    def test_manager_list_response(self, mock_get):
        mock_get.return_value = [{"id": 2, "name": "Second"}, {"id": 1, "name": "First"}]
        url = reverse("db:managers-list")
        response = self.client.get(url)
        self.assertEqual(response.data["results"], mock_get.return_value)

    def test_manager_list_and_pagination(self) -> None:
        url = reverse("db:managers-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 2)

    def test_manager_create(self) -> None:
        url = reverse("db:managers-create")
        resp = self.client.post(
            url,
            data={"name": "Third"}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Manager.objects.count(), 3)
        self.assertEqual(Manager.objects.get(pk=3).name, "Third")

    def test_manager_update(self) -> None:
        self.manager = Manager.objects.first()
        url = reverse("db:manager-rud", args=[self.manager.pk])
        resp = self.client.put(url, content_type='application/json', data=json.dumps({"name": "New name"}))
        self.manager.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.manager.name, "New name")

    def test_manager_delete(self) -> None:
        self.manager = Manager.objects.first()
        url = reverse("db:manager-rud", args=[self.manager.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Manager.objects.count(), 1)

    def test_manager_read(self) -> None:
        self.manager = Manager.objects.first()
        url = reverse("db:manager-rud", args=[self.manager.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["id"], self.manager.pk)
        self.assertEqual(resp.data["name"], "Second")


class TestDatabaseUrls(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='testpassword'
        )
        self.manager = Manager.objects.create(name="Test")
        self.db_1 = Database.objects.create(
            manager=self.manager,
            name="First db"
        )
        self.db_2 = Database.objects.create(
            manager=self.manager,
            name="Second db"
        )

    def test_database_list_and_pagination(self) -> None:
        url = reverse("db:database-list", args=[self.manager.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 2)

    def test_database_create(self) -> None:
        url = reverse("db:database-create", args=[self.manager.pk])
        resp = self.client.post(
            url,
            data={"name": "Third db", "manager": self.manager}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Database.objects.count(), 3)
        self.assertEqual(Database.objects.get(pk=3).name, "Third db")

    def test_database_delete(self) -> None:
        url = reverse("db:database-rud", args=[self.manager.pk, self.db_1.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Database.objects.count(), 1)

    def test_database_read(self) -> None:
        url = reverse("db:database-rud", args=[self.manager.pk, self.db_2.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["id"], self.db_2.pk)
        self.assertEqual(resp.data["name"], "Second db")


class TestTableUrls(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='testpassword'
        )
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="First db"
        )
        self.table_1 = Table.objects.create(
            database=self.db,
            name="First table"
        )
        self.table_2 = Table.objects.create(
            database=self.db,
            name="Second table"
        )

    def test_table_list_and_pagination(self) -> None:
        url = reverse("db:table-list", args=[self.manager.pk, self.db.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 2)

    def test_table_create(self) -> None:
        url = reverse("db:table-create", args=[self.manager.pk, self.db.pk])
        resp = self.client.post(
            url,
            data={"name": "Third table", "database": self.db}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Table.objects.count(), 3)
        self.assertEqual(Table.objects.get(pk=3).name, "Third table")

    def test_table_delete(self) -> None:
        url = reverse("db:table-rud", args=[self.manager.pk, self.db.pk, self.table_1.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Table.objects.count(), 1)

    def test_table_read(self) -> None:
        url = reverse("db:table-rud", args=[self.manager.pk, self.db.pk, self.table_2.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["id"], self.table_2.pk)
        self.assertEqual(resp.data["name"], "Second table")


class TestColumnUrls(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='testpassword'
        )
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="Test db"
        )
        self.table = Table.objects.create(
            database=self.db,
            name="Test table"
        )
        self.column_1 = Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.column_2 = Column.objects.create(
            name="Second",
            type=2,
            db=self.table
        )

    def test_column_list_and_pagination(self) -> None:
        url = reverse("db:column-list", args=[self.manager.pk, self.db.pk, self.table.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 2)

    def test_column_create(self) -> None:
        url = reverse("db:column-create", args=[self.manager.pk, self.db.pk, self.table.pk])
        resp = self.client.post(
            url,
            data={"name": "Third column", "db": self.table, "type": 1}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Column.objects.count(), 3)
        self.assertEqual(Column.objects.get(pk=3).name, "Third column")

    def test_column_delete(self) -> None:
        url = reverse("db:column-rud", args=[self.manager.pk, self.db.pk, self.table.pk, self.column_1.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Column.objects.count(), 1)

    def test_column_read(self) -> None:
        url = reverse("db:column-rud", args=[self.manager.pk, self.db.pk, self.table.pk, self.column_1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["id"], self.column_1.pk)
        self.assertEqual(resp.data["name"], "First")

    def test_column_swap(self) -> None:
        url = reverse("db:column-swap", args=[self.manager.pk, self.db.pk, self.table.pk])
        resp = self.client.post(
            url,
            data={"pk": 1, "name": 2}
        )
        self.column_1.refresh_from_db()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual("Second", self.column_1.name)


class TestRowUrls(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='test_user',
            password='testpassword'
        )
        self.manager = Manager.objects.create(name="Test")
        self.db = Database.objects.create(
            manager=self.manager,
            name="First db"
        )
        self.table = Table.objects.create(
            database=self.db,
            name="First table"
        )
        self.column_1 = Column.objects.create(
            name="First",
            type=0,
            db=self.table
        )
        self.column_2 = Column.objects.create(
            name="Second",
            type=2,
            db=self.table
        )
        self.row_1 = Row.objects.create(
            table=self.table
        )
        self.row_2 = Row.objects.create(
            table=self.table
        )
        RowValue.objects.create(
            row=self.row_1,
            value=1
        )
        RowValue.objects.create(
            row=self.row_2,
            value=15
        )
        RowValue.objects.create(
            row=self.row_1,
            value="a"
        )
        RowValue.objects.create(
            row=self.row_2,
            value="b"
        )

    def test_row_list_and_pagination(self) -> None:
        url = reverse("db:row-list", args=[self.manager.pk, self.db.pk, self.table.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["total_count"], 2)

    def test_row_delete(self) -> None:
        url = reverse("db:row-rud", args=[self.manager.pk, self.db.pk, self.table.pk, self.row_1.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(Row.objects.count(), 1)

    def test_row_read(self) -> None:
        url = reverse("db:row-rud", args=[self.manager.pk, self.db.pk, self.table.pk, self.row_1.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["id"], 1)
