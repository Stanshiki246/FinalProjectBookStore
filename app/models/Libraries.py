from app import db

libraries=db.Table('libraries',db.Column('user_id',db.Integer(),db.ForeignKey('library_customers.id')),
               db.Column('product_id',db.Integer(),db.ForeignKey('library_products.id')),
               info={'bind_key': 'libraries'})

class Library_customers(db.Model):
    __bind_key__ = 'libraries'
    id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),nullable=False)
    my_libraries=db.relationship('Library_products',secondary=libraries,
                                    lazy='dynamic',backref=db.backref('user',lazy='dynamic'))

    def is_in_my_library(self,product):
        return self.my_libraries.filter(libraries.c.product_id == product.id).count() > 0

    def add_into_my_library(self,product):
        if not self.is_in_my_library(product):
            self.my_libraries.append(product)

    def remove_from_my_library(self,product):
        if self.is_in_my_library(product):
            self.my_libraries.remove(product)

    def my_library_is_empty(self):
        return self.my_libraries.count() > 0


class Library_products(db.Model):
    __bind_key__ = 'libraries'
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(128),nullable=False,unique=True,index=True)
    booktype=db.Column(db.String(20),index=True,nullable=False)
    author=db.Column(db.String(128),index=True,nullable=False)
    image=db.Column(db.String(256),nullable=False,unique=True,index=True)
    product_id=db.Column(db.Integer(),nullable=False)
    page_files=db.relationship('Comics',backref='product',lazy='dynamic')

class Comics(db.Model):
    __bind_key__ = 'libraries'
    id=db.Column(db.Integer(),primary_key=True)
    filename=db.Column(db.String(256),index=True,nullable=False)
    page_num=db.Column(db.Integer(),nullable=False)
    product_id=db.Column(db.Integer(),db.ForeignKey('library_products.id'))
