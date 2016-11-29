import datetime
from django.shortcuts import redirect, render, get_list_or_404, render_to_response
from ecommerce.models import *

# Create your views here.

def index(request):
    """
    商品一覧画面(/ec/list/)が呼び出された際に呼び出されるビューです。
    商品情報を返します。
    """

    products = get_list_or_404(Product)

    #   セッションにカートの情報を格納するListを定義します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()

    response = render(request, 'product_list.html', {'products': products})

    return response

def cart_add(request, product_id):
    """
    カートに任意の商品を追加する場合に呼び出されるビューです。
    カート(セッション)に任意の商品の商品IDを追加します。
    """

    #   カート(セッション)に商品を追加します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']

    item = [item for item in cart if item['product_id'] == str(product_id)]
    if item:
        item[0]['quantity'] = str(int(item[0]['quantity']) + int(request.POST['quantity'])) 
    else:
        cart.append({
            'product_id': product_id,
            'quantity': request.POST['quantity']
        })

    request.session['cart'] = cart

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    return response

def cart_delete(request, product_id):
    """
    カートに入っている任意の商品を削除する場合に呼び出されるビューです。
    カート(セッション)から任意の商品の商品IDを削除します。
    """

    #   カート(セッション)から指定された商品を削除します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']
    #   同じ商品が複数listに入っていた場合に、指定されてIDのオブジェクトをすべて削除する
    cart = [item for item in cart if not item['product_id'] == str(product_id)]

    request.session['cart'] = cart

    products = get_list_or_404(Product)

    response = redirect('/ec/cart_list/', {'products': products})

    return response


def cart_reset(request):
    """
    カートを空にするがクリックされた場合に実行されるビューです。
    カートの中身(セッション)を空にします。
    """

    #   カート(セッション)からすべての商品を削除します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    del request.session['cart']

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    return response

def cart_list(request):
    """
    カートの中身を表示するページが表示される場合に実行されるビューです。
    カートに入っている商品情報を返します。
    """

    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']

    #   カートに入っている商品の情報を取得します
    products = Product.objects.filter(id__in=[item['product_id'] for item in cart])

    details = []
    total = 0

    for product in products:
        quantity =  [item['quantity'] for item in cart if item['product_id'] == str(product.id)][0]
        subtotal = int(product.price) * int(quantity)
        total += subtotal

        details.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart_list.html', {'details': details, 'total': total})

def order(request):
    """
    注文画面が表示される場合に実行されるビューです。
    カートに入っている商品情報と決済方法と注文画面を返します。
    """

    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']

    #   カートに入っている商品の情報を取得します
    products = Product.objects.filter(id__in=[item['product_id'] for item in cart])

    #   決済方法を取得します。
    payments = get_list_or_404(Payment)

    details = []
    total = 0

    for product in products:
        quantity = [item['quantity'] for item in cart if item['product_id'] == str(product.id)][0]
        subtotal = int(product.price) * int(quantity)
        total += subtotal

        details.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'order.html', {'details': details, 'payments': payments, 'total': total})

def order_execute(request):
    """
    注文画面からPOSTされた際に実行されるビューです。
    お客様情報を保存し注文された商品情報を保存します。
    """

    err_msg = ''

    if not request.POST['first_name']:
        err_msg = 'お名前(名)'
    elif not request.POST['last_name']:
        err_msg = 'お名前(姓)'
    elif not request.POST['postal_code']:
        err_msg = '郵便番号'
    elif not request.POST['prefecture']:
        err_msg = '都道府県'
    elif not request.POST['city']:
        err_msg = '市区町村'
    elif not request.POST['street1']:
        err_msg = '番地'
    elif not request.POST['street2']:
        err_msg = '建物名'
    elif not request.POST['tel']:
        err_msg = '電話番号'
    elif not request.POST['email']:
        err_msg = 'メールアドレス'
    else:
        err_msg = ''

    if err_msg:
        #   カート(セッション)内にある商品IDを取得します。
        if not request.session.has_key('cart'):
            request.session['cart'] = list()
        cart = request.session['cart']

        #   カートに入っている商品の情報を取得します
        products = Product.objects.filter(id__in=[item['product_id'] for item in cart])

        #   決済方法を取得します。
        payments = get_list_or_404(Payment)

        err_msg = err_msg + 'が入力されていません'

        return render(request, 'order.html', {'products': products, 'payments': payments, 'message':err_msg})



    #   送信されたお客様情報を保存します。
    customer = Customer(first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        postal_code=request.POST['postal_code'],
                        prefecture=request.POST['prefecture'],
                        city=request.POST['city'],
                        street1=request.POST['street1'],
                        street2 =request.POST['street2'],
                        tel=request.POST['tel'],
                        email=request.POST['email'])
    customer.save()

    #   Paymentオブジェクトを取得します。
    payment = Payment.objects.get(id=int(request.POST['payment']))

    #   注文情報を保存します。
    order = Order(customer=customer, payment=payment)
    order.save()

    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']

    #   カートに入っている商品の情報を取得します
    products = Product.objects.filter(id__in=[item['product_id'] for item in cart])

    for product in products:
        order_product = Order_Product(order=order, product=product, count=1, price=product.price)
        order_product.save()

    #   注文完了画面にリダイレクトします。
    return redirect('/ec/order_complete/')

def order_complete(request):
    """
    注文完了時に実行されるビューです。
    注文完了画面を返します。
    """

    response = render_to_response('order_complete.html')

    #   カートの中身を削除します
    if request.session.has_key('cart'):
        del request.session['cart']
    return response
