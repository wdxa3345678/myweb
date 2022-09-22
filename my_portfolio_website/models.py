from my_portfolio_website import db,login_manager
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__="users"

    id=db.Column(db.Integer,primary_key=True,nullable=False)
    profile_image=db.Column(db.String(20),nullable=False,default="default_profile.png")
    email=db.Column(db.String(64),unique=True, index=True)
    username=db.Column(db.String(64),unique=True,index=True)
    password_hash=db.Column(db.String(128))

    posts=db.relationship("Blogpost",backref="author",lazy=True)
    comments=db.relationship("Comment",back_populates="comment_author")

    def __init__(self,email,username,password):
        self.email=email
        self.username=username
        self.password=generate_password_hash(password,method="pbkdf2:sha256",salt_length=8)

    def check_password(self,password):
        return check_password_hash(self.password,password)

class Blogpost(db.Model):
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    text=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,nullable=False)

    author = db.relationship("User",back_populates="post")
    comments=db.relationship("Comment",back_populates="parent_post")


    def __init__(self,title,text,user_id):
        self.text=text
        self.title=title
        self.user_id=user_id


class Comment(db.Model):
    __tablename__="comments"
    id=db.Column(db.Integer,primary_key=True)
    post_id=db.Column(db.Integer,db.ForeignKey("blog_posts.id"))
    author_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    text=db.Column(db.Text,nullable=False)

    parent_post=db.relationship("Blogpost",back_populates="comments")
    comment_author=db.relationship("User",back_populates="comments")

    def __init__(self,post_id,author_id,text):
        self.post_id=post_id
        self.author_id=author_id
        self.text=text