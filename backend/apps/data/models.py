from django.db import models


class ExampleDataDaily(models.Model):
    date = models.DateField()
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    nir = models.IntegerField()
    related_id = models.IntegerField()

    def __str__(self):
        return f"{self.id=} {self.related_id=} {self.date=} {self.red=} {self.green=} {self.blue=} {self.nir=}"

    class Meta:
        verbose_name = "Example Data Daily"
        verbose_name_plural = "Example Data Daily"
        ordering = [
            "related_id",
            "date",
        ]
