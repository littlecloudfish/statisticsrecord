"""Routes for user authentication."""
import json
from flask import jsonify

from flask_login import login_required
from .model_video import Video
from flask import Blueprint
from .dashboard import dashboard_bp
from ..index.model_ip import IP
from ..auth.model_account import Account
from ..dashboard.model_operation import Operation

# Blueprint Configuration
_dashboard_bp = Blueprint(
    "_dashboard_bp", __name__, template_folder="templates", static_folder="static")


@_dashboard_bp.route('/api_v1/records', methods=['GET'])
def records():
    records = IP.query.all()
    return jsonify([i.serialize for i in records])


@_dashboard_bp.route('/api_v1/accounts', methods=['GET'])
def accounts():
    records = Account.query.all()
    return jsonify([i.serialize for i in records])


@_dashboard_bp.route('/api_v1/operates', methods=['GET'])
def operates():
    records = Operation.query.all()
    return jsonify([i.serialize for i in records])

@_dashboard_bp.route('/api_v1/login', methods=['GET'])
def login():
    return jsonify({'name':'nemo','password': '123456'})
