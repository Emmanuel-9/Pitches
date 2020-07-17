from . import main
from flask import render_template,request,redirect,url_for,abort,flash
from ..models import Pitch,User,Comment
from flask_login import login_required,current_user
from .forms import PitchForm,UpdateProfile,CommentForm
from .. import db
import markdown2


@main.route('/')
def index():

  title = 'Pitches'  

  return render_template('index.html',title = title)

@main.route('/pitch')
def pitches():
  pitches = Pitch.query.all()
  brand = Pitch.query.filter_by(category='Brand').all()
  product = Pitch.query.filter_by(category='Product').all()
  project = Pitch.query.filter_by(category='Project').all()
  investor = Pitch.query.filter_by(category='Investor').all()

  return render_template('pitches.html',pitches=pitches,brand=brand,product=product,project=project,investor=investor)


@main.route('/pitch/new',methods = ['GET','POST'])
@login_required
def new_pitch():
  form = PitchForm()

  if form.validate_on_submit():
    title=form.title.data
    category = form.category.data
    pitch = form.pitch.data
    author = current_user
    new_pitch = Pitch(title=title,category=category,pitch=pitch,author=current_user._get_current_object().id)

    db.session.add(new_pitch)
    db.session.commit()

    flash('Awesome! Pitch created','success')
    return redirect(url_for('main.pitches',id=new_pitch.id))

  return render_template('newpitches.html',title='Add Your Pitch',pitch_form=form)

@main.route('/user/<uname>')
def profile(uname):
  user = User.query.filter_by(username=uname).first()

  if user is None:
    abort(404)

  return render_template('profile/profile.html',user=user)

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
  user = User.query.filter_by(username=uname).first()

  if user is None:
    abort (404)
  form = UpdateProfile()

  if form.validate_on_submit():
    user.bio = form.bio.data

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('.profile',uname=user.username))

  return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods=['POST'])
@login_required
def update_pic(uname):
  user = User.query.filter_by(username=uname).first()
  if 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    user.profile_pic_path = path
    db.session.commit()

  return redirect(url_for('main.profile',uname=uname))

@main.route('/comments/<int:id>',methods=['GET','POST'])
def comment_review(id):
  comment = CommentForm()
  pitch=Pitch.query.get(id)

  if comment.validate_on_submit():
    content = comment.comment.data
    
    new_post = Comment(comment=content,title=pitch.id)

    db.session.add(new_post)
    db.session.commit()  
    
  post = 'Post Your Comment'
  user=User.query.get(id)
  comments = Comment.query.filter_by(title=pitch.id).all()  
  if pitch is None:
    abort(404)
        
  # format_comment = markdown2.markdown(comment.,extras=["code-friendly", "fenced-code-blocks"])
  return render_template('comments.html',comment_form=comment,post=post,comments=comments,pitch=pitch,user=user)