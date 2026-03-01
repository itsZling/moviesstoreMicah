from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.db.models import Sum

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.user.username

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    amountPurchased = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        curr = self.order.user
        totalQ = Item.objects.filter(order__user=curr).aggregate(total=Sum('quantity'))
        total = totalQ['total'] or 0
        Item.objects.filter(order__user=curr).update(amountPurchased=total)
