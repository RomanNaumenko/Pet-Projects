from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    desc = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.desc}"


with app.app_context():
    db.create_all()


@app.route("/", methods=['GET'])
def index():
    return "Hello!"


@app.get("/drinks")
def get_all_drinks():
    drinks = Drink.query.all()
    output = {"drinks": [{'name': drink.name, 'description': drink.desc} for drink in drinks]}
    return output


@app.get("/drinks/<id>")
def get_drink_by_id(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.desc}


@app.post("/drinks")
def add_drink():
    drink = Drink(name=request.json["name"], desc=request.json["description"])
    db.session.add(drink)
    db.session.commit()
    return {"id": drink.id}


@app.delete("/drinks/<id>")
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message": "delete completed"}


if __name__ == "__main__":
    app.run()
