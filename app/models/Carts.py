from app import db

carts=db.Table('carts',db.Column('user_id',db.Integer(),db.ForeignKey('cart_customers.id')),
               db.Column('product_id',db.Integer(),db.ForeignKey('cart_products.id')),
               info={'bind_key': 'carts'})

class Cart_customers(db.Model):
    __bind_key__ = 'carts'
    id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),nullable=False)
    my_carts=db.relationship('Cart_products',secondary=carts,
                                    lazy='dynamic',backref=db.backref('user',lazy='dynamic'))

    def is_in_my_carts(self,product):
        return self.my_carts.filter(carts.c.product_id == product.id).count() > 0

    def add_into_my_carts(self,product):
        if not self.is_in_my_carts(product):
            self.my_carts.append(product)

    def remove_from_my_carts(self,product):
        if self.is_in_my_carts(product):
            self.my_carts.remove(product)

    def my_carts_is_empty(self):
        return self.my_carts.count() > 0

class Cart_products(db.Model):
    __bind_key__ = 'carts'
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(128),nullable=False,unique=True,index=True)
    price=db.Column(db.Integer(),nullable=False)
    image=db.Column(db.String(256),nullable=False,unique=True,index=True)
    product_id=db.Column(db.Integer(),nullable=False)
