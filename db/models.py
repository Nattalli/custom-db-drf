from django.core.exceptions import ValidationError
from django.db import models

COLUMN_TYPES = [
        (0, "int"),
        (1, "real"),
        (2, "char"),
        (3, "str"),
        (4, "html"),
        (5, "strInvl")
    ]


class Manager(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("-id", )


class Database(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.manager.name}'s database {self.name}"

    class Meta:
        ordering = ("-id", )


class Column(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.IntegerField(choices=COLUMN_TYPES)
    db = models.ForeignKey("Table", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"'{self.db.name}' table: {self.name} - {[type_[1] for type_ in COLUMN_TYPES if type_[0] == self.type][0]}"


class Table(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.name}: {[[type_[1] for type_ in COLUMN_TYPES if type_[0]==column.type][0] for column in Column.objects.filter(db__id=self.id)]}"

    class Meta:
        ordering = ("-id", )


class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-id", )

    def __str__(self) -> str:
        return f"{[item.value for item in RowValue.objects.filter(row__id=self.id)]}"


class RowValue(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    value = models.TextField()
