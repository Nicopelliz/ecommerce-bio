
from django import template
from prodotti.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            quantity = qs[0].get_total_quantity()
            if quantity != 0:
                return quantity
