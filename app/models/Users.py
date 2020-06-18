from app import db,login
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime
from flask_login import UserMixin


class Users(UserMixin,db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True,nullable=False)
    email=db.Column(db.String(128),index=True,unique=True,nullable=False)
    first_name=db.Column(db.String(128),index=True,nullable=False)
    last_name=db.Column(db.String(128),index=True,nullable=False)
    phone_number=db.Column(db.String(15),index=True,unique=True,nullable=False)
    password_hash=db.Column(db.String(256),nullable=False)
    usertype=db.Column(db.String(20),index=True,nullable=False)
    created_at=db.Column(db.DateTime(),default=datetime.now())
    updated_at=db.Column(db.DateTime(),default=datetime.now())

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

