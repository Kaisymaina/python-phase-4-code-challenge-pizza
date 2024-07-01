from app import app
from models import db, Eatery, Pie, EateryPizza

with app.app_context():
    EateryPizza.query.delete()
    Pie.query.delete()
    Eatery.query.delete()

    # Create and add eateries
    eateries = [
        Eatery(name="Karen's Pizza Shack", location='address1'),
        Eatery(name="Sanjay's Pizza", location='address2'),
        Eatery(name="Kiki's Pizza", location='address3')
    ]
    db.session.add_all(eateries)
    db.session.commit()

    # Create and add pies
    pies = [
        Pie(name="Emma", toppings="Dough, Tomato Sauce, Cheese"),
        Pie(name="Geri", toppings="Dough, Tomato Sauce, Cheese, Pepperoni"),
        Pie(name="Melanie", toppings="Dough, Sauce, Ricotta, Red peppers, Mustard")
    ]
    db.session.add_all(pies)
    db.session.commit()

    # Create and add eatery-pie relationships
    eatery_pizzas = [
        EateryPizza(eatery=eateries[0], pizza=pies[0], cost=1),
        EateryPizza(eatery=eateries[1], pizza=pies[1], cost=4),
        EateryPizza(eatery=eateries[2], pizza=pies[2], cost=5)
    ]
    db.session.add_all(eatery_pizzas)
    db.session.commit()

    print("Seeding completed!")
