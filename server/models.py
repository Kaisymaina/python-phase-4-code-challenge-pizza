from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Eatery(db.Model, SerializerMixin):
    __tablename__ = "eateries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    eatery_pizzas = relationship("EateryPizza", back_populates="eatery")
    pizzas = association_proxy("eatery_pizzas", "pizza")

    serialize_rules = ('-eatery_pizzas.eatery',)

    def __repr__(self):
        return f"<Eatery {self.name}>"

class Pie(db.Model, SerializerMixin):
    __tablename__ = "pies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    toppings = db.Column(db.String, nullable=False)

    eatery_pizzas = relationship("EateryPizza", back_populates="pizza")
    eateries = association_proxy("eatery_pizzas", "eatery")

    serialize_rules = ('-eatery_pizzas.pizza',)

    def __repr__(self):
        return f"<Pie {self.name}, {self.toppings}>"

class EateryPizza(db.Model, SerializerMixin):
    __tablename__ = "eatery_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer, nullable=False)

    eatery_id = db.Column(db.Integer, ForeignKey('eateries.id'), nullable=False)
    pizza_id = db.Column(db.Integer, ForeignKey('pies.id'), nullable=False)

    eatery = relationship("Eatery", back_populates="eatery_pizzas")
    pizza = relationship("Pie", back_populates="eatery_pizzas")

    serialize_rules = ('-eatery.eatery_pizzas', '-pizza.eatery_pizzas')

    @validates('cost')
    def validate_cost(self, key, cost):
        if cost < 1 or cost > 30:
            raise ValueError("Cost must be between 1 and 30")
        return cost

    def __repr__(self):
        return f"<EateryPizza ${self.cost}>"

