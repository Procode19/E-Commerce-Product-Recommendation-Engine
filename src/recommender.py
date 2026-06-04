import heapq
import random
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set


class Product:
    def __init__(self, item_id: str, title: str, category: str, brand: str, price: float, tags: str, rating: float):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.brand = brand
        self.price = price
        self.tags = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]
        self.rating = float(rating)

    def __repr__(self) -> str:
        return f"Product({self.item_id}, {self.title}, category={self.category}, price={self.price})"


class User:
    def __init__(self, user_id: str, created: str = "2026-01-01"):
        self.user_id = user_id
        self.created = datetime.fromisoformat(created)
        self.search_history: List[str] = []
        self.cart_items: List[str] = []
        self.purchased_items: List[str] = []
        self.viewed_items: List[str] = []

    def __repr__(self) -> str:
        return f"User({self.user_id}, searches={len(self.search_history)}, purchased={len(self.purchased_items)})"


class RecommendationEngine:
    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.users: Dict[str, User] = {}
        self.products_by_category: Dict[str, List[str]] = defaultdict(list)
        self.popularity: Counter = Counter()
        self.cooccurrence: Dict[str, Counter] = defaultdict(Counter)
        self.item_similarity: Dict[str, Dict[str, float]] = {}
        self.user_categories: Dict[str, Counter] = defaultdict(Counter)
        self.user_search_terms: Dict[str, Counter] = defaultdict(Counter)
        self.random_seed = random.Random(42)

    def load_products(self, product_rows: List[Dict]):
        for row in product_rows:
            item = Product(
                item_id=row["item_id"],
                title=row["title"],
                category=row["category"],
                brand=row["brand"],
                price=float(row["price"]),
                tags=row["tags"],
                rating=float(row.get("rating", 4.0)),
            )
            self.products[item.item_id] = item
            self.products_by_category[item.category].append(item.item_id)
        self._normalize_category_items()

    def load_users(self, user_rows: List[Dict]):
        for row in user_rows:
            self.users[row["user_id"]] = User(user_id=row["user_id"], created=row.get("created", "2026-01-01"))

    def load_interactions(self, interactions: List[Dict]):
        interactions.sort(key=lambda item: item.get("timestamp", ""))
        for event in interactions:
            user_id = event["user_id"]
            item_id = event.get("item_id")
            event_type = event["event"]
            search_text = event.get("search_text", "")

            if user_id not in self.users:
                self.users[user_id] = User(user_id=user_id)

            user = self.users[user_id]

            if event_type == "search":
                user.search_history.append(search_text)
                self.user_search_terms[user_id].update(search_text.lower().split())
                continue

            if item_id not in self.products:
                continue

            if event_type == "view":
                user.viewed_items.append(item_id)
                self.popularity[item_id] += 1
            elif event_type == "add_cart":
                user.cart_items.append(item_id)
                self.popularity[item_id] += 2
            elif event_type == "purchase":
                user.purchased_items.append(item_id)
                self.popularity[item_id] += 5

        self._build_user_category_profiles()
        self._build_cooccurrence()
        self._build_item_similarity()

    def _normalize_category_items(self):
        for category, item_ids in self.products_by_category.items():
            self.products_by_category[category] = sorted(
                item_ids,
                key=lambda i: (-self.products[i].rating, self.products[i].price, i),
            )

    def _build_user_category_profiles(self):
        for user_id, user in self.users.items():
            for item_id in user.purchased_items + user.cart_items + user.viewed_items:
                if item_id in self.products:
                    self.user_categories[user_id].update([self.products[item_id].category])

    def _build_cooccurrence(self):
        for user in self.users.values():
            visited = []
            visited.extend(user.viewed_items)
            visited.extend(user.cart_items)
            visited.extend(user.purchased_items)
            unique_items = list(dict.fromkeys(visited))
            for i, item_id in enumerate(unique_items):
                for other_id in unique_items[i + 1 :]:
                    self.cooccurrence[item_id][other_id] += 1
                    self.cooccurrence[other_id][item_id] += 1

    def _build_item_similarity(self):
        for item_id, product in self.products.items():
            self.item_similarity[item_id] = {}
            for candidate_id, candidate in self.products.items():
                if item_id == candidate_id:
                    continue
                co_score = float(self.cooccurrence[item_id].get(candidate_id, 0))
                tag_score = self._jaccard_similarity(set(product.tags), set(candidate.tags))
                category_bonus = 1.0 if product.category == candidate.category else 0.0
                self.item_similarity[item_id][candidate_id] = co_score * 2.0 + tag_score * 4.0 + category_bonus

    @staticmethod
    def _jaccard_similarity(left: Set[str], right: Set[str]) -> float:
        if not left or not right:
            return 0.0
        intersection = len(left & right)
        union = len(left | right)
        return intersection / union if union else 0.0

    def get_user_profile(self, user_id: str) -> List[str]:
        if user_id not in self.users:
            return []
        categories = self.user_categories[user_id].most_common()
        return [category for category, _ in categories]

    def get_popular_items(self, top_n: int = 10) -> List[str]:
        popular = [item for item, _ in self.popularity.most_common(top_n)]
        if len(popular) < top_n:
            missing = [item_id for item_id in self.products if item_id not in popular]
            popular.extend(missing[: top_n - len(popular)])
        return popular

    def get_similar_items(self, item_id: str, top_n: int = 5) -> List[str]:
        if item_id not in self.item_similarity:
            return []
        similar = sorted(
            self.item_similarity[item_id].items(), key=lambda pair: (-pair[1], pair[0])
        )
        return [item for item, _ in similar[:top_n]]

    def _score_candidate(self, user_id: str, item_id: str, recent_item: Optional[str] = None) -> float:
        product = self.products[item_id]
        score = 0.0
        score += self.popularity[item_id] * 1.0
        score += product.rating * 2.0
        if recent_item and recent_item in self.item_similarity and item_id in self.item_similarity[recent_item]:
            score += self.item_similarity[recent_item][item_id] * 2.5
        category_profile = self.user_categories[user_id]
        score += category_profile.get(product.category, 0) * 2.0
        if any(term in product.tags for term in self.user_search_terms[user_id]):
            score += 2.0
        if item_id in self.users[user_id].cart_items:
            score += 1.5
        if item_id in self.users[user_id].viewed_items:
            score += 0.5
        return score

    def _collect_candidates(self, user_id: str, recent_item: Optional[str] = None, k: int = 30) -> Set[str]:
        candidates: Set[str] = set()
        if recent_item and recent_item in self.products:
            candidates.update(self.get_similar_items(recent_item, top_n=k))
        profile_categories = self.get_user_profile(user_id)
        for category in profile_categories[:2]:
            candidates.update(self.products_by_category.get(category, [])[:k])
        candidates.update(self.get_popular_items(top_n=k))
        if user_id in self.users and self.users[user_id].search_history:
            keywords = set(self.user_search_terms[user_id].keys())
            for item_id, product in self.products.items():
                if len(keywords & set(product.tags)) >= 1:
                    candidates.add(item_id)
        return candidates

    def recommend(
        self,
        user_id: str,
        k: int = 10,
        recent_item: Optional[str] = None,
        explore: float = 0.1,
        filter_purchased: bool = True,
    ) -> List[Dict]:
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)

        candidates = self._collect_candidates(user_id, recent_item=recent_item, k=max(30, k * 3))
        purchased = set(self.users[user_id].purchased_items)
        scored_candidates = []

        for item_id in candidates:
            if filter_purchased and item_id in purchased:
                continue
            if item_id not in self.products:
                continue
            score = self._score_candidate(user_id, item_id, recent_item=recent_item)
            scored_candidates.append({"item_id": item_id, "score": score})

        if not scored_candidates:
            scored_candidates = [{"item_id": item_id, "score": self.popularity[item_id]} for item_id in self.get_popular_items(top_n=k)]

        top_items = heapq.nlargest(k, scored_candidates, key=lambda item: item["score"])

        if self.random_seed.random() < explore:
            unexplored = [item_id for item_id in self.products if item_id not in purchased]
            if unexplored:
                replace_item = self.random_seed.choice(unexplored)
                if replace_item not in [item["item_id"] for item in top_items]:
                    insertion_index = min(len(top_items) - 1, max(0, k - 1))
                    top_items[insertion_index] = {"item_id": replace_item, "score": top_items[insertion_index]["score"] * 0.75}

        return top_items

    def recommend_similar_products(self, item_id: str, k: int = 5) -> List[Dict]:
        similar_ids = self.get_similar_items(item_id, top_n=k)
        return [
            {
                "item_id": candidate_id,
                "score": self.item_similarity.get(item_id, {}).get(candidate_id, 0.0),
            }
            for candidate_id in similar_ids
        ]

    def generate_report(self, user_id: str, recent_item: Optional[str] = None, k: int = 10, explore: float = 0.1) -> str:
        recommendations = self.recommend(user_id, k=k, recent_item=recent_item, explore=explore)
        lines = [f"Recommendation Report for user: {user_id}", "=" * 40]
        profile = self.get_user_profile(user_id)
        lines.append(f"Recent item: {recent_item or 'None'}")
        lines.append(f"Top categories in profile: {', '.join(profile) if profile else 'No category history'}")
        lines.append("")
        lines.append("Top recommendations:")
        for rank, item in enumerate(recommendations, start=1):
            product = self.products[item["item_id"]]
            lines.append(
                f"{rank}. {product.title} ({product.item_id}) | category={product.category} | brand={product.brand} | price=${product.price:.2f} | score={item['score']:.2f}"
            )
        report_text = "\n".join(lines)
        return report_text

    def print_user_summary(self, user_id: str) -> str:
        if user_id not in self.users:
            return f"No user found for user_id={user_id}."
        user = self.users[user_id]
        lines = [f"User summary for {user_id}", "=" * 30]
        lines.append(f"Search history: {user.search_history}")
        lines.append(f"Cart items: {user.cart_items}")
        lines.append(f"Purchased items: {user.purchased_items}")
        lines.append(f"Viewed items: {user.viewed_items}")
        lines.append(f"Favorite categories: {self.get_user_profile(user_id)}")
        return "\n".join(lines)

    def print_product_catalog(self) -> str:
        lines = ["Product catalog", "=" * 30]
        for item in sorted(self.products.values(), key=lambda p: (p.category, p.item_id)):
            lines.append(
                f"{item.item_id}: {item.title} | category={item.category} | brand={item.brand} | price=${item.price:.2f} | rating={item.rating:.1f}"
            )
        return "\n".join(lines)
