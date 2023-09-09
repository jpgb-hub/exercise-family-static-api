import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(jackson_family.get_all_members()), 200

@app.route('/member', methods=['POST'])
def add_member():
    try:
        member_data = request.get_json()
        if not member_data:
            raise APIException("Información del miembro no proporcionada", status_code=400)
        
        new_member = jackson_family.add_member(member_data)
        return jsonify(new_member), 200
    except APIException as api_err:
        return jsonify({"msg": str(api_err)}), api_err.status_code
    except Exception as err:
        return jsonify({"msg": str(err)}), 500

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    try:
        member = jackson_family.get_member(id)
        if not member:
            raise APIException("Miembro no encontrado", status_code=404)
        return jsonify(member), 200
    except APIException as api_err:
        return jsonify({"msg": str(api_err)}), api_err.status_code
    except Exception as err:
        return jsonify({"msg": str(err)}), 500

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    if member:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"done": False, "error": "Member not found"}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = request.get_json()
        if not member_data:
            raise APIException("Información del miembro no proporcionada", status_code=400)
        
        updated_member = jackson_family.update_member(id, member_data)
        if not updated_member:
            raise APIException("Miembro no encontrado", status_code=404)
        
        return jsonify(updated_member), 200
    except APIException as api_err:
        return jsonify({"msg": str(api_err)}), api_err.status_code
    except Exception as err:
        return jsonify({"msg": str(err)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)