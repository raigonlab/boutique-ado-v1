# Do Django, traga as ferramentas:
# render = junta o HTML com os dados e monta a página final
# redirect = manda o visitante para outro endereço
# reverse = transforma o apelido de uma URL ('products') no endereço real ('/products/')
# get_object_or_404 = busca UM item no banco; se não existir, mostra erro 404
from django.shortcuts import render, redirect, reverse, get_object_or_404

# messages = mostra avisos para o usuário (ex: "você não digitou nada!")
from django.contrib import messages

# Q = permite montar buscas com "OU" (procure no nome OU na descrição)
from django.db.models import Q

# Do arquivo models desta mesma pasta, traga o modelo Product
from .models import Product

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Comece com TODOS os produtos
    products = Product.objects.all()

    # Caixa do termo buscado. Começa vazia (None = "nada")
    query = None

    # request.GET = o que veio no endereço depois do "?"
    # Ex: /products/?q=jeans  ->  request.GET = {'q': 'jeans'}
    if request.GET:
        # Se veio o campo 'q' (é o name="q" do input da barra de busca)...
        if 'q' in request.GET:
            # ...guarde o texto digitado na caixa query
            query = request.GET['q']

            # Se o texto está vazio (clicou em buscar sem digitar)...
            if not query:
                # ...mostre um aviso de erro...
                messages.error(request, "You didn't enter any search criteria!")
                # ...e volte para a página de todos os produtos
                return redirect(reverse('products'))

            # Monte a busca: nome CONTÉM o texto  OU (|)  descrição CONTÉM o texto
            # icontains = "contém", sem ligar para maiúscula/minúscula
            queries = Q(name__icontains=query) | Q(description__icontains=query)

            # Filtre os produtos: fique só com os que combinam com a busca
            products = products.filter(queries)

    # Mochila: os produtos (todos ou filtrados) + o termo buscado
    context = {
        'products': products,
        'search_term': query,
    }

    # Responda com a página products.html preenchida com a mochila
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