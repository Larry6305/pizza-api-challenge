from flask import Blueprint, jsonify, request
from ..models.restaurant_pizza import RestaurantPizza
from ..models.pizza import Pizza
from ..models.restaurant import Restaurant
from ..config import db

restaurant_pizza_bp = Blueprint("restaurant_pizzas", __name__, url_prefix="/restaurant_pizzas")

@restaurant_pizza_bp.route("", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    if not new_rp.validate():
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400

    db.session.add(new_rp)
    db.session.commit()

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    return jsonify({
        "id": new_rp.id,
        "price": new_rp.price,
        "pizza_id": pizza.id,
        "restaurant_id": restaurant.id,
        "pizza": {"id": pizza.id, "name": pizza.name, "ingredients": pizza.ingredients},
        "restaurant": {"id": restaurant.id, "name": restaurant.name, "address": restaurant.address}
    }), 201
