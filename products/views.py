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

# (NOVO) Lower = transforma texto em minúsculas, dentro do banco.
# Usado para ordenar por nome sem que "Zebra" venha antes de "abacaxi"
from django.db.models.functions import Lower

# Do arquivo models desta mesma pasta, traga os modelos Product e Category
from .models import Product, Category

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Comece com TODOS os produtos
    products = Product.objects.all()

    # Caixas que começam vazias (None = "nada"):
    query = None        # termo buscado
    categories = None   # categorias escolhidas
    sort = None         # (NOVO) por qual campo ordenar (price, rating, name...)
    direction = None    # (NOVO) direção: 'asc' (crescente) ou 'desc' (decrescente)

    # request.GET = o que veio no endereço depois do "?"
    # Ex: /products/?sort=price&direction=asc
    #     -> request.GET = {'sort': 'price', 'direction': 'asc'}
    if request.GET:

        # (NOVO) Se veio o campo 'sort' no endereço...
        if 'sort' in request.GET:
            # ...guarde o campo escolhido (ex: 'price')
            sortkey = request.GET['sort']
            # Guarde uma cópia original em "sort" (usada no fim, em current_sorting)
            sort = sortkey

            # Se for ordenar por NOME...
            if sortkey == 'name':
                # ...ordene por uma versão em minúsculas do nome
                sortkey = 'lower_name'
                # annotate = cria um "campo temporário" lower_name em cada produto
                products = products.annotate(lower_name=Lower('name'))

            # Se veio também a direção...
            if 'direction' in request.GET:
                direction = request.GET['direction']
                # Se for 'desc', coloque um "-" na frente: no Django, "-price"
                # significa "do maior para o menor"
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            # Ordene os produtos pelo campo escolhido
            products = products.order_by(sortkey)

        # Se veio o campo 'category' no endereço...
        if 'category' in request.GET:
            # ...pegue o texto e corte nas vírgulas, virando uma lista
            # Ex: 'jeans,shirts'  ->  ['jeans', 'shirts']
            categories = request.GET['category'].split(',')

            # Fique só com produtos cuja categoria tem o nome DENTRO (__in) da lista
            # category__name = "vá até a categoria do produto e olhe o campo name"
            products = products.filter(category__name__in=categories)

            # Troque a lista de textos pelos objetos Category de verdade,
            # para podermos usar no HTML depois (ex: o friendly_name)
            categories = Category.objects.filter(name__in=categories)

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

    # (NOVO) Junte campo + direção num texto só. Ex: 'price_asc'
    # Se não escolheu nada, fica 'None_None'
    current_sorting = f'{sort}_{direction}'

    # Mochila: produtos + termo buscado + categorias + (NOVO) ordenação atual
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
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