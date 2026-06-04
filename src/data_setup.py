import json
import os
import random
from datetime import datetime
from typing import Dict, List

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_json_file(file_name: str) -> List[Dict]:
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    return []


def load_sample_products() -> List[Dict]:
    products = load_json_file("sample_products.json")
    if products:
        return products

    return [
        {"item_id": "P001", "title": "Wireless Earbuds", "category": "Electronics", "brand": "SoundWave", "price": 59.99, "tags": "audio, bluetooth, earbuds", "rating": 4.3},
        {"item_id": "P002", "title": "Smart Fitness Watch", "category": "Electronics", "brand": "TimeFit", "price": 129.99, "tags": "fitness, wearable, health", "rating": 4.5},
        {"item_id": "P003", "title": "Running Shoes", "category": "Footwear", "brand": "SpeedRun", "price": 79.99, "tags": "running, sports, comfort", "rating": 4.2},
        {"item_id": "P004", "title": "Casual Sneakers", "category": "Footwear", "brand": "UrbanStep", "price": 64.99, "tags": "casual, everyday, fashion", "rating": 4.1},
        {"item_id": "P005", "title": "Denim Jacket", "category": "Apparel", "brand": "TrendLab", "price": 89.99, "tags": "jacket, denim, style", "rating": 4.4},
        {"item_id": "P006", "title": "Yoga Mat", "category": "Fitness", "brand": "FlexFlow", "price": 29.99, "tags": "yoga, exercise, wellness", "rating": 4.6},
        {"item_id": "P007", "title": "Backpack", "category": "Accessories", "brand": "PackMate", "price": 49.99, "tags": "travel, bag, school", "rating": 4.3},
        {"item_id": "P008", "title": "Noise Cancelling Headphones", "category": "Electronics", "brand": "QuietTone", "price": 149.99, "tags": "music, noise cancelling, audio", "rating": 4.7},
        {"item_id": "P009", "title": "Formal Shirt", "category": "Apparel", "brand": "SharpSuit", "price": 39.99, "tags": "shirt, formal, office", "rating": 4.0},
        {"item_id": "P010", "title": "Bluetooth Speaker", "category": "Electronics", "brand": "BeatBox", "price": 45.99, "tags": "speaker, portable, music", "rating": 4.2},
        {"item_id": "P011", "title": "Trail Running Socks", "category": "Footwear", "brand": "TrailPro", "price": 12.99, "tags": "socks, trail, comfort", "rating": 4.0},
        {"item_id": "P012", "title": "Laptop Sleeve", "category": "Accessories", "brand": "TechGuard", "price": 24.99, "tags": "laptop, protection, sleeve", "rating": 4.1},
        {"item_id": "P013", "title": "Sunglasses", "category": "Accessories", "brand": "SunWave", "price": 34.99, "tags": "sunglasses, uv protection, fashion", "rating": 4.5},
        {"item_id": "P014", "title": "Smartphone Stand", "category": "Electronics", "brand": "HoldIt", "price": 19.99, "tags": "stand, desk, mobile", "rating": 4.3},
        {"item_id": "P015", "title": "Gym Duffel Bag", "category": "Fitness", "brand": "FitCarry", "price": 59.99, "tags": "gym, bag, workout", "rating": 4.4},
    ]


def load_sample_users() -> List[Dict]:
    users = load_json_file("sample_users.json")
    if users:
        return users

    return [
        {"user_id": "U001", "created": "2026-01-10"},
        {"user_id": "U002", "created": "2026-02-05"},
        {"user_id": "U003", "created": "2026-03-21"},
        {"user_id": "U004", "created": "2026-04-14"},
        {"user_id": "U005", "created": "2026-05-02"},
    ]


def create_sample_interactions(products: List[Dict], users: List[Dict]) -> List[Dict]:
    sample_searches = [
        "wireless earbuds",
        "fitness watch",
        "running shoes",
        "yoga mat",
        "denim jacket",
        "backpack for school",
        "noise cancelling headphones",
        "smartphone stand",
        "sunglasses",
        "gym duffel bag",
    ]
    sample_events = []
    random.seed(42)
    for user in users:
        user_id = user["user_id"]
        search_term = random.choice(sample_searches)
        sample_events.append(
            {
                "user_id": user_id,
                "event": "search",
                "search_text": search_term,
                "timestamp": datetime(2026, 5, random.randint(1, 28), random.randint(8, 22)).isoformat(),
            }
        )
        item_ids = [product["item_id"] for product in products]
        viewed = random.sample(item_ids, 3)
        for item_id in viewed:
            sample_events.append(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "event": "view",
                    "timestamp": datetime(2026, 5, random.randint(1, 28), random.randint(8, 22)).isoformat(),
                }
            )
        cart_count = random.randint(1, 3)
        carts = random.sample(item_ids, cart_count)
        for item_id in carts:
            sample_events.append(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "event": "add_cart",
                    "timestamp": datetime(2026, 5, random.randint(1, 28), random.randint(8, 22)).isoformat(),
                }
            )
        purchased = random.sample(item_ids, 2)
        for item_id in purchased:
            sample_events.append(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "event": "purchase",
                    "timestamp": datetime(2026, 5, random.randint(1, 28), random.randint(8, 22)).isoformat(),
                }
            )
    sample_events.sort(key=lambda item: item["timestamp"])
    return sample_events


def save_sample_files():
    products = load_sample_products()
    users = load_sample_users()
    interactions = create_sample_interactions(products, users)
    with open(os.path.join(DATA_DIR, "sample_products.json"), "w", encoding="utf-8") as handle:
        json.dump(products, handle, indent=2)
    with open(os.path.join(DATA_DIR, "sample_users.json"), "w", encoding="utf-8") as handle:
        json.dump(users, handle, indent=2)
    with open(os.path.join(DATA_DIR, "sample_interactions.json"), "w", encoding="utf-8") as handle:
        json.dump(interactions, handle, indent=2)


if __name__ == "__main__":
    save_sample_files()
    print("Sample product, user, and interaction files saved to data/")
