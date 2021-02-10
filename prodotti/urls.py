from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (ProductList,
                    ProductDetail,
                    add_to_cart,
                    elimina_dal_carrello,
                    diminuisci_quantita,
                    Carrello,
                    Checkout,
                    PaymentView,
                    success_page
)


urlpatterns = [

    path('mercato/', ProductList.as_view(), name='mercato'),
    path('mercato/<slug:slug>/', ProductDetail.as_view(), name='dettaglio-prodotto'),
    path('aggiungi-al-carrello/<slug:slug>/', add_to_cart, name='aggiungi-al-carrello'),
    path('rimuovi-dal-carrello/<slug:slug>/', elimina_dal_carrello, name='elimina-dal-carrello'),
    path('diminuisci-quantita/<slug:slug>/', diminuisci_quantita, name='diminuisci-quantita'),
    path('carrello/', login_required(Carrello.as_view()), name='carrello'),
    path('checkout/', login_required(Checkout.as_view()), name='checkout'),
    path('pagamento/<opzioni_di_pagamento>', PaymentView.as_view(), name='payment'),
    path('success/pagamento', success_page, name='success'),

]