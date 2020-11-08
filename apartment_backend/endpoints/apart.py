from flask import Blueprint, request
from ..addons import db

import json
from flask import jsonify as flask_jsonify

from bson import ObjectId
from datetime import datetime


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return int(o.strftime('%s')) * 1000
        return json.JSONEncoder.default(self, o)


def jsonify(data):
    return flask_jsonify(JSONEncoder().encode(data))


bp = Blueprint('bookmarks', __name__)


@bp.route('/bookmarks', methods=['GET'])
def list_bookmarks():
    return jsonify([apart for apart in db.bookmarks.find({})])


@bp.route('/bookmarks', methods=['POST'])
def create_bookmark():
    result = db.bookmarks.insert_one({
        'title': request.json['title'],
        'place': request.json['place'],
        'url': request.json['url'],
        'saved_on': datetime.now()
    })
    return jsonify(db.bookmarks.find_one({'_id': result.inserted_id}))
