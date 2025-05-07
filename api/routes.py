from flask import Blueprint, request, jsonify
from electre.core import run_electre

api = Blueprint('api', __name__)

@api.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API працює!'})

@api.route('/api/run-electre', methods=['POST'])
def run_electre_route():
    data = request.json  # Отримаємо JSON із frontend
    result = run_electre(data)
    return jsonify(result)
