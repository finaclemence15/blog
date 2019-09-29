from flask import render_template,request,redirect,url_for
from . import main 
from ..models import Comment,Blog,User, PhotoProfile, Quote, Subscription
from ..request import get_quote
from .forms import UpdateProfile,CommentForm,UpdateProfile,AddBlogForm,SubscriptionForm,UpdateBlogForm
from flask_login import login_required, current_user
from ..import db,photos
from ..email import mail_message

# Views

@main.route('/', methods = ['GET', 'POST'])
def index():
 '''
   View root page function that returns the index page and its data
   '''
 form=SubscriptionForm()
 if form.validate_on_submit():
       name = form.name.data

       email= form.email.data
       new_subscriber=Subscription(name=name,email=email)
       db.session.add(new_subscriber)
       db.session.commit()

       mail_message("Thank you for your  subscribe","email/welcome_user",new_subscriber.email,user=new_subscriber)

       return redirect(url_for('main.index'))
 quote=get_quote()
 blogs=Blog.get_blogs()
 title= "WELCOME"

 return render_template('index.html',title=title,quote=quote,blogs=blogs ,subscription_form=form)

@main.route('/blog/new/', methods = ['GET','POST'])
@login_required
def create_blogs():
    form = AddBlogForm()


    if form.validate_on_submit():
        # category = form.category.data
        title = form.title.data 

        blog = form.content.data 
        content = form.content.data 

        new_blog = Blog(description=content,user=current_user, title=title)
        new_blog.save_blog()

        subscribers=Subscription.query.all()
        for subscriber in subscribers:
           mail_message("New Blog Post","email/send_email",subscriber.email,user=subscriber,blog=new_blog)

        return redirect(url_for('main.index'))


    title = "Add Post"   
    return render_template('blogs.html', title = title, blog_form = form)


@main.route('/comment/new/<int:id>', methods = ['GET','POST'])
# @login_required
def create_comments(id):
    form = CommentForm()
    blog= Blog.query.filter_by(id=id).first()

    if form.validate_on_submit():

        comment = form.comment.data
        username=form.username.data

        new_comment =Comment(content = comment , blog= blog)
        db.session.add(new_comment)
        db.session.commit()

    comments = Comment.get_comments(id=id)

    return render_template('comments.html', form=form ,comments=comments)

@main.route('/blog/<int:id>')
def blog(id):
    blog=Blog.query.filter_by(id=id).first()
    comments=Comment.get_comments(id=id)
    return render_template('blog.html',blog=blog,comments=comments)
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    '''
    View update pic profile function that returns the uppdate profile pic page
    '''
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))

@main.route('/delete/blog/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_blog(id):
    blog=Blog.query.filter_by(id=id).first()

    if blog is not None:
      blog.delete_blog()
    return redirect(url_for('main.index'))

@main.route('/delete/comment/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
    comment=Comment.query.filter_by(id=id).first()

    if comment is not None:
      comment.delete_comment()
    return redirect(url_for('main.index'))


@main.route('/edit/blog/<int:id>',methods= ['GET','POST'])
@login_required
def update_blog(id):
   blog=Blog.query.filter_by(id=id).first()
   if blog is None:
        abort(404)

   form=UpdateBlogForm()

   if form.validate_on_submit():
         blog.title=form.title.data
         blog.content=form.content.data

         db.session.add(blog)
         db.session.commit()

         return redirect(url_for('main.index'))
   return render_template('update_blog.html',form=form)
