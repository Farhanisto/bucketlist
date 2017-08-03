from flask_restplus import fields
from api.restplus import api

user = api.model('user', {
    'id': fields.Integer(readOnly=True, description='Unique identifier of a person'),
    'username': fields.String(required=True, description='Your email address'),
    'password': fields.String(required=True, description='Your secret password'),


})

bucketlist = api.model('bucketlist', {
    'id': fields.Integer(readOnly=True, description="unique identifier for bucket Item"),
    'name': fields.String(required=False, description="name of this Item"),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
})

bucket = api.model('bucket', {
    'id': fields.Integer(readOnly=True, description="unique identifier for bucket"),
    'name': fields.String(required=True, description="name of this bucket"),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True, description="Name of owner")

})
bucket_n_items = api.model('bucket_n_items', {
    'id': fields.Integer(readOnly=True, description="unique identifier for bucket"),
    'name': fields.String(required=True, description="name of this bucket"),
    'items': fields.List(fields.Nested(bucketlist),description="Items in this bucket"),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True, description="Name of owner")

})
bucket_name = api.model('bucket_name', {
    'name': fields.String(required=True, discription="name of this bucket")
})

bucket_item = api.model('edit', {
    'name': fields.String(required=True, description='name of bucketlist or bucket item'),
    'done': fields.Boolean(required=False, description='status of the bucketlist item', default=False),
})