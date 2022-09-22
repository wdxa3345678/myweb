from flask import render_template,redirect,url_for,flash,request,Blueprint
from flask_login import login_user,login_required,current_user,logout_user
from my_portfolio_website import db
from my_portfolio_website.models import User,Blogpost
from my_portfolio_website.users.forms import RegisterForm,LoginForm,UpdateUserForm
from my_portfolio_website.users.picture_handler import add_profile_pic

users=Blueprint("users",__name__)

@users.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,
                  password=form.password.data,
                  username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash("註冊成功!")
        return redirect(url_for("users.login"))
    return render_template("register.html",form=form)

@users.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("登入成功")
            next=request.args.get("next")
            if next==None or not next[0]=="/":
                next=url_for("core.index")
            return redirect(next)
        else:
            flash("信箱或密碼錯誤，請重新輸入正確的信箱及密碼")
            return redirect(url_for("users.login"))
    return render_template("login.html",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/account",methods=["GET","POST"])
@login_required
def account():
    form=UpdateUserForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username=current_user.username
            pic=add_profile_pic(form.picture.data,username)
            current_user.profile_image=pic
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("帳號資料已更新")
        return redirect(url_for("users.account"))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.email.data=current_user.email
    profile_image=url_for("static",filename="profile_pics/"+current_user.profile_image)
    return render_template("account.html",profile_image=profile_image,form=form,current_user=current_user)

@users.route("/<username>")
def user_posts(username):
    page=request.args.get("page",1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    blog_posts=User.query.filter_by(author=user).order_by(Blogpost.data.desc()).paginate(page=page,per_page=5)#desc:descending  asc：ascending
    return render_template("user_blog_posts.html",blog_posts=blog_posts,user=user)