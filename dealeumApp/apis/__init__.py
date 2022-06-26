from flask_restx import Api
from dealeumApp.apis.deals import api as deals_api

api = Api(version="0.1",title="DealeumApi",description="A Deal Serving Api")



api.add_namespace(deals_api)