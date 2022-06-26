from flask import Flask
from flask.helpers import url_for
from flask_admin.contrib import sqla
from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail
from sassutils.wsgi import SassMiddleware
from flask_migrate import Migrate


db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
cors = CORS(supports_credentials=True)
bcrypt = Bcrypt()
migrate = Migrate()



from .routes.auth import auth as auth_blueprint
from .routes.main import main as main_blueprint
from .routes.deals import dealsbp as deal_blueprint




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '51bb382be184885eb5f5b922b674c764'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:6778@localhost:3306/dealeum'
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True
    app.config['UPLOADS FOLDER'] = app.root_path + "/uploads"
    app.config['TEMP_FOLDER'] = app.root_path + "/tempfiles"
    
    app.config['MAIL_SERVER'] = "smtp.gmail.com"
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = "blablabla@gmail.com"
    app.config['MAIL_PASSWORD'] = "123123123123123"
    app.config['MAIL_USE_TLS'] = True

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'dealeumApp':('static/sass','static/css','/static/css')
    })

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(deal_blueprint, url_prefix='/deals')
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .models import deal, user, category
    migrate.init_app(app,db)
    
    from .apis import api
    api.init_app(app)
    
    return app

