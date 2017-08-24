import logging

from flask import request, jsonify, make_response,abort
from flask_restplus import Resource
from api.bucketlist.serializers import user,bucket,bucket_name,bucket_n_items,bucketlist,bucket_item
from api.restplus import api
from models.models import User, Bucket, BucketList
from api.bucketlist.parsers import pagination_arguments


log = logging.getLogger(__name__)
ns = api.namespace("bucket", description="Bucket operations")

@ns.route('/')
@ns.response(201, "succesfully created")
@ns.header("Authorization", "JWT Token", required=True)
class Bucket_endpoint(Resource):
    """Class that deals with the creation and getting of buckets"""
    @api.expect(bucket_name)
    @api.marshal_with(bucket)
    def post(self):
        """Create buckets"""
        access_token = request.headers.get("Authorization")
        post_data = request.json
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                name = post_data.get('name')
                bucket = Bucket(name=name, created_by=user_id)
                bucket.save()
                return bucket, 201
            abort(401, "please login")
        else:
            abort(403, "please login")

    @api.expect(pagination_arguments, validate=True)
    @api.marshal_list_with(bucket_n_items)
    def get(self):
        access_token = request.headers.get("Authorization")

        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                args = pagination_arguments.parse_args(request)
                print(args)
                page = args.get('page', 1)
                per_page = args.get('per_page', 10)

                bucket_list = Bucket.query.filter_by(created_by=user_id)
                if not bucket_list:
                    abort(404, "Not Found")
                else:
                    items_filled =[]
                    bucketlists = bucket_list.paginate(page, per_page, error_out=False)
                    print(bucketlists.items)
                    for buck in bucketlists.items:
                        items_present = buck.bucketitems
                        res = {
                            'id': buck.id,
                            'name': buck.name,
                            'items': items_present,
                            'date_created': buck.date_created,
                            'date_modified': buck.date_modified,
                            'created_by': buck.created_by,
                        }
                        items_filled.append(res)
                    return items_filled, 200
        else:
            return abort(401, "unauthorized")


@ns.route('/<int:id>')
@ns.response(201, "succesfully created")
@ns.header("Authorization", "JWT Token", required=True)
class Bucket_changes(Resource):
    def delete(self, id):
        """Deletion of a bucket"""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_to_del =Bucket.query.filter_by(id=id, created_by= user_id).first()
                if not bucket_to_del:
                    abort(404, "No buckets found")
                bucket_to_del.delete()
                return "bucket id {} succesfully deleted".format(bucket_to_del.id), 200
            else:
                abort(401, "please login")
    @api.expect(bucket_name)
    @api.marshal_with(bucket)
    def put(self, id):
        """Update a bucket"""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_to_del = Bucket.query.filter_by(id=id, created_by=user_id).first()
                if not bucket_to_del:
                    abort(404, "No buckets found")
                new_name = request.json.get("name")
                print(new_name)
                bucket_to_del.name = new_name
                bucket_to_del.save()
                return bucket_to_del, 200

            else:
                abort(401, "please login")

    @api.marshal_with(bucket)
    def get(self, id):
        "Get a particulat bucket"
        access_token = request.headers.get("Authorization")
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_to_get = Bucket.query.filter_by(id=id, created_by=user_id).first()
                if not bucket_to_get:
                    abort(404, "Not found")
                return bucket_to_get, 200
            else:
                abort(401, "unauthorized")


@ns.route('/<int:id>/items')
@ns.response(201, "successfully created")
@ns.header("Authorization", "JWT Token", required=True)
class bucket_items(Resource):
    @api.expect(bucket_name)
    @api.marshal_with(bucketlist)
    def post(self, id):
        """Add items """
        access_token = request.headers.get("Authorization")
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                name = request.json.get("name")
                bucketitem=BucketList(name=name, bucket_id=id)
                bucketitem.save()
                return bucketitem, 201

        abort(401, "Unauthorized")


@ns.route('/<int:id>/items/<int:item_id>')
@ns.response(201, "succefully created")
@ns.header("Authorization", "JWT Token", required=True)
class bucket_items(Resource):
    def delete(self, id, item_id):
        """delete an item in a bucket"""
        access_token = request.headers.get("Authorization")
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_from = Bucket.query.filter_by(id=id).first()
                if bucket_from.created_by == user_id:
                    item_to_del = BucketList.query.filter_by(id=item_id).first()
                    if not item_to_del:
                        abort(404, "item not found")
                    else:
                        item_to_del.delete()
                        return {"message": "successfully deleted item"

                                }, 200
            else:
                abort(401, "Unauthorized")
            abort(401, "Unauthorized")

    @api.expect(bucket_item)
    @api.marshal_with(bucketlist)
    def put(self, id, item_id):
        """update an item in a bucket"""
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_from = Bucket.query.filter_by(id=id).first()
                if not bucket_from:
                    abort(404, "No such buckets.")
                item_to_update = BucketList.query.filter_by(id=item_id).first()
                if not item_to_update:
                    abort(404, "no such item in this bucket")
                name = request.json.get('name')
                done = request.json.get('done')
                item_to_update.name = name
                item_to_update.done = done
                item_to_update.save()
                return item_to_update, 200
            else:
                abort(401, "please login")
        else:
            abort(401, "unauthorized")

    @api.marshal_with(bucketlist)
    def get(self, id, item_id):
        access_token = request.headers.get('Authorization')
        if access_token:
            user_id = User.decode_auth_token(access_token)
            if not isinstance(user_id, str):
                bucket_from = Bucket.query.filter_by(id=id).first()
                result = []
                if not bucket_from:
                    abort(404, "No such buckets")
                item_to_update = BucketList.query.filter_by(id=item_id).first()
                res = {
                    'id': bucket_from.id,
                    'name': bucket_from.name,
                    'items': item_to_update,
                    'date_created': bucket_from.date_created,
                    'date_modified': bucket_from.date_modified,
                    'created_by': bucket_from.created_by,
                }
                result.append(res)
                return result,200
            else:
                abort(401,"Unauthorized")
        else:
            abort(401, "please login first")
