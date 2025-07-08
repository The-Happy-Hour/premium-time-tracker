from flask import Blueprint, request, jsonify
from src.models.duration_user import DurationUserModel

duration_user_bp = Blueprint('duration_user', __name__)
duration_user_model = DurationUserModel()

@duration_user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        users = duration_user_model.get_all_users()
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@duration_user_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        user_id = data.get('user_id')
        duration = data.get('duration')
        end_time = data.get('end_time')
        
        if not all([name, user_id, duration, end_time]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        user_id_str = duration_user_model.create_user(name, user_id, duration, end_time)
        return jsonify({'success': True, 'user_id': user_id_str})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@duration_user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        duration = data.get('duration')
        end_time = data.get('end_time')
        
        if not all([duration, end_time]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        success = duration_user_model.update_user(user_id, duration, end_time)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@duration_user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        success = duration_user_model.delete_user(user_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

