from .models import StatisticInfo, Row, Table, Column


def create_new_record_to_statistic_table():
    for table in Table.objects.all():
        StatisticInfo.objects.create(
            table=table,
            row_amount=Row.objects.filter(table__id=table.id).count(),
            column_amount=Column.objects.filter(db__id=table.id).count()
        )
