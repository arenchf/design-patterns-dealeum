from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from dealeumApp.models.deal import Deal
import json

main = Blueprint('main', __name__)

@main.route('/',methods=['GET'])
def home():
    
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1

    per_page = 5
    deals = Deal.query.order_by(Deal.id.desc()).paginate(page,per_page,error_out=False)
    
    return render_template('home.html',deals=deals)


