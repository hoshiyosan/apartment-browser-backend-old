"""
Fetch article at given url and return parsed data.
"""
from flask import Blueprint, request, jsonify
from ..apartment.parser import PageParser

bp = Blueprint('parse', __name__)

from werkzeug.exceptions import HTTPException
class RequestParser:
    def __init__(self, schema):
        self.schema = schema

    def parse(self, data, **defaults):
        if data is None:
            raise HTTPException
        
        parsed = {}
        for key, required in data.items():
            if required:
                parsed[key] = data[key]
            else:
                parsed[key] = data.get(key, defaults.get(key))
        return parsed


parse_article_parser = RequestParser({'url': True, 'body': True})

@bp.route('/parse', methods=['POST'])
def parse_article_endpoint():
    data = parse_article_parser.parse(request.json)
    
    return PageParser(data['url'], data['body']).parse()
