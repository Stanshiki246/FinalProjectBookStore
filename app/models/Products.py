from app import db
from datetime import datetime



wishlists=db.Table('wishlists',db.Column('user_id',db.Integer(),db.ForeignKey('customers.id')),
                   db.Column('product_id',db.Integer(),db.ForeignKey('products.id')),
                   info={'bind_key': 'products'})

class Customers(db.Model):
    __bind_key__ = 'products'
    id = db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),nullable=False)
    wished_products=db.relationship('Products',secondary=wishlists,
                                    lazy='dynamic',backref=db.backref('user',lazy='dynamic'))

    def add_into_wishlist(self,product):
        if not self.is_in_wishlist(product):
            self.wished_products.append(product)

    def remove_from_wishlist(self,product):
        if self.is_in_wishlist(product):
            self.wished_products.remove(product)

    def is_in_wishlist(self,product):
        return self.wished_products.filter(wishlists.c.product_id == product.id).count() > 0

    def clear_wishlist(self):
        self.wished_products.clear()


class Products(db.Model):
    __bind_key__ = 'products'
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(128),index=True,unique=True,nullable=False)
    price=db.Column(db.Integer(),index=True,nullable=False)
    created_at=db.Column(db.DateTime(),default=datetime.now())
    updated_at=db.Column(db.DateTime(),default=datetime.now())
    image=db.Column(db.String(256),index=True,unique=True,nullable=False)
    booktype=db.Column(db.String(20),index=True,nullable=False)
    genres=db.Column(db.String(256),index=True,nullable=False)
    synopsis=db.Column(db.String(512),index=False,nullable=False)
    author=db.Column(db.String(128),index=True,nullable=False)



    def __repr__(self):
        return '<Books {}>'.format(self.title)



