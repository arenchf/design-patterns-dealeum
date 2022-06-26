from datetime import datetime
from dealeumApp import db, login_manager
from flask_login import UserMixin   
from werkzeug.security import check_password_hash
from dealeumApp.models.deal import deal_downvotes_table, deal_upvotes_table, comment_downvote_table, comment_upvotes_table

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    
user_roles_table = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(63), unique=True,nullable=False)
    roles = db.relationship('Role',secondary=user_roles_table, backref=db.backref('users',lazy="dynamic"),lazy='dynamic')
    deals = db.relationship('Deal',backref='user',lazy=True)
    profile_image = db.Column(db.String(127),nullable=False, default='default_user.jpg')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    deal_upvotes = db.relationship("Deal",secondary = deal_upvotes_table, back_populates = "deal_upvotes")
    deal_downvotes = db.relationship("Deal",secondary = deal_downvotes_table, back_populates = "deal_downvotes")
    comment_upvotes = db.relationship("Comment",secondary = comment_upvotes_table, back_populates = "comment_upvotes")
    comment_downvotes = db.relationship("Comment",secondary = comment_downvote_table, back_populates = "comment_downvotes")
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.roles}')"
    
    def verify_password(self,pwd):
        return check_password_hash(self.password, pwd)
    

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50),unique=True)

    def __repr__(self):
        return f"Role('{self.id}','{self.name}')"


# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id',ondelete='CASCADE'))


