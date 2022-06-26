from datetime import datetime
from slugify import slugify
from dealeumApp import db



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    slug = db.Column(db.String(256))
    image = db.Column(db.String(256),default="default_category.jpg")
    active = db.Column(db.Boolean(),nullable=False,default=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    super_category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    super_category = db.relationship('Category', remote_side=[id])

    def __init__(self, *args, **kwargs):
        # if not 'slug' in kwargs:
        #     self.slug=slugify(kwargs.get('name'))
        super().__init__(*args,**kwargs)
    
    def set_slug(self):
        self.slug = slugify(self.name+ " " + str(self.id))

    def __repr__(self):
        return f"Category('{self.id}','{self.name}','{self.slug}','{self.super_category.name}')"



class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(128),unique=True,nullable=False)
    slug = db.Column(db.String(256))
    image = db.Column(db.String(256),default="default_store.jpg")

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            self.slug =slugify(kwargs.get('name'))
        super().__init__(*args,**kwargs)
