
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import current_user, login_required
from dealeumApp.functions.decorators.auth import login_required_restx
from dealeumApp.models.deal import Comment, Deal
from dealeumApp import db


dealsbp = Blueprint('deal', __name__)



@dealsbp.route('/add',methods=['GET','POST'])
@login_required
def add_deal():
    
    if request.method == 'POST':
        
        print("ADD")
        flash("Deal has successfully created")
        print(request.form.to_dict())
        return redirect(url_for('main.home'))
    
    print("GETTING")
    return render_template('deal/deal_add.html')


@dealsbp.route('/<deal_slug>')
def deal_detail(deal_slug):
    # deal_id = request.args.get('deal_id')
    deal = Deal.query.filter_by(slug=str(deal_slug)).first()
    
    print("DEAL DETAILS")
    print(deal)
    print("UPVOTES ",deal.deal_upvotes)
    comments = Comment.query.filter_by(deal_id=deal.id).all()
    return render_template('deal/deal_detail.html',deal=deal,comments=comments)



@dealsbp.route('/<deal_slug>/comments', methods=['POST','DELETE'])
def deal_comment(deal_slug):
    if request.method == 'DELETE':
        # DELETE ALL COMMENTS FROM A DEAL
        pass
    
    
    # ADD COMMENT TO A DEAL

    if request.form.get("comment"):
        comment_message = request.form.get("comment")
    
    else:
        return make_response(jsonify(success=False, error_message='No comment message found'),400)
    
    print("CURRENT USER ID", current_user.id)
    deal = Deal.query.filter_by(slug=deal_slug).first()
    comment = Comment(message= comment_message,user_id=current_user.id,deal_id=deal.id)

    db.session.add(comment)
    db.session.commit()

    
    
    print("COMMENT ADDED")
    return redirect(url_for('deal.deal_detail',deal_slug=deal_slug))



