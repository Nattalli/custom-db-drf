from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RowValue, Column

COLUMN_TYPES = [
    (0, "int"),
    (1, "real"),
    (2, "char"),
    (3, "str"),
    (4, "html"),
    (5, "strInvl")
]


@receiver(post_save, sender=RowValue)
def validate_row_values(sender, instance, created, **kwargs):
    if created:
        row_values = RowValue.objects.filter(row__id=instance.row.id)
        columns = Column.objects.filter(db__id=instance.row.table_id)
        column_types = [column.type for column in columns]
        column_type = column_types[row_values.count() - 1]
        value = instance.value

        if column_type == 0:
            assert int(value), TypeError(f"Row value should be Integer, now it has "
                                         f"{type(instance.value)} type!")

        elif column_type == 1:
            assert float(value), TypeError(f"Row value should be Real, now it has "
                                           f"{type(instance.value)} type!")

        elif column_type == 2:
            assert len(value) == 1, TypeError(f"Row value type should be Charset, now it has "
                                              f"{type(instance.value)} type!")

        elif column_type == 3:
            assert str(value), TypeError(f"Row value type should be String, now it has "
                                         f"{type(instance.value)} type!")

        elif column_type == 4:
            open_tag = value.count("<")
            close_tag = value.count(">")
            assert str(value), TypeError(f"Row value should be Charset, now it has "
                                         f"{type(instance.value)} type!")
            assert open_tag == close_tag, ValueError("Count of open and close tags should be equal!")
            assert (open_tag != 0 and close_tag != 0), ValueError("HTML file should contain at least 1 tag")

        elif column_type == 5:
            assert list(value) and str(list(value)[0]) and str(list(value)[1]), TypeError(f"Row value should be "
                                                                                          f"String Invl, now it has {type(instance.value)} type with ({type(instance.value[0])} and {type(instance.value[1])}) elements!")
            assert list(value)[0] < list(value)[1], ValueError("First value should be less than second")
