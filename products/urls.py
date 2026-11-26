# Do Django, traga a ferramenta "path", que liga um endereço (URL) a uma view
from django.urls import path

# Do app products (o "." = "esta pasta"), traga o arquivo views.py
from . import views

# Lista de endereços deste app
urlpatterns = [
    # '' = endereço vazio, ou seja, a "raiz" do app.
    # Como no projeto vamos ligar este app em 'products/',
    # este '' vira o endereço: /products/
    # views.all_products = a função que responde quando alguém visita
    # name='products' = apelido da URL, usado no HTML com {% url 'products' %}
    path('', views.all_products, name='products'),
]