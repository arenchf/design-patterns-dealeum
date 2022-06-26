from flask_restx import Resource, fields, reqparse, abort, Namespace, Model
from flask_restx.marshalling import marshal_with
from dealeumApp.functions.decorators.auth import roles_accepted, login_required_restx
from flask import request, flash, jsonify, make_response, session
from flask_login import current_user, login_required
from dealeumApp.models.deal import Comment, Deal
from dealeumApp.models.category import Category
from dealeumApp import db
import json

api = Namespace('api/v1', description='Deals operations')

return_deal = api.model('Deal',{
    'id':fields.Integer(readonly=True),
    'slug':fields.String(required=True),
})

parser = reqparse.RequestParser()
parser.add_argument('title',type=str,required=True)
parser.add_argument('message',type=str)
parser.add_argument('new_price',type=float,required=True)
parser.add_argument('old_price',type=float)
parser.add_argument('deal_url',type=str)

@api.route('/deals/<string:slug>')
class DealDetail(Resource):
    @api.marshal_with(return_deal,200)
    # @login_required_restx
    def get(self,slug):
        print("HELLO, ",slug)
        deal = Deal.query.filter_by(slug=slug).first()
        if deal:
            return deal,200
        else:
            abort(404,'Deal not found')

@api.route('/deals')
class DealList(Resource):
    @api.marshal_with(return_deal,201)
    @api.doc('create_deal')
    # @login_required_restx
    # @roles_accepted("Admin")
    def post(self):
        '''Create a new deal'''
        args = parser.parse_args()
        deal = Deal(title=args['title'],message=args['message'],new_price=args['new_price'],old_price=args['old_price'],url=args['deal_url'],author=current_user)
        db.session.add(deal)
        db.session.flush([deal])
        deal.set_slug()
        
        db.session.commit()
        flash("Deal has been created","success")
        return deal,201;

    def delete(self):
        '''Delete the deal'''

        deal = Deal.query.filter_by(slug="neue-titel").first()

        db.session.delete(deal)
        db.session.commit()
        return {'message':'success'},200


vote_parser = api.parser()
vote_parser.add_argument('voteType',type=str,choices=('upvote', 'downvote'), required=True, help="The type of the vote")


@api.route('/deals/<string:slug>/votes')
class DealVotes(Resource):
    
    # @login_required_restx
    # @api.expect(vote_parser)
    def put(self,slug):
        print("HI")
        print(request.args)
        deal = Deal.query.filter_by(slug=slug).first()
        args = vote_parser.parse_args()
        print(args)
        voteType = args['voteType']
        print(voteType)
        wasVoted = False
        if voteType == "upvote":

            if deal in current_user.deal_upvotes:
                current_user.deal_upvotes.remove(deal)
                deal.points -=1
                db.session.commit()
                return {'success':True,'message':'Successfully upvoted','wasVoted':wasVoted, 'removed':True}, 200

            if deal in current_user.deal_downvotes:
                wasVoted = True
                current_user.deal_downvotes.remove(deal)
                deal.points += 1

            current_user.deal_upvotes.append(deal)
            deal.points += 1
            db.session.commit()

            return {'success':True,'message':'Successfully upvoted','wasVoted':wasVoted, 'removed':False}, 200

        elif voteType == "downvote":
            if deal in current_user.deal_downvotes:
                current_user.deal_downvotes.remove(deal)
                deal.points +=1
                db.session.commit()
                return {'success':True,'message':'Successfully downvoted','wasVoted':wasVoted, 'removed':True}, 200
            
            
            if deal in current_user.deal_upvotes:
                wasVoted = True
                current_user.deal_upvotes.remove(deal)
                deal.points -= 1

            current_user.deal_downvotes.append(deal)
            deal.points -= 1
            db.session.commit()
            return {'success':True,'message':'Successfully downvoted','wasVoted':wasVoted, 'removed':False}, 200
            
        




role_dao = {
    'name': fields.String,
}

user_dao = {
    'id': fields.Integer,
    'username': fields.String,
    'profile_image': fields.String,
    'roles':fields.List(fields.Nested(role_dao))
}
deal_dao = {
    'id': fields.Integer,
    'title':fields.String,
    'points':fields.Integer,
    'new_price':fields.Float,
    'old_price':fields.Float,
    'message':fields.String,
}

returned_comment = {
    'message': fields.String,
    'points':fields.Integer,
    'created_at':fields.DateTime,
    'deal': fields.Nested(deal_dao),
    'user': fields.Nested(user_dao),
}

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('message',type=str,required=True)

@api.route('/deals/<string:slug>/comments')
class CommentsList(Resource):

    @api.marshal_with(returned_comment,201)
    # @login_required_restx
    def post(self,slug):
        args = comment_parser.parse_args()
        deal = Deal.query.filter_by(slug=slug).first()
        comment = Comment(message=args['message'],user=current_user, deal=deal)
        db.session.add(comment)
        db.session.commit()
        return comment,201

    def get(self):
        pass



category_dao = {
    'name': fields.String,
    'slug': fields.String,
    'image': fields.String,
    'id':fields.Integer,
    'super_category_id':fields.Integer,
    }
category_dao_nested = {
    'name': fields.String,
    'slug': fields.String,
    'image': fields.String,
    'id':fields.Integer,
    'super_category_id':fields.Integer,
    'super_category':fields.Nested(category_dao)
}


category_parser = reqparse.RequestParser()
category_parser.add_argument('name',type=str,required=True)
category_parser.add_argument('superCategoryName',type=str,required=False)
category_parser.add_argument('superCategoryId',type=int,required=False)

@api.route('/categories')
class CategoryList(Resource):

    @api.marshal_with(category_dao_nested,200)
    @api.doc('get the list of categories')
    def get(self):
        categories = Category.query.all()
        return categories,200

    @api.marshal_with(category_dao_nested,201)
    @api.expect(category_parser)
    def post(self):
        args = category_parser.parse_args()
        super_category = None
        if args['superCategoryId']:
            found_category:Category = Category.query.filter_by(id=args['superCategoryId']).first()
            if found_category != None:
                super_category = found_category

        elif args['superCategoryName']:
            found_category:Category = Category.query.filter_by(name=args['superCategoryName']).first()
        
            if found_category != None:
                super_category = found_category

        if super_category == None:
            category = Category(name=args['name'])
        else:
            category = Category(name=args['name'],super_category=super_category)

        db.session.add(category)
        db.session.flush([category])
        category.set_slug()
        db.session.commit()
        return category, 201



change_category_parser = reqparse.RequestParser()
change_category_parser.add_argument('name',type=str,required=False)
change_category_parser.add_argument('active',type=bool,required=False)

@api.route('/categories/<string:slug>')
class CategoryDetail(Resource):

    
    @api.doc('get a category')
    @api.marshal_with(category_dao_nested,200)
    def get(self,slug):
        category = Category.query.filter_by(slug=slug).first()

        if category != None:
            return category ,200
        else:
            return {'success':False,'message':'Category not found'}, 404


    @api.expect(change_category_parser)
    def put(self,slug):
        category:Category = Category.query.filter_by(slug=slug).first()
        
        if category == None:
            return {'success':False,'message':'Category not found'}, 404

        elif category != None:
            args = vote_parser.parse_args()

            if args['name'] == None:
                category.name = args['name']
            if args['active'] == None:
                category.active = args['active']
            
            

        db.session.commit()
        return category, 200

        



 

    


category_search_parser = reqparse.RequestParser()
category_search_parser.add_argument('searchArgument',type=str,required=True)

@api.route('/categories/search')
class CategorySearch(Resource):
    pass
