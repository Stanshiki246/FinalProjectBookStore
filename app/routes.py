from flask import render_template,flash,redirect,url_for,request,session,jsonify
from app import app,db
from app.forms import *
from flask_login import current_user,login_user,logout_user,login_required
from app.models.Users import Users
from app.models.Products import Customers,Products
from app.models.Carts import Cart_customers,Cart_products
from app.models.Transactions import Trans_products,Trans_users,Transactions,PaymentProof,Orders
from app.models.Libraries import Library_customers,Library_products,Comics
from werkzeug.urls import url_parse
from datetime import datetime,time,date,timedelta


@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    form=SearchTitle()
    if form.validate_on_submit():
        return redirect(url_for('search_product',name=form.title.data.replace(' ','+')))
    return render_template('index.html', title='Home',users=Users.query.all(),products=Products.query.all(),form=form,
                           customer=Customers.query.filter_by(user_id=current_user.id).first())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data,first_name=form.first_name.data,
                     last_name=form.last_name.data,phone_number=form.phone_num.data,usertype='Customer'
                     )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        customer=Customers(user_id=user.id)
        db.session.add(customer)
        db.session.commit()
        trans_customer=Trans_users(username=user.username,first_name=user.first_name,
                                           last_name=user.last_name,email=user.email,
                                           phone_number=user.phone_number,user_id=user.id)
        db.session.add(trans_customer)
        db.session.commit()
        cart_customer=Cart_customers(user_id=user.id)
        db.session.add(cart_customer)
        db.session.commit()
        library_customer=Library_customers(user_id=user.id)
        db.session.add(library_customer)
        db.session.commit()
        flash('You have been registered in this webpage')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form,usertype='Customer')

@app.route('/delete/<int:id>')
def delete(id):
    user=Users.query.filter_by(id=id).first()
    if user is not None:
        if user.usertype == 'Customer':
            customer=Customers.query.filter_by(user_id=id).first()
            if customer is not None:
                db.session.delete(customer)
                db.session.commit()
            cart_customer=Cart_customers.query.filter_by(user_id=id).first()
            if cart_customer is not None:
                db.session.delete(cart_customer)
                db.session.commit()
            trans_customer=Trans_users.query.filter_by(user_id=id).first()
            if trans_customer is not None:
                db.session.delete(trans_customer)
                db.session.commit()
            library_customer=Library_customers.query.filter_by(user_id=id).first()
            if library_customer is not None:
                db.session.delete(library_customer)
                db.session.commit()
        db.session.delete(user)
        db.session.commit()
        flash('Deleted Successfully!')
    else:
        flash('There is no user in the database')
    return redirect(url_for('index'))

@app.route('/add_product',methods=['GET','POST'])
def add_product():
    form=AddProduct()
    if form.validate_on_submit():
        price=0
        if form.bookTypes.data == 'Comic':
            price=15000
        elif form.bookTypes.data == 'Novel':
            price=50000
        GenreStr=""
        for i in form.genres.data:
            GenreStr += i+","
        product=Products(title=form.title.data,price=price,booktype=form.bookTypes.data,image=form.image.data,
                         genres=GenreStr,synopsis=form.synopsis.data,author=form.author.data)
        db.session.add(product)
        db.session.commit()
        cart_product=Cart_products(title=product.title,price=product.price,image=product.image,product_id=product.id)
        db.session.add(cart_product)
        db.session.commit()
        trans_product=Trans_products(title=product.title,price=product.price,image=product.image,product_id=product.id)
        db.session.add(trans_product)
        db.session.commit()
        library_product=Library_products(title=product.title,image=product.image,author=product.author,product_id=product.id,
                                         booktype=product.booktype)
        db.session.add(library_product)
        db.session.commit()
        flash('Product has been added successfully')
        return redirect(url_for('index'))
    return render_template('AddProduct.html',title="Add Product",form=form)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    product=Products.query.filter_by(id=id).first()
    if product is not None:
        cart_product=Cart_products.query.filter_by(user_id=id).first()
        if cart_product is not None:
            db.session.delete(cart_product)
            db.session.commit()
        trans_product=Trans_products.query.filter_by(user_id=id).first()
        if trans_product is not None:
            db.session.delete(trans_product)
            db.session.commit()
        library_product=Library_products.query.filter_by(user_id=id).first()
        if library_product is not None:
            db.session.delete(library_product)
            db.session.commit()
        if product.booktype == 'Comic':
            comics=Comics.query.filter_by(product_id=id).all()
            if comics is not None:
                db.session.query(Comics).filter_by(product_id=id).delete()
                db.session.commit()
        db.session.delete(product)
        db.session.commit()
        flash('Product has been deleted successfully')
    else:
        flash('Nothing is in this list')
    return redirect(url_for('index'))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form=EditUserForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(id=id).first()
        if user.check_password(form.oldpassword.data):
            user.username=form.username.data
            user.email=form.email.data
            user.phone_number=form.phone_num.data
            user.updated_at=datetime.now()
            user.set_password(form.newpassword.data)
            db.session.commit()
            if user.usertype == 'Customer':
                customer=Trans_users.query.filter_by(user_id=id).first()
                customer.username=user.username
                customer.phone_number=user.phone_number
                customer.email=user.email
                db.session.commit()
            flash('Your account has been updated')
            return redirect(url_for('index'))
        else:
            flash('Wrong password')
            return redirect(url_for('update',id=id))
    return render_template('update.html',title='Edit My Account',user=Users.query.filter_by(id=id).first(),form=form)

@app.route('/product/<int:id>')
def product(id):
    #customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    return render_template('ProductDetails.html',title='Product Details',product=Products.query.filter_by(id=id).first(),
                           comic=Comics.query.filter_by(product_id=id).first(),
                           cart_customer=Cart_customers.query.filter_by(user_id=current_user.id).first(),
                           cart_product=Cart_products.query.filter_by(product_id=id).first(),
                           library_customer=Library_customers.query.filter_by(user_id=current_user.id).first(),
                           library_product=Library_products.query.filter_by(product_id=id).first()
                           #order_product=Trans_products.query.filter_by(product_id=id).first(),
                           #orders=Orders.query.filter_by(customer=customer).all()
                           )

@app.route('/read_novel/<int:id>')
def read_novel(id):
    return render_template('NovelReader.html',title='Novel PDF Reader',product=Library_products.query.filter_by(id=id).first())

@app.route('/read_comic/<int:id>/<int:page>',methods=['GET','POST'])
def read_comic(id,page):
    product=Library_products.query.filter_by(id=id).first()
    form=PageJump()
    if form.validate_on_submit():
        return redirect(url_for('read_comic',id=id,page=form.page.data))
    return render_template('ComicReader.html',title='Comic Reader',product=product,page=page,form=form,
                           comic=Comics.query.filter_by(product_id=id,page_num=page).first(),pages=Comics.query.filter_by(product_id=id).count())

@app.route('/add_into_wishlist/<int:id>')
def add_into_wishlist(id):
    customer=Customers.query.filter_by(user_id=current_user.id).first()
    product=Products.query.filter_by(id=id).first()
    customer.add_into_wishlist(product)
    db.session.commit()
    flash('Added into Wish List Successfully')
    return redirect(url_for('index'))

@app.route('/remove_from_wishlist/<int:id>')
def remove_from_wishlist(id):
    customer=Customers.query.filter_by(user_id=current_user.id).first()
    product=Products.query.filter_by(id=id).first()
    customer.remove_from_wishlist(product)
    db.session.commit()
    flash('Removed from Wish List Successfully')
    return redirect(url_for('my_wishlist'))

@app.route('/my_wishlist')
def my_wishlist():
    return render_template('Wishlist.html',title='My Wish List',
                           user=Customers.query.filter_by(user_id=current_user.id).first())

@app.route('/search_product/<string:name>',methods=['GET','POST'])
def search_product(name):
    form=SearchTitle()
    if form.validate_on_submit():
        return redirect(url_for('search_product',name=form.title.data.replace(' ','+')))
    SearchingArr=name.split('+')
    FoundedProducts=[]
    for product in Products.query.all():
        SearchedArr=product.title.split()
        for i in SearchedArr:
            for j in SearchingArr:
                if i.lower() == j.lower():
                    if product not in FoundedProducts:
                        FoundedProducts.append(product)
    return render_template('SearchProduct.html',title='Search Results',products=FoundedProducts,form=form)

@app.route('/staff_register',methods=['GET','POST'])
def staff_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data,first_name=form.first_name.data,
                     last_name=form.last_name.data,phone_number=form.phone_num.data,usertype='Staff'
                     )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered in this webpage')
        return redirect(url_for('login'))
    return render_template('register.html', title='Staff Register', form=form,usertype='Staff')

@app.route('/admin_register',methods=['GET','POST'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data,first_name=form.first_name.data,
                     last_name=form.last_name.data,phone_number=form.phone_num.data,usertype='Admin'
                     )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been registered in this webpage')
        return redirect(url_for('login'))
    return render_template('register.html', title='Admin Register', form=form,usertype='Admin')

@app.route('/comic_page_interface/<int:id>',methods=['GET','POST'])
def comic_page_interface(id):
    form=AddComicPage()
    if form.validate_on_submit():
        product=Library_products.query.filter_by(product_id=id).first()
        FileList=[]
        counter=1
        for file in form.filename.data:
            comic=Comics(filename=file,page_num=counter,product=product)
            FileList.append(comic)
            counter += 1
        db.session.add_all(FileList)
        db.session.commit()
        FileList.clear()
        flash('Comic page has been added')
        return redirect(url_for('comic_page_interface',id=id))
    return render_template('ComicPages.html',title='Comic Page Interface',form=form,
                           comics=Comics.query.filter_by(product_id=id).all(),
                           product=Library_products.query.filter_by(product_id=id).first())

@app.route('/delete_comic_pages/<int:id>')
def delete_comic_pages(id):
    comics=Comics.query.filter_by(product_id=id).all()
    if comics is not None:
        db.session.query(Comics).filter_by(product_id=id).delete()
        db.session.commit()
        flash('All pages have been deleted')
        return redirect(url_for('comic_page_interface',id=id))

@app.route('/edit_product/<int:id>',methods=['GET','POST'])
def edit_product(id):
   form=EditProducts()
   #form.synopsis.data=Products.query.filter_by(id=id).first().synopsis
   if form.validate_on_submit():
       product=Products.query.filter_by(id=id).first()
       GenreStr=""
       for i in form.genres.data:
           GenreStr += i+","
       product.genres=GenreStr
       product.synopsis=form.synopsis.data
       product.updated_at=datetime.now()
       db.session.commit()
       flash('Product details have been edited')
       return redirect(url_for('product',id=id))
   return render_template('EditDetails.html',title='Edit Products',form=form,
                          product=Products.query.filter_by(id=id).first())

@app.route('/my_profile')
def my_profile():
    return render_template('MyAccount.html',title='My Account')

@app.route('/my_cart')
def my_cart():
    return render_template('MyCart.html',title='My Cart',user=Cart_customers.query.filter_by(user_id=current_user.id).first())

@app.route('/add_into_cart/<int:id>')
def add_into_cart(id):
    cart_customer=Cart_customers.query.filter_by(user_id=current_user.id).first()
    cart_product=Cart_products.query.filter_by(product_id=id).first()
    cart_customer.add_into_my_carts(cart_product)
    db.session.commit()
    flash('Added into Cart Successfully')
    return redirect(url_for('product',id=id))

@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    cart_customer=Cart_customers.query.filter_by(user_id=current_user.id).first()
    cart_product=Cart_products.query.filter_by(product_id=id).first()
    cart_customer.remove_from_my_carts(cart_product)
    db.session.commit()
    flash('Removed from Cart Successfully')
    return redirect(url_for('my_cart'))

@app.route('/set_all_up')
def set_all_up():
    CustomerList=[]
    customers=Customers.query.all()
    for customer in customers:
        cart_customer=Cart_customers.query.filter_by(user_id=customer.user_id).first()
        if cart_customer is None:
            new_cart_customer=Cart_customers(user_id=customer.user_id)
            CustomerList.append(new_cart_customer)
    db.session.add_all(CustomerList)
    db.session.commit()
    CustomerList.clear()
    ProductList=[]
    products=Products.query.all()
    for product in products:
        cart_product=Cart_products.query.filter_by(product_id=product.id).first()
        if cart_product is None:
            new_cart_product=Cart_products(title=product.title,price=product.price,image=product.image,product_id=product.id)
            ProductList.append(new_cart_product)
    db.session.add_all(ProductList)
    db.session.commit()
    ProductList.clear()
    customers=Users.query.filter_by(usertype='Customer').all()
    for customer in customers:
        trans_customer=Trans_users.query.filter_by(user_id=customer.id).first()
        if trans_customer is None:
            new_trans_customer=Trans_users(username=customer.username,first_name=customer.first_name,
                                           last_name=customer.last_name,email=customer.email,
                                           phone_number=customer.phone_number,user_id=customer.id)
            CustomerList.append(new_trans_customer)
    db.session.add_all(CustomerList)
    db.session.commit()
    CustomerList.clear()
    products=Products.query.all()
    for product in products:
        trans_product=Trans_products.query.filter_by(product_id=product.id).first()
        if trans_product is None:
            new_trans_product=Trans_products(title=product.title,price=product.price,image=product.image,product_id=product.id)
            ProductList.append(new_trans_product)
    db.session.add_all(ProductList)
    db.session.commit()
    ProductList.clear()
    customers=Customers.query.all()
    for customer in customers:
        library_customer=Library_customers.query.filter_by(user_id=customer.user_id).first()
        if library_customer is None:
            new_library_customer=Library_customers(user_id=customer.user_id)
            CustomerList.append(new_library_customer)
    db.session.add_all(CustomerList)
    db.session.commit()
    CustomerList.clear()
    products=Products.query.all()
    for product in products:
        library_product=Library_products.query.filter_by(product_id=product.id).first()
        if library_product is None:
            new_library_product=Library_products(title=product.title,image=product.image,author=product.author,product_id=product.id)
            ProductList.append(new_library_product)
    db.session.add_all(ProductList)
    db.session.commit()
    ProductList.clear()
    flash('All have been set up')
    return redirect(url_for('index'))

#Render My Order
@app.route('/my_order')
def my_order():
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    return render_template('MyOrders.html',title='My Orders',orders=Orders.query.filter_by(customer=customer).all())

@app.route('/check_out')
def check_out():
    cart_customer=Cart_customers.query.filter_by(user_id=current_user.id).first()
    carts=cart_customer.my_carts
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    if cart_customer.my_carts_is_empty():
        totalprice=0
        for cart in carts:
            totalprice += cart.price
        new_order=Orders(total_price=totalprice,datestamp=datetime.now(),deadline=datetime.now()+timedelta(days=1),customer=customer)
        db.session.add(new_order)
        db.session.commit()
        for cart in carts:
            product=Trans_products.query.filter_by(product_id=cart.product_id).first()
            new_order.add_into_order_itemlists(product)
            db.session.commit()
        for cart in carts:
            cart_customer.remove_from_my_carts(cart)
            db.session.commit()
        flash('Orders have been made')
        return redirect(url_for('my_order'))
    else:
        flash('No items in this cart')
        return redirect(url_for('my_cart'))
#Render Order List
@app.route('/my_order_list/<int:id>')
def my_order_list(id):
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    return render_template('OrderList.html',title='Order Item List',order=Orders.query.filter_by(id=id,customer=customer).first())

@app.route('/cancel_order/<int:id>')
def cancel_order(id):
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    order=Orders.query.filter_by(id=id,customer=customer).first()
    order.status="Cancelled"
    db.session.commit()
    return redirect(url_for('my_order'))
#Render Payment Proof Form
@app.route('/payment_proof_form/<int:id>',methods=['GET','POST'])
def payment_proof_form(id):
    form=PaymentProofForm()
    if form.validate_on_submit():
        customer=Trans_users.query.filter_by(user_id=current_user.id).first()
        order=Orders.query.filter_by(id=id,customer=customer).first()
        proof_time=time(form.hours.data,form.minutes.data)
        today=date.today()
        dtime=datetime.combine(today,proof_time)
        payment=PaymentProof(bank_account_name=form.bank_account_name.data,bank_name=form.bank_name.data,
                             exact_money=form.exact_price.data,transfer_datetime=dtime,order=order)
        db.session.add(payment)
        db.session.commit()
        order.status = 'Sent'
        db.session.commit()
        flash('Payment Proof has been sent successfully. Please wait for the confirmation')
        return redirect(url_for('my_order'))
    return render_template('PaymentProof.html',title='Payment Proof Form',form=form)

@app.route('/manage_payment')
def manage_payment():
    return render_template('ManagePayment.html',title='Manage Payment',payments=PaymentProof.query.all())

@app.route('/manage_orders')
def manage_orders():
    return render_template('ManageOrders.html',title='Manage Orders',orders=Orders.query.all())

@app.route('/accept_payment/<int:id>')
def accept_payment(id):
    payment=PaymentProof.query.filter_by(order_id=id).first()
    order=Orders.query.filter_by(id=id).first()
    order.status = 'Accepted'
    db.session.commit()
    db.session.delete(payment)
    db.session.commit()
    flash('Complete the order now')
    return redirect(url_for('manage_orders'))

@app.route('/reject_payment/<int:id>')
def reject_payment(id):
    payment=PaymentProof.query.filter_by(order_id=id).first()
    order=Orders.query.filter_by(id=id).first()
    order.status = 'Rejected'
    db.session.commit()
    db.session.delete(payment)
    db.session.commit()
    flash('Redo the order now')
    return redirect(url_for('manage_orders'))

@app.route('/finish_orders/<int:id>')
def finish_orders(id):
    order=Orders.query.filter_by(id=id).first()
    transaction=Transactions(total_price=order.total_price,datestamp=datetime.now(),user_id=order.user_id)
    db.session.add(transaction)
    db.session.commit()
    for product in order.order_itemlists:
        trans_product=Trans_products.query.filter_by(product_id=product.product_id).first()
        transaction.add_into_trans_itemlists(trans_product)
        db.session.commit()
    for product in order.order_itemlists:
        order.remove_from_order_itemlists(product)
        db.session.commit()
    order.status = 'Done'
    db.session.commit()
    flash("Orders have been completed")
    return redirect(url_for('manage_orders'))

@app.route('/redo_orders/<int:id>')
def redo_orders(id):
    order=Orders.query.filter_by(id=id).first()
    order.status = 'Unpaid'
    db.session.commit()
    flash('Order has been redone')
    return redirect(url_for('manage_orders'))

@app.route('/clear_all_order_items/<int:id>')
def clear_all_order_items(id):
    order=Orders.query.filter_by(id=id).first()
    for item in order.order_itemlists:
        order.remove_from_order_itemlists(item)
        db.session.commit()
    flash('All order items have been cleared')
    return redirect(url_for('manage_orders'))

#Render My Transaction
@app.route('/my_transaction')
def my_transaction():
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    return render_template('MyTransactions.html',title='My Transaction',
                           transactions=Transactions.query.filter_by(customer=customer).all())

@app.route('/manage_transactions')
def manage_transactions():
    return render_template('ManageTransactions.html',title='Manage Transactions',transactions=Transactions.query.all())

@app.route('/send_products/<int:id>/<int:product_id>')
def send_products(id,product_id):
    transaction=Transactions.query.filter_by(id=id).first()
    library=Library_customers.query.filter_by(id=transaction.user_id).first()
    library_product=Library_products.query.filter_by(product_id=product_id).first()
    if not library.is_in_my_library(library_product):
        library.add_into_my_library(library_product)
        db.session.commit()
        flash('The item is sent to customer')
    else:
        flash('The item has been sent already')
    return redirect(url_for('manage_transactions'))

#Render Transaction List
@app.route('/my_transaction_list/<int:id>')
def my_transaction_list(id):
    customer=Trans_users.query.filter_by(user_id=current_user.id).first()
    return render_template('TransactionLists.html',title='Transaction Item Lists',
                       transaction=Transactions.query.filter_by(id=id,customer=customer).first(),customer=customer)

@app.route('/manage_transaction_items/<int:id>')
def manage_transaction_items(id):
    transaction=Transactions.query.filter_by(id=id).first()
    return render_template('ManageTransactionItems.html',title='Manage Transaction Items',transaction=transaction,
                           libraries=Library_products.query.all())

#Render My Library
@app.route('/my_library')
def my_library():
    return render_template('MyLibrary.html',title='My Library',user=Library_customers.query.filter_by(user_id=current_user.id).first())
