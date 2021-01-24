from .cart import Cart

def cart_total_quantity(request):
#if request.user.is_authenticated:
	cart = Cart(request)  # posso toglierlo o metterlo e non cambia niente
	total_quantity = 0
	for key, value in request.session['cart'].items():
		total_quantity += value['quantity']
	if total_quantity > 0:
		return {'cart_total_quantity': total_quantity}
	else:
		return {'cart_total_quantity': ''}


def cart_total_amount(request):
#if request.user.is_authenticated:
	cart = Cart(request) # posso toglierlo o metterlo e non cambia niente
	total_bill = 0.0
	for key,value in request.session['cart'].items():
		total_bill = total_bill + (float(value['price']) * value['quantity'])
	if total_bill > 0:
		return {'cart_total_amount': total_bill}
	else:
		return {'cart_total_amount': ''}
#else:
#	return {'cart_total_amount': ''}
