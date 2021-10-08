# from django.db import models
# from django.utils import timezone
#
#
# class Order(models.Model):
#     user_first_name = models.CharField(max_length=100)
#     user_last_name = models.CharField(max_length=100)
#     user_email = models.EmailField()
#     user_message = models.TextField(max_length=1000)
#     order_date = models.DateTimeField(default=timezone.now)
#     order_created = models.DateTimeField(auto_now_add=True)
#     order_updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ('-created',)
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     def __str__(self):
#         return 'Order {}'.format(self.id)
#
#     def get_total_cost(self):
#         return sum(item.get_cost() for item in self.items.all())
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items')
#     product = models.ForeignKey(Product, related_name='order_items')
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return '{}'.format(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity
