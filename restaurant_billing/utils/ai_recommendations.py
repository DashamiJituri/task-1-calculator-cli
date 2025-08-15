# ai_recommendations.py
import random

# Simulated menu data
menu_items = [
    "Margherita Pizza", "Farmhouse Pizza", "Veg Burger",
    "Chicken Burger", "Pasta Alfredo", "Pasta Arrabiata",
    "Coke", "Pepsi", "Chocolate Cake", "Vanilla Ice Cream"
]

# Sample recommendations based on previous orders
recommendation_map = {
    "Margherita Pizza": ["Farmhouse Pizza", "Pasta Alfredo"],
    "Veg Burger": ["Coke", "Chocolate Cake"],
    "Chicken Burger": ["Pepsi", "Vanilla Ice Cream"],
    "Pasta Alfredo": ["Garlic Bread", "Coke"],
    "Pasta Arrabiata": ["Garlic Bread", "Pepsi"]
}

def get_recommendations(customer_orders):
    """
    Takes a list of previous orders and returns AI-based recommendations.
    """
    recs = []
    for item in customer_orders:
        if item in recommendation_map:
            recs.extend(recommendation_map[item])
    if not recs:  # If no matching past items
        recs = random.sample(menu_items, 2)
    return list(set(recs))  # Remove duplicates
