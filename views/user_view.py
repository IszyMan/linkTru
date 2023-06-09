from flask import Blueprint, render_template, redirect, url_for, request, flash
from forms import *
from models import *
from extensions import db
from flask_login import login_user, login_required, current_user


user_blp = Blueprint("user_blp", __name__)


@user_blp.route('/', methods=["GET", "POST"])
def home():
    form = GenerateBrandName()
    # posts = CreateProfile.query.all()
    if request.method == "POST":
        brand_name = request.form.get('brandname').lower()
        if not brand_name:
            flash('Input Required', 'danger')
            return redirect(url_for('user_blp.home'))
        user_ = User.query.filter_by(brand_name=brand_name).first()
        if user_:
            # User with that brand already exists
            flash("Brand Name already exists!", "danger")
            return redirect(url_for('user_blp.home'))
        return redirect(url_for('auth_blp.register', brandie=brand_name))
    return render_template("index.html", form=form)


@user_blp.route('/join', methods=["GET", "POST"])
def join():
    # Every render_template has a logged_in variable set.
    form = GenerateBrandName()
    if request.method == "POST":
        brand_name = request.form.get('brandname')
        user_ = User.query.filter_by(brand_name=brand_name).first()
        if user_:
            # User already exists
            flash("Brand Name already exists!")
            return redirect(url_for('home'))

        new_user = User(brand_name=brand_name)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("auth_blp.register"))
    return render_template("join.html", form=form, current_user=current_user)


@user_blp.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    form = CreatePostForm()
    brand_url = f"{request.host_url}{current_user.brand_name}"
    posts = CreateProfile.query.all()
    if form.validate_on_submit():
        new_post = CreateProfile(
            linkname=form.linkname.data,
            yourlink=form.yourlink.data,
            product=form.product.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("user_blp.admin"))
    return render_template("admin.html", all_posts=posts,
                           name=current_user.first_name.title(),
                           logged_in=True,
                           form=form,
                           brand_url=brand_url)


@user_blp.route('/<path:sub_path>', methods=["GET", "POST"])
def profile(sub_path):
    requested_profile = ''
    all_profiles = User.query.all()
    for profiles in all_profiles:
        if profiles.first_name == sub_path:
            requested_profile = profiles
    return render_template("profile.html", all_posts=requested_profile, current_user=current_user)


# @user_blp.route('/', subdomain="<brandie>")
# def brand(brandie):
#     check_brand = User.query.filter_by(brand_name=brandie.lower()).first()
#     if not check_brand:
#         return render_template("404.html")
#     return render_template("brand.html", brandie=brandie.upper())

@user_blp.route('/<brandname>/', methods=["GET", "POST"])
def brand(brandname):
    check_brand = User.query.filter_by(brand_name=brandname.lower()).first()
    if not check_brand:
        return render_template("404.html")
    return render_template("brand.html", brandie=brandname.upper())


@user_blp.route('/<brandname>/<linkname>', methods=["GET", "POST"])
def product(brandname, linkname):
    check_brand = User.query.filter_by(brand_name=brandname.lower()).first()
    if not check_brand:
        return render_template("404.html")
    check_product = CreateProfile.query.filter_by(linkname=linkname.lower()).first()
    if not check_product:
        return render_template("404.html")
    return render_template("product.html", brandie=brandname.upper(), linkname=linkname.upper())
