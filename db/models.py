from django.db import models


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


class Table(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("-id", )


class Column(models.Model):
    COLUMN_TYPES = [
        (0, "int"),
        (1, "real"),
        (2, "char"),
        (3, "str"),
        (4, "html"),
        (5, "strInvl")
    ]
    name = models.CharField(max_length=255, unique=True)
    type = models.IntegerField(choices=COLUMN_TYPES)
    db = models.ForeignKey(Table, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-id", )

    def __str__(self) -> str:
        return f"{[item.value for item in RowValue.objects.filter(row__id=self.id)]}"


class RowValue(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    value = models.TextField()
