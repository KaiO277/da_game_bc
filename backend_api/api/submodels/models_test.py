from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        if self.name:
            return self.name 
        return str(self.id) + "_" + "Product"