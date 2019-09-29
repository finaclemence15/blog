from . import db
from werkzeug.security import generate_password_hash,check_password_hash
# from flask_sqlalchemy import flask_SQLAlchemy
from flask_login import UserMixin
from . import login_manager


class Quote:
  '''
  Quote class to define quote objects
  '''

  def __init__(self,id,author,content):
    self.id=id
    self.author=author
    self.content=content


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    blog = db.relationship('Blog', backref = 'user', lazy='dynamic')
    all_comments = db.relationship('Comment',backref = 'user',lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255)) 
    

    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)

    
    def __repr__(self):
        return f'User {self.username}'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))   

class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    description = db.Column(db.String(255))
    comments = db.relationship('Comment',backref = 'blog',lazy='dynamic')


    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def clear_blogs(cls):
        Blog.search_blogs.clear()

    @classmethod
    def get_bloge(cls):
        blogs=Blogs.query.all()
        return blogs


    @classmethod 
    def get_blogs(cls):
        blogs = Blog.query.filter_by().all()
        return blogs
    

    def delete_blog(self):
       
        db.session.delete(self)
        db.session.commit()
    

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    content = db.Column(db.String(255))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments=Comment.query.filter_by(blog_id=id).all()
        return comments
    

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    


class Subscription(db.Model):
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    email =db.Column(db.String(255), unique = True , index = True)

