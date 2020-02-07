from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Shoe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), unique=False)
    history = db.Column(db.String(144), unique=False)
    vendor = db.Column(db.String(144), unique=False)

    def __init__(self, country, history, vendor):
        self.country = country
        self.history = history
        self.vendor = vendor


class ShoeSchema(ma.Schema):
    class Meta:
        fields = ('country', 'history', 'vendor', "id")
        


shoe_schema = ShoeSchema()
shoes_schema = ShoeSchema(many=True)

@app.route('/shoe', methods=["POST"])
def add_shoe():
    country = request.json['country']
    history = request.json['history']
    vendor = request.json['vendor']

    new_shoe = Shoe(country, history, vendor)

    db.session.add(new_shoe)
    db.session.commit()

    shoe = Shoe.query.get(new_shoe.id)

    return shoe_schema.jsonify(shoe)

@app.route('/shoes', methods=['GET'])
def get_shoes():
    all_shoes = Shoe.query.all()
    result = shoes_schema.dump(all_shoes)
    return jsonify(result)


@app.route("/shoe/<id>", methods=["GET"])
def get_shoe(id):
    shoe = Shoe.query.get(id)
    return shoe_schema.jsonify(shoe)


@app.route("/shoe/<id>", methods=["PUT"])
def shoe_update(id):
    shoe = Shoe.query.get(id)
    country = request.json['country']
    history = request.json['history']
    vendor = request.json['vendor']
    
    shoe.country = country
    shoe.history = history
    shoe.vendor = vendor
    
    db.session.commit()
    return shoe_schema.jsonify(shoe)

@app.route("/shoe/<id>", methods=["DELETE"])
def shoe_delete(id):
    shoe = Shoe.query.get(id)
    db.session.delete(shoe)
    db.session.commit()
    
    return "Dem shoes ugly as hell!!! Get it gone! (it was successfully deleted)"


if __name__ == '__main__':
    app.run(debug=True)    