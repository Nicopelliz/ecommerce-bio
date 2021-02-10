
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Product, OrderItem, Order, ShippingAddress, Payment
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CheckoutForm
import stripe, random, string

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductList(ListView):
    model = Product
    paginate_by = 4
    template_name = 'mercato.html'
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    template_name = 'dettaglio_prodotto.html'
    context_object_name = 'product'


@login_required(login_url="/login")
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def elimina_dal_carrello(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def diminuisci_quantita(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(product__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class Carrello(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart/cart_detail.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'cart/empty_cart.html')


class Checkout(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'object': order,
                'DISPLAY_COUPON_FORM': True
            }

            return render(self.request, "cart/checkout.html", context)
        except ObjectDoesNotExist:
            return render(self.request, 'cart/cart_detail.html')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(self.request.POST)
            if form.is_valid():
                indirizzo = form.cleaned_data.get('indirizzo')
                citta = form.cleaned_data.get('citta')
                provincia = form.cleaned_data.get('provincia')
                codice_postale = form.cleaned_data.get('codice_postale')
                # usa_come_indirizzo_di_spedizione = form.cleaned_data.GET('usa_come_indirizzo_di_spedizione')
                # salva = form.cleaned_data.GET('salva')
                opzioni_di_pagamento = form.cleaned_data.get(
                    'opzioni_di_pagamento')
                billing_address = ShippingAddress(
                    user=self.request.user,
                    indirizzo=indirizzo,
                    citta=citta,
                    provincia=provincia,
                    codice_postale=codice_postale,
                    opzioni_di_pagamento=opzioni_di_pagamento
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                print(form.cleaned_data)
                return redirect("payment", opzioni_di_pagamento)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("home")

def create_idempotency_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))


class PaymentView(View):

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            payment = ShippingAddress.objects.get(user=self.request.user)
            context = {
                'payment': payment,
                'object': order,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, 'cart/payment.html', context)
        except ObjectDoesNotExist:
            return render(self.request, 'cart/cart_detail.html')

    def post(self, *args, **kwargs):
        
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price()*100)  # perchè è in cents

        idempotency_key = create_idempotency_key()

        try:
        # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
                amount=amount,
                currency="eur",
                source=token,
                idempotency_key=idempotency_key
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount/100
            payment.save()
        
            order.ordered = True
            order.payment = payment
            order.save() 

            messages.success(self.request, 'Ordine eseguito con successo!')    

            return redirect('home')

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return HttpResponseRedirect(self.request.path_info)

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, 'Rate limit Error')
            return HttpResponseRedirect(self.request.path_info)
            
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, 'FuCk you Invalid Request Error')
            return HttpResponseRedirect(self.request.path_info)
            
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, 'Authentication Error')
            return HttpResponseRedirect(self.request.path_info)
         
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, ' API Connection Error')
            return HttpResponseRedirect(self.request.path_info)
            
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, 'Stripe Error')
            return HttpResponseRedirect(self.request.path_info)
            
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            # yourself an email
            messages.error(self.request, 'Stripe Error')
            return HttpResponseRedirect(self.request.path_info)

def success_page(request):
    return render(request, 'cart/success.html')

        

