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


from .models import Category, Product, Info, CustomUser, InfoCategory
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
    
    if not amount:
        amount = []
    
    total_price = 0
    
    for product, num in zip(products, amount):
        total_price += product.price * num
       
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
    news = Info.objects.filter(is_public=True).order_by('-published_at')
    
    context = {
        'title': title,
        'news': news
        
    }
    
    return render(request, 'ec/index.html', context)


def info_index(request):
    title = 'NEWS'
    infos = Info.objects.filter(is_public=True).order_by('-published_at')
    recents = Info.objects.filter(is_public=True).order_by('-published_at')[:5]
    news_categories = InfoCategory.objects.all()
    
    context = {
        'infos': infos,
        'title': title,
        'recents': recents,
        'news_categories': news_categories
        
    }
    
    return render(request, 'ec/info_index.html', context)

    
def info_detail(request, info_id):
    info = get_object_or_404(Info, id=info_id)
    recents = Info.objects.filter(is_public=True).order_by('-published_at')[:5]
    info_category = info.category.all()
    news_categories = InfoCategory.objects.all()
    
    comments = info.comments.filter(approve=True).order_by('-created_at')
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
    
    context = {
        'title': title,
        'info': info,
        'recents': recents,
        'news_categories': news_categories,
        'form': form,
        'comments': comments
        
    }
    
    return render(request, 'ec/info_detail.html', context)



def info_category(request, category_id):
    category = InfoCategory.objects.get(id=category_id)
    news_categories = InfoCategory.objects.all()
    category_infos = Info.objects.filter(category__id=category_id).order_by('-published_at')
    recents = Info.objects.filter(is_public=True).order_by('-published_at')
    title = category.name
    
    context = {
        'category_infos': category_infos,
        'title': title,
        'recents': recents,
        'news_categories': news_categories
        
    }
    
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
    
    context = {
        'title': title,
        'form': form
        
    }
    
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
            
        context = {
            'signup_form': signup_form,
            'login_form': login_form,
            'title': title
            
        }
        
        return render(request, 'registration/login.html', context)

    def get(self, request, *arg, **kwargs):
        title = 'SIGN UP'
        signup_form = UserCreateForm()
        login_form = LoginForm()
        
        context = {
            'signup_form': signup_form,
            'login_form': login_form,
            'title': title
            
        }
        
        return render(request, 'registration/login.html', context)

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
            
        context = {
            'login_form': login_form,
            'signup_form': signup_form,
            'title': title
            
        }
        
        return render(request, 'registration/login.html', context)
        
    def get(self, request, *arg, **kwargs):
        title = 'LOGIN'
        login_form = LoginForm()
        signup_form = UserCreateForm()
        
        context = {
            'login_form': login_form,
            'signup_form': signup_form,
            'title': title
            
        }
        
        return render(request, 'registration/login.html', context)
        
account_login = Account_login.as_view()


def account_delete(request):
    pass


def account_info(request):
    title = 'ACCOUNT INFO'
    return render(request, 'ec/account_info.html', {'title': title})


def account_edit(request):
    title = 'EDIT ACCOUNT'
    user = get_object_or_404(CustomUser, id=request.user.id)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('account_info')
    else:
        form = AccountForm({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        })
    
    context = {
        'title': title,
        'form': form
        
    }
    
    return render(request, 'ec/account_edit.html', context)


# shop pages

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
    
    context = {
        'products': products,
        'categories': categories, 
        'title': title,
        'cart_products': cart_products,
        'amount': amount,
        'total_price': total_price,
        'search_params': search_params,
        'search_word': search_word,
    }
    
    return render(request, 'ec/shop.html', context)


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    cart_products, amount, total_price = cart_list(request)
    title = product.name
    
    context = {
        'product': product,
        'categories': categories,
        'title': title,
        'cart_products': cart_products,
        'amount': amount,
        'total_price': total_price,
        
    }
    
    if request.method == 'POST':
        #if 'update' in request.POST:
        cart = request.session.get('cart')
        amount = request.session.get('amount')
        if cart:
        #    filtered_cart = []
         #   filtered_amount = []
            for p_id, num in zip(cart, amount):
                if p_id == request.POST['product-id']:
                    index = cart.index(p_id)
                    amount[index] = request.POST['number']
            request.session['cart'] = cart
            request.session['amount'] = amount
        return redirect(request.META['HTTP_REFERER'])       
    
    return render(request, 'ec/product_detail.html', context)
    
    
def category(request, category_id):
    category = Category.objects.get(id=category_id)
    categories = get_all_category()
    products = Product.objects.filter(category__id=category_id).order_by('-created_at')
    params = request.GET.copy()
    
    if 'orderby' in params:
        order = request.GET.get('orderby')
        if order == 'newest':
            pass
        if order == 'price-asc':
            products_1 = Product.objects.filter(category__id=category_id, quantity__gt=0).order_by('price')
            products_2 = Product.objects.filter(category__id=category_id, quantity=0).order_by('price')
            products = list(chain(products_1, products_2))
        if order == 'price-des':
            products_1 = Product.objects.filter(category__id=category_id, quantity__gt=0).order_by('-price')
            products_2 = Product.objects.filter(category__id=category_id, quantity=0).order_by('-price')
            products = list(chain(products_1, products_2))
    
    products = paginating(request, products)       
    cart_products, amount, total_price = cart_list(request)
    title = category.name
    
    context = {
        'products': products,
        'title': title,
        'categories': categories,
        'cart_products': cart_products,
        'amount': amount,
        'total_price': total_price,
        
    }
    
    return render(request, 'ec/category.html', context)
    
    
# favorites  

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
    
def faved_products(request):
    user_id = request.user.id
    faved_user = CustomUser.objects.get(id=user_id)
    products = faved_user.favorite_products.all()
    title = 'FAVORITES'
    return render(request, 'ec/favorites.html', {'title': title, 'products': products})
    

# cart

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
 

@require_POST
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
    
    
@require_POST
def cart_update(request, product_id, number):
    cart = request.session.get('cart')
    amount = request.session.get('amount')
    if cart:
        for p_id, num in zip(cart, amount):
            if p_id == product_id:
                index = cart.index(p_id)
                amount[index] = number
        request.session['cart'] = cart
        request.session['amount'] = amount
    return redirect(request.META['HTTP_REFERER'])

    
@require_POST
def cart_delete(request, product_id):
    cart = request.session.get('cart')
    amount = request.session.get('amount')
    if cart:
        filtered_cart = []
        filtered_amount = []
        for p_id, num in zip(cart, amount):
            if p_id != product_id:
                filtered_cart.append(p_id)
                filtered_amount.append(num)
        request.session['cart'] = filtered_cart
        request.session['amount'] = filtered_amount
    return redirect(request.META['HTTP_REFERER'])
