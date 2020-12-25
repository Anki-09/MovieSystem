from app import app,db
from datetime import datetime
from app.forms import LoginForm,RegistrationForm,EditProfileForm,ReviewForm
from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user,login_user
from flask_login import logout_user,login_required
from app.models import User,movie_details,Reviews
from werkzeug.urls import url_parse
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
             next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In',form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form )
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form )
@app.route('/index/<lang>')
def language(lang):
    return render_template('language.html',lang=lang)
@app.route('/index/<lang>/<mtype>')
def movie(lang,mtype):
    con=movie_details.query.all()
    results = [
                {
                    "name": one.name,
                    "lang": one.lang,
                    "mtype":one.mtype,
                    "image":one.image,
                    "rating":one.rating,
                    "desc":one.desc
                } for one in con]
    return render_template('mtype.html',lang=lang,mtype=mtype,results=results)
@app.route('/index/<lang>/<mtype>/<mname>/review')
def seeReview(lang,mtype,mname):
    mov=movie_details.query.filter_by(lang=lang,mtype=mtype,name=mname).first()
    con=Reviews.query.filter_by(movie_id=mov.id).all()
    dictreview = [ 
            {
                "username":User.query.filter_by(id=one.user_id).first().username,
                "comment":one.comment,
                "rate":one.rate,
                "timestamp":one.timestamp
                }for one in con]
    return render_template('review.html',lang=lang,mtype=mtype,mname=mname,dictreview=dictreview)
@app.route('/index/<lang>/<mtype>/<mname>/addreview',methods=['GET', 'POST'])
def addReview(lang,mtype,mname):
    form=ReviewForm()
    if form.validate_on_submit():
        obj1=movie_details.query.filter_by(lang=lang,mtype=mtype,name=mname).first()
        obj = Reviews(comment=form.comment.data, rate=form.rate.data,user_id=current_user.id, movie_id=obj1.id)
        db.session.add(obj)
        rating=0.0
        count=0
        for one in Reviews.query.filter_by(movie_id=obj1.id).all():
            rating+=one.rate
            count+=1
        obj1.rating=round(rating/count,2)
        db.session.commit()
        flash('Successfully added review')
        return redirect(url_for('addReview',lang=lang,mtype=mtype,mname=mname))
    return render_template('addreview.html',mname=mname,form=form)
