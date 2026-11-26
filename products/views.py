# Do Django, traga a ferramenta "render": ela junta o HTML com os dados
# e monta a página final
from django.shortcuts import render

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
