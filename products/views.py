# Do Django, traga duas ferramentas:
# render = junta o HTML com os dados e monta a página final
# get_object_or_404 = busca UM item no banco; se não existir, mostra erro 404
from django.shortcuts import render, get_object_or_404

# Do arquivo models desta mesma pasta (o "." = "aqui"), traga o modelo
# Product (a tabela de produtos do banco)
from .models import Product

# Create your views here.


# Crie uma função chamada all_products. Ela recebe o "request",
# que é o visitante dizendo: "quero ver essa página"
def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Vá no banco, pegue TODOS os produtos e guarde na caixa "products"
    products = Product.objects.all()

    # Monte a "mochila" (context): a etiqueta 'products' leva a caixa
    # de produtos. No HTML usamos essa etiqueta:
    # {% for product in products %}
    context = {
        'products': products,
    }

    # Responda ao visitante com a página products.html,
    # preenchida com o que está na mochila
    return render(request, 'products/products.html', context)


# Crie a função product_detail. Além do "request", ela recebe o
# "product_id", que é o número do produto que vem no endereço (ex: /products/5)
def product_detail(request, product_id):
    """ A view to show individual product details """

    # Busque no banco o produto cujo id (pk = primary key) é igual a product_id.
    # Se não achar, mostre o erro 404 em vez de quebrar o site
    product = get_object_or_404(Product, pk=product_id)

    # Mochila com UM produto só (etiqueta no singular: 'product')
    context = {
        'product': product,
    }

    # Responda com a página product_detail.html preenchida com a mochila
    return render(request, 'products/product_detail.html', context)