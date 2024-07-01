from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api
from models import db, Eatery, Pie, EateryPizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def home():
    return "<h1>Code Challenge</h1>"

@app.route('/eateries', methods=['GET'])
def list_eateries():
    eateries = Eatery.query.all()
    return jsonify([eatery.to_dict() for eatery in eateries])

@app.route('/eateries/<int:id>', methods=['GET'])
def get_eatery(id):
    eatery = Eatery.query.get(id)
    if not eatery:
        return jsonify({"error": "Eatery not found"}), 404
    return jsonify(eatery.to_dict(include=['eatery_pizzas.pizza']))

@app.route('/eateries/<int:id>', methods=['DELETE'])
def remove_eatery(id):
    eatery = Eatery.query.get(id)
    if not eatery:
        return jsonify({"error": "Eatery not found"}), 404
    db.session.delete(eatery)
    db.session.commit()
    return '', 204

@app.route('/pies', methods=['GET'])
def list_pies():
    pies = Pie.query.all()
    return jsonify([pie.to_dict() for pie in pies])

@app.route('/eatery_pizzas', methods=['POST'])
def add_eatery_pizza():
    data = request.get_json()
    try:
        eatery_pizza = EateryPizza(
            cost=data['cost'],
            eatery_id=data['eatery_id'],
            pizza_id=data['pizza_id']
        )
        db.session.add(eatery_pizza)
        db.session.commit()
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400
    return jsonify(eatery_pizza.to_dict(include=['pizza', 'eatery'])), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
