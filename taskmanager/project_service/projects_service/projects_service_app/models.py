from django.db import models


class Project(models.Model):
    class Status(models.IntegerChoices):
        ISSUED = 0, 'Создан'
        DELIVERED = 1, 'Выполнен'

    owner_email = models.EmailField(max_length=255, default=None)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices))
                                       , default=Status.ISSUED)
    tasks = models.JSONField(default=list)

    def __str__(self):
        return f'project-{self.pk}({self.time_create.strftime("%d-%m-%Y %H:%M")})'
