from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views.generic import ListView

from itertools import chain


from .models import Category, Product, News, CustomUser, NewsCategory
from .forms import ContactForm, LoginForm, UserCreateForm, AccountForm, CommentForm

'''
共通処理
'''

def get_all_category():
    categories = Category.objects.all()
    return categories

  
def cart_list(request):
    cart = request.session.get('cart')
    amount = request.session.get('amount')
    if cart:
        products = []
        for product_id in cart:
            try:
                product = Product.objects.get(id=product_id)
                products.append(product)
            except Product.DoesNotExist:
                pass
    else:
        products = []
    
    total_price = 0
    for product in products:
        total_price += product.price
        
    return products, amount, total_price


def paginating(request, products):
    paginator = Paginator(products, 12)
    
    page = request.GET.get('page', 1)
    products = paginator.page(page)
    
    return products
    


'''
view関数
'''

# main pages

def index(request):
    title = '傾奇者による傾奇者のための着物'
    news = News.objects.filter(is_public=True).order_by('-published_at')
    
    context = {'title': title, 'news': news}
    
    return render(request, 'ec/index.html', context)


def info_index(request):
    title = 'NEWS'
    infos = News.objects.order_by('-published_at')
    news_categories = NewsCategory.objects.all()
    
    context = {'infos': infos, 'title': title, 'news_categories': news_categories}
    
    return render(request, 'ec/info_index.html', context)

    
def info_detail(request, info_id):
    info = get_object_or_404(News, id=info_id)
    infos = News.objects.filter(is_public=True).order_by('-published_at')
    info_category = info.category.all()
    news_categories = NewsCategory.objects.all()
    if request.user.username:
        initial = {'author': request.user.username}
    else:
        initial = {'author': 'None'}
    if request.method == 'POST':
        form = CommentForm(request.POST, initial=initial)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = info
            comment.save()
            return redirect('info_detail', info_id=info.id) 
    else:
        
        form = CommentForm(request.POST or None, initial=initial)
    title = info.title
    
    context = {'title': title,
               'info': info,
               'infos': infos,
               'news_categories': news_categories,
               'form': form}
    
    return render(request, 'ec/info_detail.html', context)



def info_category(request, category_id):
    category = NewsCategory.objects.get(id=category_id)
    news_categories = NewsCategory.objects.all()
    category_infos = News.objects.filter(category__id=category_id).order_by('-published_at')
    infos = News.objects.order_by('-published_at')
    title = category.name
    
    context = {'category_infos': category_infos,
               'infos': infos,
               'title': title,
               'news_categories': news_categories}
    
    return render(request, 'ec/info_category.html', context)
    

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            contact.save()
            message = 'お問い合わせありがとうございます。'
            return redirect('contact')
    else:
        form = ContactForm()
    title = 'CONTACT'
    
    context = {'title': title, 'form': form}
    
    return render(request, 'ec/contact.html', context)
 
    
def about(request):
    title = 'ABOUT'
    return render(request, 'ec/about.html', {'title': title})    


def account(request):
    title = 'ACCOUNT'
    return render(request, 'ec/account.html', {'title': title})


class Create_account(CreateView):
    def post(self, request, *arg, **kwargs):
        signup_form = UserCreateForm(data=request.POST)
        login_form = LoginForm()
        title = 'SIGN UP'
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('username')
            password = signup_form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('account')
            
        return render(request, 'registration/login.html', {'signup_form': signup_form, 'login_form': login_form, 'title': title})

    def get(self, request, *arg, **kwargs):
        title = 'SIGN UP'
        signup_form = UserCreateForm()
        login_form = LoginForm()
        
        return render(request, 'registration/login.html', {'signup_form': signup_form, 'login_form': login_form, 'title': title})

create_account = Create_account.as_view()


class Account_login(View):
    def post(self, request, *arg, **kwargs):
        login_form = LoginForm(data=request.POST)
        signup_form = UserCreateForm()
        title = 'LOGIN'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            user = CustomUser.objects.get(username=username)
            login(request, user)
            return redirect('account')
        return render(request, 'registration/login.html', {'login_form': login_form, 'signup_form': signup_form, 'title': title})
        
    def get(self, request, *arg, **kwargs):
        title = 'LOGIN'
        login_form = LoginForm()
        signup_form = UserCreateForm()
        return render(request, 'registration/login.html', {'login_form': login_form, 'signup_form': signup_form, 'title': title})
        
account_login = Account_login.as_view()


def account_delete(request):
    pass


def account_info(request):
    title = 'ACCOUNT INFO'
    context = {'title': title}
    return render(request, 'ec/account_info.html', context)


def account_edit(request):
    title = 'EDIT ACCOUNT'
    user = get_object_or_404(CustomUser, id=request.user.id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('account_info')
    else:
        form = AccountForm({'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name
        })
    
    context = {'title': title, 'form': form}
    
    return render(request, 'ec/account_edit.html', context)


# shop pages

def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    cart_products, amount, total_price = cart_list(request)
    title = product.name
    
    
    context = {'product': product,
               'categories': categories,
               'title': title,
               'cart_products': cart_products,
               'amount': amount,
               'total_price': total_price,}
    
    return render(request, 'ec/product_detail.html', context)
    
    
def category(request, category_id):
    category = Category.objects.get(id=category_id)
    categories = get_all_category()
    products = Product.objects.filter(category__id=category_id).order_by('-created_at')
    products = paginating(request, products)
    cart_products, amount, total_price = cart_list(request)
    title = category.name
    
    context = {'products': products,
               'title': title,
               'categories': categories,
               'cart_products': cart_products,
               'amount': amount,
               'total_price': total_price}
    
    return render(request, 'ec/category.html', context)
    

class List(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = ProductFilter(self.request.GET, queryset=Product.order_by('-created_at').filter(
            Q(name__icontains=q_word) | Q(brand__icontains=q_word) | Q(description__icontains=q_word)))
        context["orderby"] = ProductFilter(self.request.GET, queryset=Product.objects.all().order_by('release_date'))
        return context
        
    
def shop(request):
    title = 'ONLINE SHOP'
    cart_products, amount, total_price = cart_list(request)
    categories = get_all_category()
    params = request.GET.copy()
    search_word = None
    
    if 'search' in params:
        search_word = request.GET.get('search')
        products = Product.objects.order_by('-created_at').filter(
            Q(name__icontains=search_word) | Q(brand__icontains=search_word) | Q(description__icontains=search_word))
    else:
        products = Product.objects.order_by('-created_at')
        
    if 'orderby' in params:
        order = request.GET.get('orderby')
        if order == 'newest':
            products = Product.objects.order_by('-created_at')
        if order == 'price-asc':
            products_1 = Product.objects.filter(quantity__gt=0).order_by('price')
            products_2 = Product.objects.filter(quantity=0).order_by('price')
            products = list(chain(products_1, products_2))
        if order == 'price-des':
            products_1 = Product.objects.filter(quantity__gt=0).order_by('-price')
            products_2 = Product.objects.filter(quantity=0).order_by('-price')
            products = list(chain(products_1, products_2))
        
    
    if 'page' in params:
        page = params['page']
        del params['page']
    else:
        page = 1
    search_params = params.urlencode()
    
    paginator = Paginator(products, 12)
    products = paginator.page(page)
    
    
    
    context = {'products': products,
               'categories': categories, 
               'title': title,
               'cart_products': cart_products,
               'amount': amount,
               'total_price': total_price,
               'search_params': search_params,
               'search_word': search_word,
    }
    
    return render(request, 'ec/shop.html', context)

               
@require_POST
def favorite_product(request, product_id):
    parameter = request.get_full_path()
    product = get_object_or_404(Product, id=product_id)
    request.user.favorite_products.add(product)
    return redirect(request.META['HTTP_REFERER'])
    
@require_POST 
def unfavorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    request.user.favorite_products.remove(product)
    return redirect(request.META['HTTP_REFERER'])
    

def fav_products(request, user_id):
    fav_user = CustomUser.objects.get(id=user_id)
    products = fav_user.favorite_products.all()
    title = 'FAVORITES'
    return render(request, 'ec/favorites.html', {'title': title, 'products': products})
    

def cart_add2(request, product_id):
    cart = request.session.get('cart', [])
    
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect(request.META['HTTP_REFERER'])
    
    
    
def cart_add(request, product_id):
    cart = request.session.get('cart', [])
    amount = request.session.get('amount', [])
    
    if product_id not in cart:
        cart.append(product_id)
        amount.append(1)
    else:
        index = cart.index(product_id)
        amount[index] += 1
        
    request.session['cart'] = cart
    request.session['amount'] = amount
    
    return redirect(request.META['HTTP_REFERER'])
    

def cart(request):
    title = 'CART'
    cart_products, amount, total_price = cart_list(request)
    context = {
        'title': title,
        'cart_products': cart_products,
        'amount': amount,
        'total_price': total_price,
    }
    
    return render(request, 'ec/cart.html', context)