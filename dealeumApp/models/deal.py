from datetime import datetime
from flask_restx.inputs import date
from slugify import slugify
from sqlalchemy.orm import defaultload
from dealeumApp import db




    
# user_roles_table = db.Table('user_roles',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
# )


deal_upvotes_table = db.Table('deal_upvotes',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('deal_id',db.Integer(),db.ForeignKey('deals.id')),
    )

deal_downvotes_table = db.Table('deal_downvotes',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('deal_id',db.Integer(),db.ForeignKey('deals.id')),
    )

class Deal(db.Model):
    __tablename__ = 'deals'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(320), nullable=False)
    slug = db.Column(db.String(500),unique=True, nullable=True)
    url = db.Column(db.Text())
    message = db.Column(db.Text())
    new_price = db.Column(db.Float())
    old_price = db.Column(db.Float())
    start_date = db.Column(db.DateTime(), nullable=True, default=datetime.utcnow)
    end_date = db.Column(db.DateTime(), nullable=True)
    ended = db.Column(db.Boolean(),default=False)
    views = db.Column(db.Integer(), default= 0)
    category_id = db.Column(db.Integer(),db.ForeignKey('categories.id'))
    category = db.relationship('Category')
    store_id = db.Column(db.Integer(),db.ForeignKey('stores.id'))
    store = db.relationship('Store')
    updated_from = db.Column(db.Integer(),db.ForeignKey('deals.id'), default=None,nullable=True)
    updated_at = db.Column(db.DateTime(), nullable=True,default=None)
    show = db.Column(db.Boolean(), default = True)
    latest = db.Column(db.Boolean(),default = True)
    points = db.Column(db.Integer(), default = 0)
    deal_upvotes = db.relationship("User",secondary = deal_upvotes_table, back_populates = "deal_upvotes")
    deal_downvotes = db.relationship("User",secondary = deal_downvotes_table, back_populates = "deal_downvotes")
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    author = db.relationship('User')
    deal_image = db.Column(db.String(127),nullable=False, default='default_deal.jpg')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    

    def set_slug(self):
        self.slug = slugify(self.title+ " " + str(self.id))

    def __repr__(self):
        return f"Deal('{self.id}','{self.title}','{self.title}','{self.old_price}','{self.new_price}','{self.created_at}')"



comment_upvotes_table = db.Table('comment_upvotes',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('comment_id',db.Integer(),db.ForeignKey('comments.id')),
    )

comment_downvote_table = db.Table('comment_downvotes',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('comment_id',db.Integer(),db.ForeignKey('comments.id')),
    )

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(),primary_key=True)
    message = db.Column(db.Text())
    points = db.Column(db.Integer(), default = 0)

    updated_from = db.Column(db.Integer(),db.ForeignKey('comments.id'), nullable=True, default= None)
    updated_at = db.Column(db.DateTime(), nullable=True, default=None)
    latest = db.Column(db.Boolean(),default = True)
    created_at = db.Column(db.DateTime(),default=datetime.utcnow)
    comment_upvotes = db.relationship("User",secondary = comment_upvotes_table, back_populates = "comment_upvotes")
    comment_downvotes = db.relationship("User",secondary = comment_downvote_table, back_populates = "comment_downvotes")
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship('User')
    deal_id = db.Column(db.Integer(),db.ForeignKey('deals.id'))
    deal = db.relationship('Deal')
    
    def __repr__(self):
        return f"Comment('{self.id}','{self.message}','{self.user_id}')"

