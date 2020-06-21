from app import db
from datetime import datetime,timedelta

order_items=db.Table('order_items',db.Column('order_id',db.Integer(),db.ForeignKey('orders.id')),
                     db.Column('product_id',db.Integer(),db.ForeignKey('trans_products.id')),
                     info={'bind_key': 'transactions'})
trans_items=db.Table('trans_items',db.Column('trans_id',db.Integer(),db.ForeignKey('transactions.id')),
                     db.Column('product_id',db.Integer(),db.ForeignKey('trans_products.id')),
                     info={'bind_key': 'transactions'})

class Trans_users(db.Model):
    __bind_key__ = 'transactions'
    id = db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True,nullable=False)
    email=db.Column(db.String(128),index=True,unique=True,nullable=False)
    first_name=db.Column(db.String(128),index=True,nullable=False)
    last_name=db.Column(db.String(128),index=True,nullable=False)
    phone_number=db.Column(db.String(15),index=True,unique=True,nullable=False)
    user_id=db.Column(db.Integer(),nullable=False)
    my_orders=db.relationship('Orders',backref='customer',lazy='dynamic')
    my_trans=db.relationship('Transactions',backref='customer',lazy='dynamic')


class Trans_products(db.Model):
    __bind_key__ = 'transactions'
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(128),nullable=False,unique=True,index=True)
    price=db.Column(db.Integer(),nullable=False)
    image=db.Column(db.String(256),nullable=False,unique=True,index=True)
    product_id=db.Column(db.Integer(),nullable=False)

class Orders(db.Model):
    __bind_key__ = 'transactions'
    id=db.Column(db.Integer(),primary_key=True)
    total_price=db.Column(db.Integer(),nullable=False)
    status=db.Column(db.String(128),default="Unpaid",index=True,nullable=False)
    datestamp=db.Column(db.DateTime(),default=datetime.now())
    deadline=db.Column(db.DateTime(),default=datetime.now()+timedelta(days=1))
    user_id=db.Column(db.Integer(),db.ForeignKey('trans_users.id'))
    order_itemlists=db.relationship('Trans_products',secondary=order_items,lazy='dynamic',
                                    backref=db.backref('order',lazy='dynamic'))

    def is_in_order_itemlists(self,product):
        return self.order_itemlists.filter(order_items.c.product_id == product.id).count() > 0

    def add_into_order_itemlists(self,product):
        if not self.is_in_order_itemlists(product):
            self.order_itemlists.append(product)

    def remove_from_order_itemlists(self,product):
        if self.is_in_order_itemlists(product):
            self.order_itemlists.remove(product)

    def order_itemlists_is_empty(self):
        return self.order_itemlists.count() > 0


class Transactions(db.Model):
    __bind_key__ = 'transactions'
    id=db.Column(db.Integer(),primary_key=True)
    total_price=db.Column(db.Integer(),nullable=False)
    datestamp=db.Column(db.DateTime(),default=datetime.now())
    user_id=db.Column(db.Integer(),db.ForeignKey('trans_users.id'))
    trans_itemlists=db.relationship('Trans_products',secondary=trans_items,lazy='dynamic',
                                    backref=db.backref('transaction',lazy='dynamic'))

    def is_in_trans_itemlists(self,product):
        return self.trans_itemlists.filter(trans_items.c.product_id == product.id).count() > 0

    def add_into_trans_itemlists(self,product):
        if not self.is_in_trans_itemlists(product):
            self.trans_itemlists.append(product)

    def remove_from_trans_itemlists(self,product):
        if self.is_in_trans_itemlists(product):
            self.trans_itemlists.remove(product)

    def clear_trans_itemlists(self):
        self.trans_itemlists.clear()

class PaymentProofs(db.Model):
    __bind_key__ = 'transactions'
    id=db.Column(db.Integer(),primary_key=True)
    bank_account_name=db.Column(db.String(256),nullable=False,index=True)
    bank_name=db.Column(db.String(256),nullable=False,index=True)
    exact_money=db.Column(db.Integer(),nullable=False)
    transfer_date=db.Column(db.String(128),nullable=False)
    order_id=db.Column(db.Integer(),nullable=False)

