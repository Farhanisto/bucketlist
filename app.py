import logging.config
from api.restplus import api
from api.bucketlist.endpoints.user import ns as user_registration
from api.bucketlist.endpoints.bucket import ns as bucket_creation
from flask import Blueprint
from models import app,db

log = logging.getLogger(__name__)
blueprint = Blueprint('api', __name__)
api.init_app(blueprint)
api.add_namespace(user_registration)
api.add_namespace(bucket_creation)
# add Rules for API Endpoints
app.register_blueprint(blueprint)


def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=app.config['FLASK_DEBUG'])

if __name__ == "__main__":
    main()


