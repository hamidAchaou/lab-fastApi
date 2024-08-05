from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from passlib.context import CryptContext

import logging
from datetime import timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.DEBUG)

from api.models import User, Suivi, Ville, TypeBien, Statut
from api.schemas import UserCreateSchema, UserLoginSchema, SuiviSchema, VilleSchema, TypeBienSchema, StatutSchema

@app.route('/token', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not pwd_context.verify(data['password'], user.password_hash):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Username or Email already registered"}), 400

    hashed_password = pwd_context.hash(data['password'])
    user = User(username=data['username'], email=data['email'], full_name=data['full_name'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User created successfully")

@app.route('/suivi/', methods=['GET'])
def read_suivis():
    suivis = Suivi.query.all()
    return jsonify([SuiviSchema().dump(suivi) for suivi in suivis])

@app.route('/suivi/<int:suivi_id>', methods=['GET'])
def read_suivi(suivi_id):
    suivi = Suivi.query.get_or_404(suivi_id)
    return jsonify(SuiviSchema().dump(suivi))

@app.route('/suivi/create', methods=['POST'])
def create_suivi():
    data = request.json
    suivi = Suivi(**data)
    db.session.add(suivi)
    db.session.commit()
    return jsonify(SuiviSchema().dump(suivi)), 201

@app.route('/suivi/update/<int:suivi_id>', methods=['PUT'])
def update_suivi(suivi_id):
    data = request.json
    suivi = Suivi.query.get_or_404(suivi_id)
    for key, value in data.items():
        setattr(suivi, key, value)
    db.session.commit()
    return jsonify(SuiviSchema().dump(suivi))

@app.route('/suivi/delete/<int:suivi_id>', methods=['DELETE'])
def delete_suivi(suivi_id):
    suivi = Suivi.query.get_or_404(suivi_id)
    db.session.delete(suivi)
    db.session.commit()
    return jsonify(message="Suivi deleted successfully")

@app.route('/ville/', methods=['GET'])
def read_villes():
    villes = Ville.query.all()
    return jsonify([VilleSchema().dump(ville) for ville in villes])

@app.route('/ville/<int:ville_id>', methods=['GET'])
def read_ville(ville_id):
    ville = Ville.query.get_or_404(ville_id)
    return jsonify(VilleSchema().dump(ville))

@app.route('/ville/create', methods=['POST'])
def create_ville():
    data = request.json
    ville = Ville(**data)
    db.session.add(ville)
    db.session.commit()
    return jsonify(VilleSchema().dump(ville)), 201

@app.route('/ville/update/<int:ville_id>', methods=['PUT'])
def update_ville(ville_id):
    data = request.json
    ville = Ville.query.get_or_404(ville_id)
    for key, value in data.items():
        setattr(ville, key, value)
    db.session.commit()
    return jsonify(VilleSchema().dump(ville))

@app.route('/ville/delete/<int:ville_id>', methods=['DELETE'])
def delete_ville(ville_id):
    ville = Ville.query.get_or_404(ville_id)
    db.session.delete(ville)
    db.session.commit()
    return jsonify(message="Ville deleted successfully")

@app.route('/typebien/', methods=['GET'])
def read_typebiens():
    typebiens = TypeBien.query.all()
    return jsonify([TypeBienSchema().dump(typebien) for typebien in typebiens])

@app.route('/typebien/<int:typebien_id>', methods=['GET'])
def read_typebien(typebien_id):
    typebien = TypeBien.query.get_or_404(typebien_id)
    return jsonify(TypeBienSchema().dump(typebien))

@app.route('/typebien/create', methods=['POST'])
def create_typebien():
    data = request.json
    typebien = TypeBien(**data)
    db.session.add(typebien)
    db.session.commit()
    return jsonify(TypeBienSchema().dump(typebien)), 201

@app.route('/typebien/update/<int:typebien_id>', methods=['PUT'])
def update_typebien(typebien_id):
    data = request.json
    typebien = TypeBien.query.get_or_404(typebien_id)
    for key, value in data.items():
        setattr(typebien, key, value)
    db.session.commit()
    return jsonify(TypeBienSchema().dump(typebien))

@app.route('/typebien/delete/<int:typebien_id>', methods=['DELETE'])
def delete_typebien(typebien_id):
    typebien = TypeBien.query.get_or_404(typebien_id)
    db.session.delete(typebien)
    db.session.commit()
    return jsonify(message="TypeBien deleted successfully")

@app.route('/statut/', methods=['GET'])
def read_statuts():
    statuts = Statut.query.all()
    return jsonify([StatutSchema().dump(statut) for statut in statuts])

@app.route('/statut/<int:statut_id>', methods=['GET'])
def read_statut(statut_id):
    statut = Statut.query.get_or_404(statut_id)
    return jsonify(StatutSchema().dump(statut))

@app.route('/statut/create', methods=['POST'])
def create_statut():
    data = request.json
    statut = Statut(**data)
    db.session.add(statut)
    db.session.commit()
    return jsonify(StatutSchema().dump(statut)), 201

@app.route('/statut/update/<int:statut_id>', methods=['PUT'])
def update_statut(statut_id):
    data = request.json
    statut = Statut.query.get_or_404(statut_id)
    for key, value in data.items():
        setattr(statut, key, value)
    db.session.commit()
    return jsonify(StatutSchema().dump(statut))

@app.route('/statut/delete/<int:statut_id>', methods=['DELETE'])
def delete_statut(statut_id):
    statut = Statut.query.get_or_404(statut_id)
    db.session.delete(statut)
    db.session.commit()
    return jsonify(message="Statut deleted successfully")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
