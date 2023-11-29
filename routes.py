from flask import render_template, request, jsonify
from db import get_page_data
from parse_json import parse_json
import json

def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of items per page

    page_data_dicts, total_pages = get_page_data(page, per_page)

    page_data_dicts = parse_json(page_data_dicts)

    return render_template('index.html', page_data=page_data_dicts, page=page, total_pages=total_pages)

def data():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of items per page

    page_data_dicts, total_pages = get_page_data(page, per_page)

    # Return the sliced data as a JSON response
    return jsonify(page_data_dicts)


def init_app(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/data', 'data', data)
