from unittest import TestCase
from django_mock_queries.asserts import assert_serializer
from db.models import Manager
from db.serializers import (
    ManagerSerializer
)


class TestSerializer(TestCase):
    def test_manager_serializer_fields(self):
        manager = Manager(id=1, name="Test")

        values = {"id": manager.id, "name": manager.name}

        assert_serializer(ManagerSerializer).instance(manager).returns("id", "name").values(
            **values
        ).mocks("make").run()
